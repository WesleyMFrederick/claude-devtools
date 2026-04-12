#!/usr/bin/env python3
"""
nba-format-promote.py — Apply gold standard formatting to answered NBA table rows.

Deterministic script: parses NBA table rows from a whiteboard markdown file,
applies strikethrough/bold/linked-anchor formatting to rows whose Status cell
contains an "answered" keyword, and validates that every #^TAG link has a
corresponding ^TAG block anchor in the file body.

Usage:
    python3 nba-format-promote.py <whiteboard.md> [--dry-run] [--json]

Exit codes:
    0 — all rows formatted correctly (or fixes applied successfully)
    1 — missing block anchors detected (printed to stderr)
    2 — file not found or parse error
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Status keywords that indicate a row is "answered" (case-insensitive)
ANSWERED_KEYWORDS = {"answered", "confirmed", "resolved"}

# Evidence tag pattern: OBS-NNN, D-NNN, Q-NNN, F-LK-NNN, F-ID-NNN, etc.
TAG_RE = re.compile(r"\b([A-Z][A-Z]*(?:-[A-Z]+)?)-(\d{3})\b")

# Already-linked tag pattern: [TAG-NNN](#^TAG-NNN)
LINKED_TAG_RE = re.compile(r"\[([A-Z][A-Z]*(?:-[A-Z]+)?-\d{3})\]\(#\^\1\)")

# Block anchor pattern in file body: ^TAG-NNN
BLOCK_ANCHOR_RE = re.compile(r"\^([A-Z][A-Z]*(?:-[A-Z]+)?-\d{3})\b")

# Table row pattern (starts with |)
TABLE_ROW_RE = re.compile(r"^\s*\|")

# Separator row pattern (| --- | --- | ...)
SEPARATOR_RE = re.compile(r"^\s*\|[\s\-:|]+\|[\s\-:|]+\|")

# Header row detection: | # | Item | ... | Status |
HEADER_RE = re.compile(r"^\s*\|\s*#\s*\|.*Status\s*\|", re.IGNORECASE)


@dataclass
class NBARow:
    """Parsed NBA table row."""
    line_number: int
    original: str
    cells: list  # [#, Item, Utility, Cost, DRI, Status]
    is_answered: bool = False
    is_gold_standard: bool = False


@dataclass
class FormatResult:
    """Result of formatting a single row."""
    line_number: int
    original: str
    formatted: str
    changed: bool
    issues: list = field(default_factory=list)


@dataclass
class ValidationResult:
    """Result of block anchor validation."""
    tag: str
    line_number: int
    has_anchor: bool


def parse_table_row(line: str) -> list:
    """Split a markdown table row into cells, stripping outer pipes."""
    if not line.strip().startswith("|"):
        return []
    # Remove leading/trailing pipe and split
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_answered(status_cell: str) -> bool:
    """Check if a status cell indicates the row is answered."""
    # Strip markdown formatting for keyword check
    clean = re.sub(r"[*~\[\]()#^]", "", status_cell).strip().lower()
    for keyword in ANSWERED_KEYWORDS:
        if keyword in clean:
            return True
    return False


def has_strikethrough(cell: str) -> bool:
    """Check if a cell is wrapped in ~~strikethrough~~."""
    stripped = cell.strip()
    return stripped.startswith("~~") and stripped.endswith("~~")


def has_bold_status(status_cell: str) -> bool:
    """Check if the status keyword is bolded."""
    for keyword in ANSWERED_KEYWORDS:
        if f"**{keyword.capitalize()}**" in status_cell or f"**{keyword.upper()}**" in status_cell:
            return True
    return False


def link_tags_in_status(status_cell: str) -> str:
    """Convert plain-text TAG-NNN references to [TAG-NNN](#^TAG-NNN) links."""
    result = status_cell

    # Find all TAG-NNN references that are NOT already linked
    def replace_unlinked(match):
        full_tag = match.group(0)
        # Check if this match is already inside a link [TAG](#^TAG)
        start = match.start()
        # Look backwards for [ that would indicate we're inside a link
        prefix = result[:start]
        # If the character before is [ or the tag appears in an existing link context, skip
        if prefix.endswith("[") or prefix.endswith("^"):
            return full_tag
        return f"[{full_tag}](#^{full_tag})"

    # First, find positions of already-linked tags to avoid double-linking
    linked_positions = set()
    for m in LINKED_TAG_RE.finditer(result):
        linked_positions.add((m.start(), m.end()))

    # Replace unlinked tags
    new_result = []
    last_end = 0
    for m in TAG_RE.finditer(result):
        tag = m.group(0)
        # Check if this position overlaps with any linked tag
        is_linked = False
        for ls, le in linked_positions:
            if ls <= m.start() < le:
                is_linked = True
                break
        if is_linked:
            new_result.append(result[last_end:m.end()])
        else:
            new_result.append(result[last_end:m.start()])
            new_result.append(f"[{tag}](#^{tag})")
        last_end = m.end()
    new_result.append(result[last_end:])

    return "".join(new_result)


def apply_strikethrough(cell: str) -> str:
    """Wrap cell content in ~~strikethrough~~ if not already wrapped."""
    stripped = cell.strip()
    if not stripped:
        return cell
    if has_strikethrough(cell):
        return cell
    return f"~~{stripped}~~"


def bold_status_keyword(status_cell: str) -> str:
    """Bold the status keyword if not already bolded."""
    result = status_cell
    for keyword in ANSWERED_KEYWORDS:
        # Case-insensitive search for the keyword without bold
        pattern = re.compile(rf"(?<!\*\*){re.escape(keyword)}(?!\*\*)", re.IGNORECASE)
        match = pattern.search(result)
        if match:
            # Check it's not already inside **...**
            before = result[:match.start()]
            if not before.rstrip().endswith("**"):
                capitalized = match.group(0).capitalize()
                result = result[:match.start()] + f"**{capitalized}**" + result[match.end():]
                break
    return result


def format_answered_row(cells: list) -> list:
    """Apply gold standard formatting to an answered row's cells.

    Expected cells: [#, Item, Utility, Cost, DRI, Status]
    """
    if len(cells) < 6:
        return cells

    formatted = list(cells)

    # Pad the # cell for visual alignment (3 chars min)
    num = formatted[0].strip()
    formatted[0] = f"{num:<3}"

    # Apply strikethrough to Item, Utility, Cost, DRI (indices 1-4)
    for i in range(1, 5):
        formatted[i] = apply_strikethrough(formatted[i])

    # Bold the status keyword
    formatted[5] = bold_status_keyword(formatted[5])

    # Link evidence tags in status cell
    formatted[5] = link_tags_in_status(formatted[5])

    return formatted


def is_gold_standard(cells: list) -> bool:
    """Check if an answered row already meets all gold standard criteria."""
    if len(cells) < 6:
        return False

    # Check strikethrough on Item, Utility, Cost, DRI (indices 1-4)
    for i in range(1, 5):
        if not has_strikethrough(cells[i]):
            return False

    # Check bold status keyword
    if not has_bold_status(cells[5]):
        return False

    # Check all TAG-NNN refs in status are linked
    status = cells[5]
    for m in TAG_RE.finditer(status):
        tag = m.group(0)
        # Check this tag is part of a [TAG](#^TAG) link
        linked_pattern = re.compile(re.escape(f"[{tag}](#^{tag})"))
        if not linked_pattern.search(status):
            return False

    return True


def rebuild_row(cells: list) -> str:
    """Rebuild a markdown table row from cells with padding."""
    padded = [f" {cell.strip()} " for cell in cells]
    return "|" + "|".join(padded) + " |"


def find_block_anchors(content: str) -> set:
    """Find all ^TAG-NNN block anchors in the file."""
    return set(BLOCK_ANCHOR_RE.findall(content))


def find_linked_tags_in_nba(content: str, nba_start: int, nba_end: int) -> list:
    """Find all TAG-NNN references in NBA table rows that need block anchors."""
    tags = []
    lines = content.split("\n")
    for i in range(nba_start, min(nba_end, len(lines))):
        line = lines[i]
        if not TABLE_ROW_RE.match(line) or SEPARATOR_RE.match(line) or HEADER_RE.match(line):
            continue
        # Find all tag references (both linked and plain)
        for m in TAG_RE.finditer(line):
            tag = m.group(0)
            tags.append(ValidationResult(tag=tag, line_number=i + 1, has_anchor=False))
    return tags


def find_nba_section(lines: list) -> tuple:
    """Find the start and end line indices of the NBA section."""
    start = None
    for i, line in enumerate(lines):
        if "Next Best Actions" in line and line.strip().startswith("#"):
            start = i
            break

    if start is None:
        return None, None

    # Find end: next H2 section or end of file
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].strip().startswith("## ") and "Tier" not in lines[i]:
            end = i
            break

    return start, end


def process_file(filepath: str, dry_run: bool = False, json_output: bool = False) -> int:
    """Main processing: parse, format, validate, write."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: File not found: {filepath}", file=sys.stderr)
        return 2

    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")

    nba_start, nba_end = find_nba_section(lines)
    if nba_start is None:
        print("Error: No 'Next Best Actions' section found", file=sys.stderr)
        return 2

    # Parse and format NBA rows
    results = []
    modified_lines = list(lines)

    for i in range(nba_start, nba_end):
        line = lines[i]

        # Skip non-table, separator, and header rows
        if not TABLE_ROW_RE.match(line) or SEPARATOR_RE.match(line) or HEADER_RE.match(line):
            continue

        cells = parse_table_row(line)
        if len(cells) < 6:
            continue

        status_cell = cells[5]
        if not is_answered(status_cell):
            continue

        # Skip rows that already meet gold standard (preserve existing whitespace)
        if is_gold_standard(cells):
            results.append(FormatResult(
                line_number=i + 1,
                original=line,
                formatted=line,
                changed=False,
            ))
            continue

        # Apply formatting
        formatted_cells = format_answered_row(cells)
        formatted_line = rebuild_row(formatted_cells)

        changed = formatted_line.strip() != line.strip()
        result = FormatResult(
            line_number=i + 1,
            original=line,
            formatted=formatted_line,
            changed=changed,
        )
        results.append(result)

        if changed:
            modified_lines[i] = formatted_line

    # Validate block anchors
    existing_anchors = find_block_anchors(content)
    tag_refs = find_linked_tags_in_nba(content, nba_start, nba_end)
    missing_anchors = []
    for ref in tag_refs:
        ref.has_anchor = ref.tag in existing_anchors
        if not ref.has_anchor:
            missing_anchors.append(ref)

    # Output
    if json_output:
        output = {
            "file": str(path),
            "nba_section": {"start": nba_start + 1, "end": nba_end},
            "rows_processed": len(results),
            "rows_changed": sum(1 for r in results if r.changed),
            "changes": [
                {
                    "line": r.line_number,
                    "before": r.original.strip(),
                    "after": r.formatted.strip(),
                    "changed": r.changed,
                }
                for r in results
            ],
            "missing_anchors": [
                {"tag": m.tag, "line": m.line_number}
                for m in missing_anchors
            ],
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable diff output
        changes_made = sum(1 for r in results if r.changed)
        if changes_made == 0:
            print(f"✓ All {len(results)} answered rows match gold standard format")
        else:
            print(f"Found {changes_made} row(s) needing formatting fixes:\n")
            for r in results:
                if r.changed:
                    print(f"  Line {r.line_number}:")
                    print(f"    BEFORE: {r.original.strip()}")
                    print(f"    AFTER:  {r.formatted.strip()}")
                    print()

        if missing_anchors:
            print(f"\n⚠ Missing block anchors ({len(missing_anchors)}):", file=sys.stderr)
            for m in missing_anchors:
                print(f"  Line {m.line_number}: ^{m.tag} not found in file body", file=sys.stderr)

    # Write changes unless dry-run
    if not dry_run and any(r.changed for r in results):
        new_content = "\n".join(modified_lines)
        path.write_text(new_content, encoding="utf-8")
        if not json_output:
            print(f"\n✓ Wrote {changes_made} fix(es) to {path}")

    # Return code
    if missing_anchors:
        return 1
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Apply gold standard formatting to answered NBA table rows"
    )
    parser.add_argument("file", help="Path to whiteboard markdown file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without writing to file",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    args = parser.parse_args()

    sys.exit(process_file(args.file, dry_run=args.dry_run, json_output=args.json))


if __name__ == "__main__":
    main()
