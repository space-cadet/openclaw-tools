#!/usr/bin/env python3
"""Parse OpenClaw session JSONL files and aggregate token usage."""

import json
import gzip
import os
import subprocess
import contextlib
import sqlite3
import tempfile
from pathlib import Path
from zoneinfo import ZoneInfo

LOCAL_TZ = ZoneInfo("Asia/Calcutta")
import argparse
import re
from pathlib import Path
from datetime import datetime, timedelta, timezone
from collections import defaultdict
import glob

DEFAULT_PRICING = {
    "kimi/k2.7": {"input": 0.90, "output": 3.75, "cache_read": 0.10, "cache_write": 1.00},
    "kimi/k2.7-code": {"input": 0.90, "output": 3.75, "cache_read": 0.10, "cache_write": 1.00},
    "kimi/k3": {"input": 2.78, "output": 13.89, "cache_read": 0.28, "cache_write": 2.78},
    "kimi/k3-1m": {"input": 2.78, "output": 13.89, "cache_read": 0.28, "cache_write": 2.78},
    "anthropic/claude-sonnet-4.5": {"input": 3.00, "output": 15.00, "cache_read": 0.30, "cache_write": 3.75},
    "openai/gpt-4o": {"input": 2.50, "output": 10.00, "cache_read": 1.25, "cache_write": 0},
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60, "cache_read": 0.075, "cache_write": 0},
    "openai/gpt-5.6-luna": {"input": 0.20, "output": 1.20, "cache_read": 0.02, "cache_write": 0},
    "openai/gpt-5.6-terra": {"input": 2.00, "output": 12.00, "cache_read": 0.20, "cache_write": 0},
    "openai/gpt-5.4": {"input": 2.50, "output": 15.00, "cache_read": 0.25, "cache_write": 0},
}

def _detect_openclaw_version():
    """Return the installed OpenClaw version string, or None on failure.

    Resolution order:
      1. Scan every NVM node tree for an openclaw install and return the
         **newest** version found. The gateway almost always runs from the
         latest install, and old trees are typically left behind after an
         upgrade, so max() is the safest single guess.
      2. Fall back to system-wide install paths.

    Never shells out to `openclaw --version` because that can block when the
    gateway is busy or the CLI is waiting on a lock.
    """
    found = []

    nvm_base = Path.home() / ".nvm" / "versions" / "node"
    if nvm_base.exists():
        for node_dir in sorted(nvm_base.iterdir()):
            pkg = node_dir / "lib" / "node_modules" / "openclaw" / "package.json"
            if pkg.exists():
                try:
                    ver = json.loads(pkg.read_text()).get("version", "")
                    if ver:
                        found.append(ver)
                except (json.JSONDecodeError, OSError):
                    continue

    for sys_pkg in (
        Path("/usr/lib/node_modules/openclaw/package.json"),
        Path("/usr/local/lib/node_modules/openclaw/package.json"),
        Path("/opt/homebrew/lib/node_modules/openclaw/package.json"),
    ):
        if sys_pkg.exists():
            try:
                ver = json.loads(sys_pkg.read_text()).get("version", "")
                if ver:
                    found.append(ver)
            except (json.JSONDecodeError, OSError):
                continue

    if not found:
        return None

    # Newest version wins. Versions are 'YYYY.M.P' — parse to a tuple for
    # reliable numeric comparison, then return the original string.
    def _key(v):
        return tuple(int(p) for p in v.split(".") if p.isdigit())

    try:
        return max(found, key=_key)
    except (ValueError, TypeError):
        return found[-1]


def _version_major_minor(version_str):
    """Return (major, minor) tuple from a version string like '2026.9.4'."""
    if not version_str:
        return None
    m = re.match(r"(\d+)\.(\d+)", version_str)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def detect_storage_backends():
    """Detect which session-storage backends are present for this install.

    Returns a dict with keys:
      version        – detected OpenClaw version string or None
      version_mm     – (major, minor) tuple or None
      jsonl_sessions – list of loose .jsonl / .jsonl.gz files found
      sqlite_dbs     – list of openclaw-agent.sqlite paths found
      zst_archives   – list of .jsonl.deleted.*.zst files found
      primary        – 'jsonl' | 'sqlite' | 'mixed' | 'unknown'
      warnings       – list of human-readable warning strings
    """
    version = _detect_openclaw_version()
    version_mm = _version_major_minor(version)

    jsonl_sessions = find_sessions()
    sqlite_dbs = list(_sqlite_transcript_sources())
    zst_archives = [
        p for p in jsonl_sessions if ".deleted." in p or p.endswith(".zst")
    ]
    loose_jsonl = [p for p in jsonl_sessions if p not in zst_archives]

    warnings = []

    if version_mm:
        # 9.x or later: (major, minor) tuple compare — a naive
        # `major >= 2026 and minor >= 9` misclassifies 2027.x as pre-9.x.
        if version_mm >= (2026, 9):
            # 9.x: SQLite is the primary live backend, JSONL may still exist
            # for older rotated sessions.
            if sqlite_dbs and not loose_jsonl:
                primary = "sqlite"
            elif sqlite_dbs and loose_jsonl:
                primary = "mixed"
                warnings.append(
                    "Mixed storage: SQLite (9.x live) + loose JSONL files detected. "
                    "Ensure the SQLite DB is readable to avoid silently missing recent sessions."
                )
            elif not sqlite_dbs and loose_jsonl:
                primary = "jsonl"
                warnings.append(
                    f"OpenClaw {version} normally stores live sessions in SQLite, "
                    "but no openclaw-agent.sqlite was found. "
                    "Falling back to JSONL only — recent sessions may be missing."
                )
            else:
                primary = "unknown"
                warnings.append("No session storage backends detected.")
        else:
            # Pre-9.x: JSONL is the only backend.
            if loose_jsonl:
                primary = "jsonl"
                if sqlite_dbs:
                    warnings.append(
                        f"OpenClaw {version} predates the SQLite storage migration "
                        "but an openclaw-agent.sqlite file is present. "
                        "The SQLite data will be ignored to match the installed version."
                    )
            elif sqlite_dbs and not loose_jsonl:
                primary = "sqlite"
                warnings.append(
                    f"OpenClaw {version} predates the SQLite storage migration "
                    "but only SQLite storage was found. "
                    "This may be a stale DB from a previous 9.x install."
                )
            else:
                primary = "unknown"
                warnings.append("No session storage backends detected.")
    else:
        # Version unknown — infer from what is present.
        if sqlite_dbs and loose_jsonl:
            primary = "mixed"
            warnings.append(
                "Could not determine OpenClaw version; "
                "both SQLite and JSONL storage detected. Reading both."
            )
        elif sqlite_dbs:
            primary = "sqlite"
            warnings.append(
                "Could not determine OpenClaw version; "
                "SQLite storage detected (OpenClaw 2026.9.x or later)."
            )
        elif loose_jsonl:
            primary = "jsonl"
            warnings.append(
                "Could not determine OpenClaw version; "
                "JSONL storage detected (OpenClaw 2026.6.x or earlier)."
            )
        else:
            primary = "unknown"
            warnings.append("No session storage backends detected.")

    return {
        "version": version,
        "version_mm": version_mm,
        "jsonl_sessions": loose_jsonl,
        "sqlite_dbs": [str(p) for p in sqlite_dbs],
        "zst_archives": zst_archives,
        "primary": primary,
        "warnings": warnings,
    }


def load_pricing():
    pricing_file = Path(__file__).parent / "pricing.json"
    if pricing_file.exists():
        with open(pricing_file) as f:
            return {**DEFAULT_PRICING, **json.load(f)}
    return DEFAULT_PRICING

def find_sessions(base_paths=None, since=None):
    """Find session files, optionally filtering by modification time.

    When *since* is given (ISO date-time string), skip files whose mtime is
    older than the start of that window. JSONL files are append-only, so the
    mtime is a reliable upper bound on the newest event they can contain.
    This avoids opening thousands of stale files when we only need today.
    """
    if base_paths is None:
        base_paths = [
            Path.home() / ".openclaw" / "agents" / "main" / "sessions",
            Path.home() / ".openclaw" / "agents" / "sub" / "sessions",
            # Codex app-server rollout logs use a nested YYYY/MM/DD layout.
            Path.home() / ".openclaw" / "agents" / "main" / "agent" / "codex-home" / "sessions",
        ]

    mtime_floor = None
    if since:
        try:
            dt = datetime.fromisoformat(since.replace("Z", "+00:00"))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=LOCAL_TZ)
            # Convert to Unix timestamp for comparison with os.path.getmtime()
            mtime_floor = dt.timestamp()
        except (ValueError, TypeError):
            mtime_floor = None

    sessions = []
    for bp in base_paths:
        if bp.exists():
            for pat in ("**/*.jsonl", "**/*.jsonl.gz", "**/*.jsonl.deleted.*.zst"):
                for p in glob.glob(str(bp / pat), recursive=True):
                    if mtime_floor is not None:
                        try:
                            if os.path.getmtime(p) < mtime_floor:
                                continue
                        except OSError:
                            continue
                    sessions.append(p)
    return sorted(set(sessions))

# ---------------------------------------------------------------------------
# SQLite transcript backend (OpenClaw 2026.9.x)
# ---------------------------------------------------------------------------
# Since the 9.x storage migration, live session transcripts live in
# `~/.openclaw/agents/<agent>/agent/openclaw-agent.sqlite` (table
# `transcript_events.event_json`), not as loose `.jsonl` files. Ended-session
# JSONL is additionally rotated to zstd archives or SQLite `archive_blob`s.
# The live DB is protected state: `exec` refuses to open it in place, so we
# snapshot it to a temp copy and read that.
_SQLITE_DB_CANDIDATES = [
    "agents/main/agent/openclaw-agent.sqlite",
    "agents/sub/agent/openclaw-agent.sqlite",
]

def _sqlite_transcript_sources(state_dir=None):
    """Yield (path, session_id) for the agent SQLite transcript DBs."""
    root = Path(state_dir) if state_dir else Path.home() / ".openclaw"
    for rel in _SQLITE_DB_CANDIDATES:
        p = root / rel
        if p.exists():
            yield p

def _snapshot_sqlite(db_path):
    """Snapshot the live DB to a temp file so we can read it without holding the
    production lock or tripping the protected-state guard.

    Uses the SQLite online-backup API rather than a raw file copy: the live DB
    is under constant write (WAL), and a plain shutil.copyfile can catch a torn
    checkpoint, yielding a copy sqlite3 then refuses to open ("unable to open
    database file"). sqlite3.Connection.backup copies a consistent snapshot even
    while the source is being written.

    Snapshots to /tmp, NOT tempfile.gettempdir(): OpenClaw sets TMPDIR to
    ~/.openclaw/tmp, which is inside the protected state dir and sqlite3 refuses
    to open databases there. /tmp is genuinely outside the guard.

    Returns the temp path, or None on failure. Caller must unlink it."""
    fd, tmp = tempfile.mkstemp(suffix=".sqlite", prefix="oc-tok-", dir="/tmp")
    os.close(fd)
    try:
        src = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            dst = sqlite3.connect(tmp)
            try:
                src.backup(dst)
            finally:
                dst.close()
        finally:
            src.close()
        return tmp
    except (sqlite3.Error, OSError):
        try:
            os.unlink(tmp)
        except OSError:
            pass
        return None

def _normalise_ts(ts):
    """Convert an ISO-8601 timestamp to a naive local (IST) string.

    Session files and the SQLite backend store UTC timestamps with a 'Z'
    suffix (e.g. '2026-09-18T15:06:59.778Z'). The --since / --until
    boundaries are local IST strings, and day buckets must follow IST
    midnights (the standing "all timestamps in IST" reporting rule).
    So we convert UTC -> IST and drop tzinfo, matching the pre-9.x
    local_timestamp()/local_date() behaviour. Unparseable timestamps are
    returned as-is so string comparison never crashes.
    """
    if not ts:
        return ""
    try:
        parsed = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(LOCAL_TZ).replace(tzinfo=None).isoformat(timespec="seconds")
    except ValueError:
        return ts


def parse_sqlite_transcripts(db_path, since=None, until=None):
    """Yield (timestamp, model, usage_dict) from transcript_events.event_json."""
    snap = _snapshot_sqlite(db_path)
    if not snap:
        return
    try:
        # Use plain connect, not URI mode — macOS sqlite3 can refuse to open
        # a freshly-created temp file in URI read-only mode.
        con = sqlite3.connect(snap)
        cur = con.cursor()
        try:
            rows = cur.execute(
                "SELECT event_json FROM transcript_events"
                " WHERE event_json LIKE '%\"usage\"%'"
            )
            for (event_json,) in rows:
                try:
                    d = json.loads(event_json)
                except (json.JSONDecodeError, TypeError):
                    continue
                m = d.get("message") or {}
                if m.get("role") != "assistant":
                    continue
                usage = m.get("usage")
                if not usage:
                    continue
                ts = d.get("timestamp") or d.get("ts") or ""
                model = m.get("model") or d.get("model") or d.get("api") or ""
                yield _normalise_ts(ts), model, usage
        finally:
            con.close()
    except sqlite3.Error:
        pass
    finally:
        try:
            os.unlink(snap)
        except OSError:
            pass

def aggregate_sqlite(since=None, until=None):
    """Aggregate token usage straight from the SQLite transcript backend."""
    by_day = defaultdict(lambda: defaultdict(lambda: {
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0
    }))
    total = 0
    for db in _sqlite_transcript_sources():
        for ts, model, usage in parse_sqlite_transcripts(db, since, until):
            if since and ts < since:
                continue
            if until and ts >= until:
                continue
            day = ts[:10] if ts else "unknown"
            key = model or "unknown"
            d = by_day[day][key]
            d["input"] += usage.get("input", 0)
            d["output"] += usage.get("output", 0)
            d["cacheRead"] += usage.get("cacheRead", 0)
            d["cacheWrite"] += usage.get("cacheWrite", 0)
            d["messages"] += 1
            total += 1
    return by_day, total

def parse_session_file(path):
    """Yield (timestamp, model, usage_dict) for each assistant message."""
    path = str(path)
    if ".deleted." in path or path.endswith(".zst"):
        ctx = contextlib.closing(_zstd_stream(path))
    elif path.endswith(".gz"):
        ctx = gzip.open(path, "rt", encoding="utf-8", errors="replace")
    else:
        ctx = open(path, "rt", encoding="utf-8", errors="replace")
    try:
        with ctx as f:
            codex_model = ""
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                # Codex rollout logs emit cumulative token_count events.  The
                # last_token_usage object is per-turn, so it is safe to sum.
                if msg.get("type") == "event_msg":
                    payload = msg.get("payload", {})
                    if payload.get("type") == "token_count":
                        info = payload.get("info") or {}
                        usage = info.get("last_token_usage") or {}
                        if usage:
                            yield (
                                _normalise_ts(msg.get("timestamp", "")),
                                codex_model or "openai/gpt-5.6-luna",
                                {
                                    "input": usage.get("input_tokens", 0),
                                    "output": usage.get("output_tokens", 0),
                                    "cacheRead": usage.get("cached_input_tokens", 0),
                                    "cacheWrite": usage.get("cache_write_input_tokens", 0),
                                },
                            )
                    continue
                if msg.get("type") == "turn_context":
                    codex_model = msg.get("payload", {}).get("model", "") or codex_model
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
                yield _normalise_ts(ts), model, usage
    except (FileNotFoundError, OSError):
        pass

def _zstd_stream(path):
    """Yield decompressed text lines from a zstd-compressed session archive."""
    proc = subprocess.Popen(
        ["zstd", "-d", "-c", "--", path],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    try:
        for line in proc.stdout:
            yield line
    finally:
        proc.stdout.close()
        proc.wait()


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
            if until and ts >= until:
                continue
            day = ts[:10] if ts else "unknown"
            model_key = model or "unknown"
            
            inp = usage.get("input", 0)
            out = usage.get("output", 0)
            
            d = by_day[day][model_key]
            d["input"] += inp
            d["output"] += out
            d["cacheRead"] += usage.get("cacheRead", 0)
            d["cacheWrite"] += usage.get("cacheWrite", 0)
            d["messages"] += 1
            
            s = by_session[sid]
            s["input"] += inp
            s["output"] += out
            s["cacheRead"] += usage.get("cacheRead", 0)
            s["cacheWrite"] += usage.get("cacheWrite", 0)
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
        "input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "name": "", "models": {}
    })
    
    for spath in sessions:
        job_id, job_name = detect_cron_job(spath)
        if not job_id:
            continue
        for ts, model, usage in parse_session_file(spath):
            if since and ts < since:
                continue
            if until and ts >= until:
                continue
            day = ts[:10] if ts else "unknown"
            key = f"{day}:{job_id}"
            
            inp = usage.get("input", 0)
            out = usage.get("output", 0)
            cache_read = usage.get("cacheRead", 0)
            cache_write = usage.get("cacheWrite", 0)
            model_key = model or "unknown"
            
            by_day_job[key]["input"] += inp
            by_day_job[key]["output"] += out
            by_day_job[key]["cacheRead"] += cache_read
            by_day_job[key]["cacheWrite"] += cache_write
            by_day_job[key]["messages"] += 1
            model_data = by_day_job[key]["models"].setdefault(model_key, {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0})
            model_data["input"] += inp
            model_data["output"] += out
            model_data["cacheRead"] += cache_read
            model_data["cacheWrite"] += cache_write
            if job_name and not by_day_job[key]["name"]:
                by_day_job[key]["name"] = job_name
    
    return by_day_job

def estimate_cost(usage, model, pricing):
    """Estimate cost in USD. Prices are per 1M tokens."""
    p = pricing.get(model)
    if p is None and "/" not in model:
        # Try common provider prefixes
        for prefix in ["kimi/", "openai/", "anthropic/", "google/", "deepseek/", "qwen/", "x-ai/"]:
            p = pricing.get(prefix + model)
            if p is not None:
                break
    if p is None:
        # Never silently price an unknown provider as Kimi.
        p = {}
    cost = 0.0
    cost += usage.get("input", 0) * (p.get("input") or 0) / 1e6
    cost += usage.get("output", 0) * (p.get("output") or 0) / 1e6
    cost += usage.get("cacheRead", 0) * (p.get("cache_read") or 0) / 1e6
    cost += usage.get("cacheWrite", 0) * (p.get("cache_write") or 0) / 1e6
    return cost

def format_report(by_day, by_session, pricing=None, costs=False):
    lines = []
    total = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "cost": 0.0}
    
    for day in sorted(by_day.keys(), reverse=True):
        lines.append(f"\n## {day}")
        day_total = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "cost": 0.0}
        for model in sorted(by_day[day].keys()):
            u = by_day[day][model]
            usage_for_cost = {"input": u["input"], "output": u["output"], "cacheRead": u["cacheRead"], "cacheWrite": u["cacheWrite"]}
            c = estimate_cost(usage_for_cost, model, pricing) if (costs and pricing) else 0.0
            lines.append(f"  {model:30s}  in={u['input']:>10,}  out={u['output']:>8,}  cache={u['cacheRead']:>8,}  msgs={u['messages']:>4}")
            if costs and pricing:
                lines.append(f"{'':34s}est. ${c:.4f}")
            for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]:
                day_total[k] += u[k]
            day_total["cost"] += c
            for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]:
                total[k] += u[k]
            total["cost"] += c
        lines.append(f"  {'Day total':30s}  in={day_total['input']:>10,}  out={day_total['output']:>8,}  cache={day_total['cacheRead']:>8,}  msgs={day_total['messages']:>4}")
        if costs and pricing:
            lines.append(f"  {'':34s}est. ${day_total['cost']:.4f}")
    
    lines.append(f"\n## Grand Total")
    lines.append(f"  input={total['input']:,}  output={total['output']:,}  cacheRead={total['cacheRead']:,}  messages={total['messages']:,}")
    if costs and pricing:
        lines.append(f"  est. cost=${total['cost']:.4f}")
    
    return "\n".join(lines)

def format_cron_report(by_day_job, pricing=None, costs=False):
    lines = []
    total = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "cost": 0.0}
    
    days = defaultdict(dict)
    for key, data in by_day_job.items():
        day, job_id = key.split(":", 1)
        days[day][job_id] = data
    
    for day in sorted(days.keys(), reverse=True):
        lines.append(f"\n## {day}")
        day_total = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0, "messages": 0, "cost": 0.0}
        
        jobs = sorted(days[day].items(), 
                     key=lambda x: x[1]["input"] + x[1]["output"], 
                     reverse=True)
        
        for job_id, data in jobs:
            name = data.get("name", job_id[:8])
            if len(name) > 28:
                name = name[:25] + "..."
            
            # Cost per model, not a blanket kimi/k2.7 rate — cron jobs run
            # Luna, k3, k2.7-code etc., and mispricing them skews reports.
            c = 0.0
            if costs and pricing:
                for model, usage in data.get("models", {}).items():
                    c += estimate_cost(usage, model, pricing)
            
            lines.append(f"  {name:<28}  calls={data['messages']:>4}  in={data['input']:>10,}  out={data['output']:>8,}  cache={data['cacheRead'] + data['cacheWrite']:>8,}")
            if costs and pricing:
                lines.append(f"{'':34s}est. ${c:.4f}")
            
            for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]:
                day_total[k] += data[k]
            day_total["cost"] += c
            for k in ["input", "output", "cacheRead", "cacheWrite", "messages"]:
                total[k] += data[k]
            total["cost"] += c
        
        lines.append(f"  {'DAY TOTAL':<28}  calls={day_total['messages']:>4}  in={day_total['input']:>10,}  out={day_total['output']:>8,}")
        if costs and pricing:
            lines.append(f"  {'':34s}est. ${day_total['cost']:.4f}")
    
    lines.append(f"\n## Grand Total")
    lines.append(f"  input={total['input']:,}  output={total['output']:,}  cacheRead={total['cacheRead']:,}  messages={total['messages']:,}")
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
            d = dict(u)
            if pricing:
                usage_for_cost = {"input": u["input"], "output": u["output"], "cacheRead": u["cacheRead"], "cacheWrite": u["cacheWrite"]}
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
            "cacheRead": data.get("cacheRead", 0),
            "cacheWrite": data.get("cacheWrite", 0),
            "messages": data["messages"]
        }
        if pricing:
            d["estimated_cost_usd"] = round(sum(estimate_cost(usage, model, pricing) for model, usage in data.get("models", {}).items()), 6)
        out["days"][day][job_id] = d
    return out

def main():
    parser = argparse.ArgumentParser(description="Track OpenClaw token usage")
    parser.add_argument("--yesterday", action="store_true", help="Report for yesterday only")
    parser.add_argument("--today", action="store_true", help="Report for today only")
    parser.add_argument("--week", action="store_true", help="Report for last 7 days")
    parser.add_argument("--all", action="store_true", help="Report all time")
    parser.add_argument("--by-model", action="store_true", help="Group by model")
    parser.add_argument("--by-cron", action="store_true", help="Group by cron job")
    parser.add_argument("--costs", action="store_true", help="Estimate costs")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    parser.add_argument("--sessions", nargs="*", help="Specific session files")
    parser.add_argument("--hours", type=float, help="Rolling window in hours")
    parser.add_argument("--days", type=int, help="Rolling window in calendar days")
    parser.add_argument("--since", help="Start time (ISO date/time or relative, e.g. 2h)")
    parser.add_argument("--until", help="End time (ISO date/time or relative, e.g. 1h)")
    parser.add_argument("--cache", action="store_true", help="Include cache columns in text output (shown by default)")
    parser.add_argument("--session-detail", action="store_true", help="Include per-session totals in text output")
    args = parser.parse_args()
    
    now = datetime.now(LOCAL_TZ)
    since = None
    until = None
    
    if args.hours is not None:
        since = (now - timedelta(hours=args.hours)).replace(tzinfo=None).isoformat(timespec="seconds")
    elif args.days is not None:
        since = (now - timedelta(days=args.days)).replace(tzinfo=None).isoformat(timespec="seconds")
    elif args.since:
        if args.since.endswith(("m", "h", "d")):
            amount = float(args.since[:-1])
            unit = args.since[-1]
            delta = timedelta(minutes=amount) if unit == "m" else timedelta(hours=amount) if unit == "h" else timedelta(days=amount)
            since = (now - delta).replace(tzinfo=None).isoformat(timespec="seconds")
        else:
            since = args.since
    elif args.today:
        since = now.strftime("%Y-%m-%dT00:00:00")
    elif args.yesterday:
        yesterday = now - timedelta(days=1)
        since = yesterday.strftime("%Y-%m-%dT00:00:00")
        until = now.strftime("%Y-%m-%dT00:00:00")
    elif args.week:
        since = (now - timedelta(days=7)).strftime("%Y-%m-%dT00:00:00")
    elif not args.all:
        args.today = True
        since = now.strftime("%Y-%m-%dT00:00:00")
    
    if args.until:
        if args.until.endswith(("m", "h", "d")):
            amount = float(args.until[:-1])
            unit = args.until[-1]
            delta = timedelta(minutes=amount) if unit == "m" else timedelta(hours=amount) if unit == "h" else timedelta(days=amount)
            until = (now - delta).replace(tzinfo=None).isoformat(timespec="seconds")
        else:
            until = args.until
    sessions = args.sessions or find_sessions(since=since)
    sqlite_sources = list(_sqlite_transcript_sources())
    if not sessions and not sqlite_sources:
        print("No session files found.")
        return

    # ── Version / backend detection ──────────────────────────────────────
    backend_info = detect_storage_backends()
    v_label = backend_info["version"] or "unknown"
    backend_label = backend_info["primary"]
    n_jsonl = len(backend_info["jsonl_sessions"])
    n_sqlite = len(backend_info["sqlite_dbs"])
    n_zst = len(backend_info["zst_archives"])

    pricing = load_pricing() if args.costs else None

    header_parts = [
        f"OpenClaw version : {v_label}",
        f"Storage backend  : {backend_label}"
        f"  (jsonl={n_jsonl}, sqlite={n_sqlite}, zst_archives={n_zst})",
    ]
    for w in backend_info["warnings"]:
        header_parts.append(f"⚠️  {w}")
    header = "\n".join(header_parts)

    # Merge SQLite transcripts only when SQLite is a live backend for this
    # install (9.x primary/mixed, or unknown-version with SQLite present).
    # On pre-9.x installs with a stale DB floating around, the classifier
    # already warned that it will be ignored — reading it anyway would
    # double-count sessions that also exist as JSONL.
    read_sqlite = bool(sqlite_sources) and backend_info["primary"] in ("sqlite", "mixed")
    # (day, model, in, out, cacheRead, cacheWrite) signatures of SQLite
    # contributions already merged — guards against double-counting a
    # session that exists in BOTH loose JSONL and the SQLite DB (transitional
    # installs) with identical per-day/model aggregates.
    seen_sqlite = set()

    def _merge_sqlite_bucket(tgt, u):
        tgt["input"] += u["input"]
        tgt["output"] += u["output"]
        tgt["messages"] += u["messages"]
        tgt["cacheRead"] += u.get("cacheRead", 0)
        tgt["cacheWrite"] += u.get("cacheWrite", 0)

    if args.by_cron:
        by_day_job = aggregate_by_cron(sessions, since=since, until=until)
        # Fold in the SQLite transcript backend (9.x storage migration) so cron
        # reports are not silently zero when every session file has rotated.
        if read_sqlite:
            sq_by_day, _ = aggregate_sqlite(since=since, until=until)
            for day, models in sq_by_day.items():
                for model, u in models.items():
                    # by_day_job is keyed 'day:job_id'; SQLite lacks cron tags, so
                    # attribute it to a synthetic 'sqlite-backend' bucket per day.
                    sig = (day, model or "unknown", u["input"], u["output"], u["cacheRead"], u["cacheWrite"])
                    if sig in seen_sqlite:
                        continue
                    seen_sqlite.add(sig)
                    key = f"{day}:sqlite-backend"
                    tgt = by_day_job[key]
                    _merge_sqlite_bucket(tgt, u)
                    if not tgt["name"]:
                        tgt["name"] = "(sqlite backend)"
        if args.json:
            cron_payload = to_cron_json(by_day_job, pricing)
            cron_payload["openclaw_version"] = v_label
            cron_payload["storage_backend"] = backend_label
            cron_payload["storage_counts"] = {
                "jsonl": n_jsonl, "sqlite": n_sqlite, "zst": n_zst
            }
            cron_payload["warnings"] = backend_info["warnings"]
            print(json.dumps(cron_payload, indent=2))
        else:
            print(header)
            print(format_cron_report(by_day_job, pricing, args.costs))
    else:
        by_day, by_session = aggregate(sessions, since=since, until=until)
        # Merge the SQLite transcript backend (9.x storage migration): ended
        # sessions live in openclaw-agent.sqlite, not as loose .jsonl files, so
        # without this a full-day report is silently zero once sessions close.
        if read_sqlite:
            sq_by_day, _ = aggregate_sqlite(since=since, until=until)
            for day, models in sq_by_day.items():
                for model, u in models.items():
                    sig = (day, model or "unknown", u["input"], u["output"], u["cacheRead"], u["cacheWrite"])
                    if sig in seen_sqlite:
                        continue
                    seen_sqlite.add(sig)
                    d = by_day[day][model or "unknown"]
                    d["input"] += u["input"]
                    d["output"] += u["output"]
                    d["cacheRead"] += u["cacheRead"]
                    d["cacheWrite"] += u["cacheWrite"]
                    d["messages"] += u["messages"]
        if args.json:
            payload = to_json(by_day, by_session, pricing)
            payload["openclaw_version"] = v_label
            payload["storage_backend"] = backend_label
            payload["storage_counts"] = {
                "jsonl": n_jsonl, "sqlite": n_sqlite, "zst": n_zst
            }
            payload["warnings"] = backend_info["warnings"]
            print(json.dumps(payload, indent=2))
        else:
            print(header)
            print(format_report(by_day, by_session, pricing, args.costs))
            if args.session_detail:
                print("\n## Sessions")
                for session_id, data in sorted(by_session.items()):
                    models = ", ".join(sorted(data["models"]))
                    print(f"  {session_id}: in={data['input']:,} out={data['output']:,} cache={data['cacheRead']:,} models={models}")

if __name__ == "__main__":
    main()
