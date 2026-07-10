#!/usr/bin/env python3
"""
Handler for /save Telegram commands.
Normalizes /save <subcmd> [args] into bookmark.py calls.

Usage:
    handler.py save-reply "<message_text>" [--message-id <id>] [--tags "..."] [--note "..."]
    handler.py save-inline "<text>" [--tags "..."] [--note "..."]
    handler.py list [--count N]
    handler.py search "<query>"
    handler.py count
    handler.py tags
    handler.py help
    handler.py show <id>
    handler.py rm <id>
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path

BOOKMARK_PY = Path(__file__).parent.parent.parent.parent / "scripts" / "bookmark.py"

def run_bookmark(*args):
    """Run bookmark.py with given args and return (stdout, stderr, rc)."""
    cmd = [sys.executable, str(BOOKMARK_PY)] + list(args)
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout, result.stderr, result.returncode


def cmd_save_reply(args):
    """Save a replied-to message."""
    # Use full content if provided (from session history), otherwise use the fallback message text
    content = args.full_content if args.full_content else args.message

    bargs = ["save", "--content", content]
    if args.tags:
        bargs += ["--tags", args.tags]
    if args.note:
        bargs += ["--note", args.note]
    if args.source:
        bargs += ["--source", args.source]
    stdout, stderr, rc = run_bookmark(*bargs)
    if rc != 0:
        print(f"Error: {stderr or stdout}", file=sys.stderr)
        return 1
    print(stdout.strip())
    return 0


def cmd_save_inline(args):
    """Save inline text."""
    return cmd_save_reply(args)  # Same logic, just different calling context


def cmd_list(args):
    """List recent bookmarks."""
    bargs = ["list"]
    if args.count:
        bargs += ["--count", str(args.count)]
    stdout, stderr, rc = run_bookmark(*bargs)
    if rc != 0:
        print(f"Error: {stderr or stdout}", file=sys.stderr)
        return 1
    print(stdout.strip() or "No bookmarks yet.")
    return 0


def cmd_search(args):
    """Search bookmarks."""
    stdout, stderr, rc = run_bookmark("search", args.query)
    if rc != 0:
        print(f"Error: {stderr or stdout}", file=sys.stderr)
        return 1
    print(stdout.strip() or f"No results for '{args.query}'.")
    return 0


def cmd_count(_args):
    """Count total bookmarks."""
    stdout, stderr, rc = run_bookmark("json")
    if rc != 0:
        print(f"Error: {stderr or stdout}", file=sys.stderr)
        return 1
    try:
        entries = json.loads(stdout)
        print(f"Total bookmarks: {len(entries)}")
    except json.JSONDecodeError:
        print("0")
    return 0


def cmd_tags(_args):
    """List all unique tags."""
    stdout, stderr, rc = run_bookmark("json")
    if rc != 0:
        print(f"Error: {stderr or stdout}", file=sys.stderr)
        return 1
    try:
        entries = json.loads(stdout)
        tags = set()
        for e in entries:
            if e.get("tags") and e["tags"] != "(none)":
                tags.update(t.strip() for t in e["tags"].split(","))
        if tags:
            print("Tags: " + ", ".join(sorted(tags)))
        else:
            print("No tags yet.")
    except json.JSONDecodeError:
        print("No bookmarks yet.")
    return 0


def cmd_help(_args):
    """Show usage help."""
    print(
        "Bookmark commands:\n"
        "  /save (reply)      — save replied-to message\n"
        "  /save <text>       — save inline text\n"
        "  /save list [N]     — list recent bookmarks (default 10)\n"
        "  /save search <q>   — search by keyword or #tag\n"
        "  /save show <#>     — show specific bookmark\n"
        "  /save rm <#>       — remove a bookmark\n"
        "  /save count        — total count\n"
        "  /save tags         — list all tags\n"
        "  /save help         — show this help"
    )
    return 0


def cmd_show(args):
    """Show a specific bookmark."""
    stdout, stderr, rc = run_bookmark("show", str(args.id))
    if rc != 0:
        print(f"Error: {stderr or stdout}", file=sys.stderr)
        return 1
    print(stdout.strip())
    return 0


def cmd_rm(args):
    """Remove a bookmark."""
    stdout, stderr, rc = run_bookmark("rm", str(args.id))
    if rc != 0:
        print(f"Error: {stderr or stdout}", file=sys.stderr)
        return 1
    print(stdout.strip())
    return 0


def main():
    parser = argparse.ArgumentParser(description="Bookmark command handler")
    sub = parser.add_subparsers(dest="command", required=True)

    # save-reply
    p_reply = sub.add_parser("save-reply", help="Save a replied-to message")
    p_reply.add_argument("message", help="Message text to save (fallback if full-content not provided)")
    p_reply.add_argument("--full-content", default="", help="Full message text from session history (overrides message)")
    p_reply.add_argument("--tags", default="", help="Comma-separated tags")
    p_reply.add_argument("--note", default="", help="User note")
    p_reply.add_argument("--source", default="telegram:main", help="Source")

    # save-inline
    p_inline = sub.add_parser("save-inline", help="Save inline text")
    p_inline.add_argument("message", help="Text to save")
    p_inline.add_argument("--tags", default="", help="Comma-separated tags")
    p_inline.add_argument("--note", default="", help="User note")

    # list
    p_list = sub.add_parser("list", help="List bookmarks")
    p_list.add_argument("--count", type=int, default=10, help="Number to show")

    # search
    p_search = sub.add_parser("search", help="Search bookmarks")
    p_search.add_argument("query", help="Search query")

    # count
    sub.add_parser("count", help="Count bookmarks")

    # tags
    sub.add_parser("tags", help="List all tags")

    # help
    sub.add_parser("help", help="Show usage help")

    # show
    p_show = sub.add_parser("show", help="Show a specific bookmark")
    p_show.add_argument("id", type=int, help="Bookmark ID")

    # rm
    p_rm = sub.add_parser("rm", help="Remove a bookmark")
    p_rm.add_argument("id", type=int, help="Bookmark ID")

    args = parser.parse_args()

    commands = {
        "save-reply": cmd_save_reply,
        "save-inline": cmd_save_inline,
        "list": cmd_list,
        "search": cmd_search,
        "count": cmd_count,
        "tags": cmd_tags,
        "help": cmd_help,
        "show": cmd_show,
        "rm": cmd_rm,
    }
    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
