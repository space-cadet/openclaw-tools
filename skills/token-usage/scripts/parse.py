#!/usr/bin/env python3
"""Parse OpenClaw session JSONL files and aggregate token usage."""

import json
import gzip
import argparse
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import glob
import os

DEFAULT_PRICING = {
    "kimi/k2.7": {"input": 0.50, "output": 2.00, "cache_read": 0.10, "cache_write": 1.00},
    "kimi/k3": {"input": 0.50, "output": 2.00, "cache_read": 0.10, "cache_write": 1.00},
    "kimi/k2.7-code": {"input": 0.50, "output": 2.00, "cache_read": 0.10, "cache_write": 1.00},
    "anthropic/claude-sonnet-4-5": {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75},
    "openai/gpt-4o": {"input": 2.50, "output": 10.00, "cache_read": 1.25, "cache_write": 0},
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60, "cache_read": 0.075, "cache_write": 0},
}

MODEL_ALIASES = {
    "k2.7": "kimi/k2.7",
    "k3": "kimi/k3",
    "k2.7-code": "kimi/k2.7-code",
    "kimi-for-coding": "kimi/k2.7-code",
    "claude-sonnet-4-5": "anthropic/claude-sonnet-4-5",
    "gpt-4o": "openai/gpt-4o",
    "gpt-4o-mini": "openai/gpt-4o-mini",
}


def normalize_model(model_name):
    """Map raw model names to pricing keys."""
    if not model_name:
        return "unknown"
    # Direct match
    if model_name in DEFAULT_PRICING:
        return model_name
    # Alias match
    if model_name in MODEL_ALIASES:
        return MODEL_ALIASES[model_name]
    # Provider prefix match (e.g., "kimi/k2.7" -> already handled)
    for alias, canonical in MODEL_ALIASES.items():
        if alias in model_name.lower():
            return canonical
    return model_name


def load_pricing():
    pricing_file = Path(__file__).parent / "pricing.json"
    if pricing_file.exists():
        with open(pricing_file) as f:
            return {**DEFAULT_PRICING, **json.load(f)}
    return DEFAULT_PRICING



def find_sessions(base_paths=None, since=None):
    if base_paths is None:
        base_paths = [
            Path.home() / ".openclaw" / "agents" / "main" / "sessions",
            Path.home() / ".openclaw" / "agents" / "sub" / "sessions",
        ]
    sessions = []
    for bp in base_paths:
        if not bp.exists():
            continue
        for ext in ["*.jsonl", "*.jsonl.gz"]:
            for spath in glob.glob(str(bp / ext)):
                # Skip trajectory files and temp files
                if ".trajectory." in spath or ".fs-safe-replace." in spath:
                    continue
                # If since is given, skip files modified before that time
                if since:
                    try:
                        mtime = os.path.getmtime(spath)
                        since_ts = datetime.fromisoformat(since.replace('Z', '+00:00')).timestamp()
                        if mtime < since_ts:
                            continue
                    except Exception:
                        pass
                sessions.append(spath)
    return sorted(set(sessions))


def parse_session_file(path):
    """Yield (timestamp, model, usage_dict) for each assistant message."""
    open_fn = gzip.open if path.endswith(".gz") else open
    with open_fn(path, "rt", encoding="utf-8", errors="replace") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                continue
            if msg.get("type") != "message":
                continue
            m = msg.get("message", {})
            if m.get("role") != "assistant":
                continue
            usage = m.get("usage") or msg.get("usage")
            if not usage:
                continue
            ts = msg.get("timestamp", "")
            model = m.get("model", msg.get("model", msg.get("api", "")))
            yield ts, model, usage


def aggregate(sessions, since=None, until=None):
    by_day = defaultdict(lambda: defaultdict(lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0
    }))
    by_session = defaultdict(lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "models": set()
    })

    for spath in sessions:
        sid = Path(spath).stem
        for ts, model, usage in parse_session_file(spath):
            if since and ts < since:
                continue
            if until and ts > until:
                continue
            day = ts[:10] if ts else "unknown"
            model_key = normalize_model(model)

            inp = usage.get("input", 0)
            out = usage.get("output", 0)
            cr = usage.get("cacheRead", 0) or usage.get("cache_read", 0)
            cw = usage.get("cacheWrite", 0) or usage.get("cache_write", 0)

            d = by_day[day][model_key]
            d["input"] += inp
            d["output"] += out
            d["cacheRead"] += cr
            d["cacheWrite"] += cw
            d["messages"] += 1

            s = by_session[sid]
            s["input"] += inp
            s["output"] += out
            s["cacheRead"] += cr
            s["cacheWrite"] += cw
            s["messages"] += 1
            s["models"].add(model_key)

    return by_day, by_session


def detect_cron_job(path):
    """Extract cron job ID and name from first user message in session."""
    open_fn = gzip.open if path.endswith(".gz") else open
    try:
        with open_fn(path, "rt", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if msg.get("type") != "message":
                    continue
                m = msg.get("message", {})
                if m.get("role") != "user":
                    continue
                content = m.get("content", [])
                text = ""
                for c in content:
                    if isinstance(c, dict) and c.get("type") == "text":
                        text += c.get("text", "")
                match = re.search(r'\[cron:([a-f0-9\-]+)\s+([^\]]+)\]', text)
                if match:
                    return match.group(1), match.group(2).strip()
                match2 = re.search(r'\[cron:([a-z0-9\-]+)\s+([^\]]+)\]', text)
                if match2:
                    return match2.group(1), match2.group(2).strip()
                break
    except Exception:
        pass
    return None, None


def aggregate_by_cron(sessions, since=None, until=None):
    """Aggregate token usage by cron job and date."""
    by_day_job = defaultdict(lambda: {
        "input": 0, "output": 0, "messages": 0, "name": ""
    })

    for spath in sessions:
        job_id, job_name = detect_cron_job(spath)
        if not job_id:
            continue
        for ts, model, usage in parse_session_file(spath):
            if since and ts < since:
                continue
            if until and ts > until:
                continue
            day = ts[:10] if ts else "unknown"
            key = f"{day}:{job_id}"

            inp = usage.get("input", 0)
            out = usage.get("output", 0)

            by_day_job[key]["input"] += inp
            by_day_job[key]["output"] += out
            by_day_job[key]["messages"] += 1
            if job_name and not by_day_job[key]["name"]:
                by_day_job[key]["name"] = job_name

    return by_day_job


def estimate_cost(usage, model, pricing):
    """Estimate cost in USD. Prices are per 1M tokens."""
    p = pricing.get(model, pricing.get("kimi/k2.7", {}))
    cost = 0.0
    cost += usage.get("input", 0) * p.get("input", 0) / 1e6
    cost += usage.get("output", 0) * p.get("output", 0) / 1e6
    cost += usage.get("cacheRead", 0) * p.get("cache_read", 0) / 1e6
    cost += usage.get("cacheWrite", 0) * p.get("cache_write", 0) / 1e6
    return cost


def format_report(by_day, by_session, pricing=None, costs=False, show_cache=False, session_detail=False):
    lines = []
    total = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "cost": 0.0}

    for day in sorted(by_day.keys(), reverse=True):
        lines.append(f"\n## {day}")
        day_total = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "cost": 0.0}
        for model in sorted(by_day[day].keys()):
            u = by_day[day][model]
            usage_for_cost = {
                "input": u["input"], "output": u["output"],
                "cacheRead": u["cacheRead"], "cacheWrite": u["cacheWrite"]
            }
            c = estimate_cost(usage_for_cost, model, pricing) if (costs and pricing) else 0.0
            cache_str = ""
            if show_cache:
                cache_str = f"  cacheR={u['cacheRead']:>10,}  cacheW={u['cacheWrite']:>8,}"
            lines.append(f"  {model:30s}  in={u['input']:>10,}  out={u['output']:>8,}{cache_str}  msgs={u['messages']:>4}")
            if costs and pricing:
                lines.append(f"{'':34s}est. ${c:.4f}")
            for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]:
                day_total[k] += u[k]
            day_total["cost"] += c
            for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]:
                total[k] += u[k]
            total["cost"] += c
        cache_str = ""
        if show_cache:
            cache_str = f"  cacheR={day_total['cacheRead']:>10,}  cacheW={day_total['cacheWrite']:>8,}"
        lines.append(f"  {'Day total':30s}  in={day_total['input']:>10,}  out={day_total['output']:>8,}{cache_str}  msgs={day_total['messages']:>4}")
        if costs and pricing:
            lines.append(f"  {'':34s}est. ${day_total['cost']:.4f}")

    # Session detail
    if session_detail:
        lines.append(f"\n## Sessions")
        for sid, s in sorted(by_session.items(), key=lambda x: x[1]["input"] + x[1]["output"], reverse=True):
            if s["messages"] == 0:
                continue
            models_str = ", ".join(sorted(s["models"]))
            lines.append(f"  {sid[:8]:8s}  in={s['input']:>10,}  out={s['output']:>8,}  msgs={s['messages']:>4}  [{models_str}]")

    lines.append(f"\n## Grand Total")
    cache_str = ""
    if show_cache:
        cache_str = f"  cacheR={total['cacheRead']:,}  cacheW={total['cacheWrite']:,}"
    lines.append(f"  input={total['input']:,}  output={total['output']:,}{cache_str}  messages={total['messages']:,}")
    if costs and pricing:
        lines.append(f"  est. cost=${total['cost']:.4f}")

    return "\n".join(lines)


def format_cron_report(by_day_job, pricing=None, costs=False):
    lines = []
    total = {"input": 0, "output": 0, "messages": 0, "cost": 0.0}

    days = defaultdict(dict)
    for key, data in by_day_job.items():
        day, job_id = key.split(":", 1)
        days[day][job_id] = data

    for day in sorted(days.keys(), reverse=True):
        lines.append(f"\n## {day}")
        day_total = {"input": 0, "output": 0, "messages": 0, "cost": 0.0}

        jobs = sorted(days[day].items(),
                     key=lambda x: x[1]["input"] + x[1]["output"],
                     reverse=True)

        for job_id, data in jobs:
            name = data.get("name", job_id[:8])
            if len(name) > 28:
                name = name[:25] + "..."

            usage_for_cost = {"input": data["input"], "output": data["output"], "cacheRead": 0, "cacheWrite": 0}
            c = estimate_cost(usage_for_cost, "kimi/k2.7", pricing) if (costs and pricing) else 0.0

            lines.append(f"  {name:<28}  calls={data['messages']:>4}  in={data['input']:>10,}  out={data['output']:>8,}")
            if costs and pricing:
                lines.append(f"{'':34s}est. ${c:.4f}")

            for k in ["input", "output", "messages"]:
                day_total[k] += data[k]
            day_total["cost"] += c
            for k in ["input", "output", "messages"]:
                total[k] += data[k]
            total["cost"] += c

        lines.append(f"  {'DAY TOTAL':<28}  calls={day_total['messages']:>4}  in={day_total['input']:>10,}  out={day_total['output']:>8,}")
        if costs and pricing:
            lines.append(f"  {'':34s}est. ${day_total['cost']:.4f}")

    lines.append(f"\n## Grand Total")
    lines.append(f"  input={total['input']:,}  output={total['output']:,}  messages={total['messages']:,}")
    if costs and pricing:
        lines.append(f"  est. cost=${total['cost']:.4f}")

    return "\n".join(lines)


def to_json(by_day, by_session, pricing=None):
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "days": {},
        "sessions": {}
    }
    for day, models in by_day.items():
        out["days"][day] = {}
        for model, u in models.items():
            d = {k: v for k, v in u.items() if k != "messages"}
            d["messages"] = u["messages"]
            if pricing:
                usage_for_cost = {
                    "input": u["input"], "output": u["output"],
                    "cacheRead": u["cacheRead"], "cacheWrite": u["cacheWrite"]
                }
                d["estimated_cost_usd"] = round(estimate_cost(usage_for_cost, model, pricing), 6)
            out["days"][day][model] = d
    for sid, s in by_session.items():
        out["sessions"][sid] = {
            **{k: s[k] for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]},
            "models": list(s["models"])
        }
    return out


def to_cron_json(by_day_job, pricing=None):
    out = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "days": {}
    }
    for key, data in by_day_job.items():
        day, job_id = key.split(":", 1)
        if day not in out["days"]:
            out["days"][day] = {}
        d = {
            "name": data.get("name", ""),
            "input": data["input"],
            "output": data["output"],
            "messages": data["messages"]
        }
        if pricing:
            usage_for_cost = {"input": data["input"], "output": data["output"], "cacheRead": 0, "cacheWrite": 0}
            d["estimated_cost_usd"] = round(estimate_cost(usage_for_cost, "kimi/k2.7", pricing), 6)
        out["days"][day][job_id] = d
    return out


def parse_time_arg(arg):
    """Parse ISO timestamp or YYYY-MM-DD."""
    if not arg:
        return None
    # Try ISO format
    for fmt in ["%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d"]:
        try:
            dt = datetime.strptime(arg, fmt)
            return dt.replace(tzinfo=timezone.utc).isoformat()
        except ValueError:
            continue
    # Try relative: 1d, 2h, 30m
    m = re.match(r'^(\d+)([dhm])$', arg.lower())
    if m:
        num, unit = int(m.group(1)), m.group(2)
        now = datetime.now(timezone.utc)
        if unit == 'd':
            since = now - timedelta(days=num)
        elif unit == 'h':
            since = now - timedelta(hours=num)
        else:
            since = now - timedelta(minutes=num)
        return since.isoformat()
    raise argparse.ArgumentTypeError(f"Cannot parse time: {arg}. Use ISO timestamp (YYYY-MM-DDTHH:MM:SS), date (YYYY-MM-DD), or relative (1d, 2h, 30m).")


def main():
    parser = argparse.ArgumentParser(description="Track OpenClaw token usage")
    parser.add_argument("--today", action="store_true", help="Report for today (calendar day UTC)")
    parser.add_argument("--yesterday", action="store_true", help="Report for yesterday")
    parser.add_argument("--week", action="store_true", help="Report for last 7 calendar days")
    parser.add_argument("--days", type=int, metavar="N", help="Report for last N calendar days")
    parser.add_argument("--hours", type=int, metavar="N", help="Report for last N hours")
    parser.add_argument("--since", type=str, metavar="TIME", help="Start time: ISO, YYYY-MM-DD, or relative (1d, 2h, 30m)")
    parser.add_argument("--until", type=str, metavar="TIME", help="End time: ISO, YYYY-MM-DD, or relative")
    parser.add_argument("--all", action="store_true", help="Report all time")
    parser.add_argument("--by-model", action="store_true", help="Group by model")
    parser.add_argument("--by-cron", action="store_true", help="Group by cron job")
    parser.add_argument("--costs", action="store_true", help="Estimate costs")
    parser.add_argument("--cache", action="store_true", help="Include cache read/write in report")
    parser.add_argument("--session-detail", action="store_true", help="Show per-session breakdown")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--sessions", nargs="*", help="Specific session files")
    args = parser.parse_args()

    now = datetime.now(timezone.utc)
    since = None
    until = None
    period_desc = "all time"

    # Handle time range
    if args.hours:
        since = (now - timedelta(hours=args.hours)).isoformat()
        period_desc = f"last {args.hours}h"
    elif args.since or args.until:
        since = parse_time_arg(args.since) if args.since else None
        until = parse_time_arg(args.until) if args.until else None
        period_desc = f"{args.since or 'start'} to {args.until or 'now'}"
    elif args.today:
        since = now.strftime("%Y-%m-%dT00:00:00")
        period_desc = "today"
    elif args.yesterday:
        yesterday = now - timedelta(days=1)
        since = yesterday.strftime("%Y-%m-%dT00:00:00")
        until = now.strftime("%Y-%m-%dT00:00:00")
        period_desc = "yesterday"
    elif args.week:
        since = (now - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00")
        period_desc = "last 7 days"
    elif args.days:
        since = (now - timedelta(days=args.days)).strftime("%Y-%m-%dT00:00:00")
        period_desc = f"last {args.days} days"
    elif not args.all:
        args.today = True
        since = now.strftime("%Y-%m-%dT00:00:00")
        period_desc = "today"

    sessions = args.sessions or find_sessions(since=since)
    if not sessions:
        print("No session files found.", file=sys.stderr)
        return

    pricing = load_pricing() if args.costs else None

    # Header
    if not args.json:
        print(f"# Token Usage Report — {period_desc}")

    if args.by_cron:
        by_day_job = aggregate_by_cron(sessions, since=since, until=until)
        if args.json:
            print(json.dumps(to_cron_json(by_day_job, pricing), indent=2))
        else:
            print(format_cron_report(by_day_job, pricing, args.costs))
    else:
        by_day, by_session = aggregate(sessions, since=since, until=until)
        if args.json:
            print(json.dumps(to_json(by_day, by_session, pricing), indent=2))
        else:
            print(format_report(by_day, by_session, pricing, args.costs, args.cache, args.session_detail))


if __name__ == "__main__":
    main()
