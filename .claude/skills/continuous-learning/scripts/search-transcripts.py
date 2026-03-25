#!/usr/bin/env python3
"""
Search claude-code transcript JSONL files for specific content.

MODES
-----
Search (default):
    python3 ~/.claude/scripts/search-transcripts.py "search term"
    python3 ~/.claude/scripts/search-transcripts.py "LBNL story" --project ResumeCoach

Segment extraction (find range between two anchors):
    python3 ~/.claude/scripts/search-transcripts.py --from "resume tailoring" --to "Glenn"
    python3 ~/.claude/scripts/search-transcripts.py --from "resume tailoring" --to "Glenn" --full

FLAGS
-----
--project/-p    Filter by project name substring (default: ResumeCoach)
--all/-a        Search all projects
--dir/-d        Search JSONL files in a custom directory (bypasses ~/.claude/projects)
--full          In segment mode, print full message text (default: first 300 chars)
"""

import argparse
import json
import sys
from pathlib import Path

PROJECTS_DIR = Path.home() / ".claude/projects"


def find_project_dir(project_hint: str | None) -> list[Path]:
    all_dirs = [d for d in PROJECTS_DIR.iterdir() if d.is_dir()]
    if not project_hint:
        return all_dirs
    hint_lower = project_hint.lower()
    matches = [d for d in all_dirs if hint_lower in d.name.lower()]
    if not matches:
        print(f"No project matching '{project_hint}'. Available:")
        for d in sorted(all_dirs):
            print(f"  {d.name}")
        sys.exit(1)
    return matches


def extract_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for item in content:
            if isinstance(item, dict):
                if item.get("type") == "text":
                    texts.append(item.get("text", ""))
                elif item.get("type") == "tool_result":
                    for c in item.get("content", []):
                        if isinstance(c, dict) and c.get("type") == "text":
                            texts.append(c.get("text", ""))
        return " ".join(texts)
    return ""


def load_messages(jsonl_path: Path) -> list[dict]:
    """Load all messages from a JSONL file as list of {line, role, text}."""
    messages = []
    try:
        with open(jsonl_path, encoding="utf-8", errors="replace") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                msg = record.get("message", {})
                text = extract_text(msg.get("content", ""))
                messages.append({
                    "line": line_num,
                    "role": msg.get("role", "unknown"),
                    "text": text,
                })
    except Exception as e:
        print(f"  [error reading {jsonl_path.name}]: {e}")
    return messages


def search_file(jsonl_path: Path, term: str) -> list[dict]:
    """Search a single JSONL file for a term. Returns list of hit dicts."""
    hits = []
    for msg in load_messages(jsonl_path):
        text = msg["text"]
        term_lower = term.lower()
        if term_lower in text.lower():
            idx = text.lower().find(term_lower)
            start = max(0, idx - 120)
            end = min(len(text), idx + 300)
            snippet = text[start:end].replace("\n", " ").strip()
            hits.append({
                "line": msg["line"],
                "role": msg["role"],
                "snippet": f"...{snippet}...",
            })
    return hits


def segment_file(jsonl_path: Path, from_term: str, to_term: str, full: bool = False) -> list[dict] | None:
    """
    Find the segment between first occurrence of from_term and last occurrence of to_term.
    Returns the messages in that range, or None if either anchor not found.
    """
    messages = load_messages(jsonl_path)
    from_lower = from_term.lower()
    to_lower = to_term.lower()

    # Find first line matching from_term
    start_idx = None
    for i, msg in enumerate(messages):
        if from_lower in msg["text"].lower():
            start_idx = i
            break

    if start_idx is None:
        return None

    # Find last line matching to_term (at or after start_idx)
    end_idx = None
    for i in range(len(messages) - 1, start_idx - 1, -1):
        if to_lower in messages[i]["text"].lower():
            end_idx = i
            break

    if end_idx is None:
        return None

    return messages[start_idx:end_idx + 1]


def main():
    parser = argparse.ArgumentParser(description="Search Claude Code transcript JSONL files.")
    parser.add_argument("term", nargs="?", help="Search term (case-insensitive)")
    parser.add_argument("--from", dest="from_term", help="Segment mode: start anchor term")
    parser.add_argument("--to", dest="to_term", help="Segment mode: end anchor term")
    parser.add_argument("--project", "-p", help="Filter by project name substring")
    parser.add_argument("--all", "-a", action="store_true", help="Search all projects (default: ResumeCoach)")
    parser.add_argument("--full", action="store_true", help="In segment mode, print full message text")
    parser.add_argument("--dir", "-d", help="Search JSONL files in a custom directory instead of ~/.claude/projects")
    args = parser.parse_args()

    # Validate mode
    segment_mode = bool(args.from_term or args.to_term)
    if segment_mode and not (args.from_term and args.to_term):
        parser.error("--from and --to must both be provided for segment extraction")
    if not segment_mode and not args.term:
        parser.error("Provide a search term, or use --from / --to for segment extraction")

    # Resolve JSONL files
    if args.dir:
        custom_path = Path(args.dir).expanduser().resolve()
        if custom_path.is_file() and custom_path.suffix == ".jsonl":
            jsonl_files = [custom_path]
            project_dirs = [custom_path.parent]
        elif custom_path.is_dir():
            jsonl_files = sorted(custom_path.glob("*.jsonl"))
            project_dirs = [custom_path]
        else:
            print(f"Not a valid file or directory: {custom_path}")
            sys.exit(1)
    else:
        if args.all:
            project_dirs = find_project_dir(None)
        elif args.project:
            project_dirs = find_project_dir(args.project)
        else:
            project_dirs = find_project_dir("ResumeCoach")
        jsonl_files = []
        for d in project_dirs:
            jsonl_files.extend(sorted(d.glob("*.jsonl")))

    # --- SEGMENT MODE ---
    if segment_mode:
        print(f"Segment mode: from='{args.from_term}' → to='{args.to_term}'")
        print(f"Searching {len(jsonl_files)} file(s)\n")
        found_any = False
        for jsonl_path in jsonl_files:
            segment = segment_file(jsonl_path, args.from_term, args.to_term, args.full)
            if segment:
                found_any = True
                print(f"{'='*60}")
                print(f"FILE: {jsonl_path.name}")
                print(f"Lines {segment[0]['line']}–{segment[-1]['line']} ({len(segment)} messages)")
                print(f"{'='*60}")
                for msg in segment:
                    preview = msg["text"] if args.full else msg["text"][:300].replace("\n", " ").strip()
                    if not args.full and len(msg["text"]) > 300:
                        preview += "..."
                    print(f"  [Line {msg['line']}] [{msg['role'].upper()}]")
                    print(f"  {preview}")
                    print()
        if not found_any:
            print("No segment found matching both anchors.")
        return

    # --- SEARCH MODE ---
    print(f"Searching {len(jsonl_files)} JSONL file(s) across {len(project_dirs)} project(s)")
    print(f"Term: '{args.term}'\n")

    total_hits = 0
    for jsonl_path in jsonl_files:
        hits = search_file(jsonl_path, args.term)
        if hits:
            total_hits += len(hits)
            print(f"{'='*60}")
            print(f"FILE: {jsonl_path.name}")
            print(f"{'='*60}")
            for h in hits:
                print(f"  [Line {h['line']}] [{h['role'].upper()}]")
                print(f"  {h['snippet']}")
                print()

    print(f"Total hits: {total_hits}")


if __name__ == "__main__":
    main()
