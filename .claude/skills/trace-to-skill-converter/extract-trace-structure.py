#!/usr/bin/env python3
"""
Deterministic trace structure extractor.

Parses a trace markdown file and outputs structured JSON with all
mechanically-extractable data. No LLM involvement.

Usage:
    python3 extract-trace-structure.py <trace-file-path>

Output: JSON to stdout with keys:
    title, artifacts, steps, phases, process_tree, steering_events,
    learnings, fact_derivations, complexity
"""

import json
import re
import sys
from pathlib import Path


def extract_title(lines: list[str]) -> str:
    """Extract trace title from first H1."""
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    return ""


def extract_artifacts(text: str) -> list[dict]:
    """Parse the Artifacts markdown table."""
    artifacts = []
    in_table = False
    header_seen = False
    for line in text.splitlines():
        if "## Artifacts" in line:
            in_table = True
            continue
        if in_table:
            if line.startswith("|") and "---" in line:
                header_seen = True
                continue
            if line.startswith("|") and header_seen:
                cols = [c.strip() for c in line.split("|")[1:-1]]
                if len(cols) >= 3:
                    artifacts.append({
                        "artifact": cols[0],
                        "path": cols[1].strip("`"),
                        "role": cols[2],
                    })
            elif header_seen and not line.startswith("|"):
                break
    return artifacts


def extract_steps(text: str) -> list[dict]:
    """Extract numbered trace steps with evidence tags and phase context."""
    steps = []
    current_phase = ""
    # Match lines like: " 1. [OBS: ..." or "10. [OBS: ..." inside code fences
    step_re = re.compile(
        r"^\s*(\d+[a-z]?)\.\s+\[([A-Z][-A-Z]*?):\s*([^\]]*)\]"
    )
    # Match both "PHASE 1: ..." (inside code fences) and "## PHASE 1: ..." (markdown headings)
    phase_re = re.compile(r"^(?:#*\s*)?PHASE\s+(\S+):\s*(.*)", re.IGNORECASE)
    boundary_markers = ["CALL ──→", "RETURN ←──", "CALL ──", "RETURN ←",
                        "→ CLI", "← CLI", "HOOK →", "→ HOOK"]
    steering_re = re.compile(r"⚠\s*USER STEERING")
    substep_re = re.compile(r"^\s*(\d+[a-z])\.\s+\[")

    # Regex for start of a step (may or may not close ] on same line)
    step_start_re = re.compile(
        r"^\s*(\d+[a-z]?)\.\s+\[([A-Z][-A-Z]*?):\s*(.*)"
    )

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        # Track phase headers
        pm = phase_re.match(line)
        if pm:
            current_phase = f"PHASE {pm.group(1)}: {pm.group(2).strip()}"

        # Match numbered steps (handle multi-line evidence tags)
        sm = step_start_re.match(line)
        if sm:
            step_num = sm.group(1)
            tag_type = sm.group(2)
            rest = sm.group(3)

            # Check if tag closes on this line
            if "]" in rest:
                source_ref = rest[:rest.index("]")].strip()
            else:
                # Tag spans multiple lines — collect until we find the closing ]
                tag_lines = [rest]
                k = i + 1
                while k < len(lines):
                    if "]" in lines[k]:
                        tag_lines.append(lines[k][:lines[k].index("]")])
                        i = k  # advance past the multi-line tag
                        break
                    tag_lines.append(lines[k])
                    k += 1
                source_ref = " ".join(
                    l.strip() for l in tag_lines
                ).strip()

            # Collect body lines until next step or section
            body_lines = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                # Stop at next numbered step, phase header, steering event, or section boundary
                if step_start_re.match(next_line) or phase_re.match(next_line):
                    break
                if steering_re.search(next_line):
                    break
                if next_line.startswith("══") or next_line.startswith("END TRACE"):
                    break
                body_lines.append(next_line)
                j += 1

            body = "\n".join(body_lines).strip()

            # Check for boundary crossings in body
            has_boundary = any(marker in body for marker in boundary_markers)

            # Check for sub-steps
            has_substeps = bool(substep_re.search(body))

            # Check for KEY LINE annotation
            is_key_line = "← KEY LINE" in line or "← KEY LINE" in body

            steps.append({
                "step_number": step_num,
                "tag_type": tag_type,
                "source_ref": source_ref,
                "phase": current_phase,
                "has_boundary_crossing": has_boundary,
                "has_substeps": has_substeps,
                "is_key_line": is_key_line,
                "body_preview": body[:200] if body else "",
            })

        i += 1

    return steps


def extract_phases(text: str) -> list[str]:
    """Extract phase headers."""
    phases = []
    for line in text.splitlines():
        m = re.match(r"^(?:#*\s*)?PHASE\s+(\S+):\s*(.*)", line, re.IGNORECASE)
        if m:
            phases.append(f"PHASE {m.group(1)}: {m.group(2).strip()}")
    return phases


def extract_process_tree(text: str) -> dict:
    """Extract process tree sections if present."""
    result = {"canonical": None, "visual_tree": None, "activity_legend": []}

    # Find ## Process Tree section
    lines = text.splitlines()
    in_pt = False
    in_canonical = False
    in_visual = False
    in_legend = False
    in_code_fence = False
    canonical_lines = []
    visual_lines = []
    legend_header_seen = False

    for i, line in enumerate(lines):
        if line.startswith("## Process Tree"):
            in_pt = True
            continue
        if in_pt and line.startswith("## ") and "Process Tree" not in line:
            break

        if in_pt:
            if line.startswith("### Canonical"):
                in_canonical = True
                in_visual = False
                in_legend = False
                in_code_fence = False
                continue
            if line.startswith("### Visual"):
                in_canonical = False
                in_visual = True
                in_legend = False
                in_code_fence = False
                continue
            if line.startswith("### Activity Legend"):
                in_canonical = False
                in_visual = False
                in_legend = True
                in_code_fence = False
                continue

            if line.strip().startswith("```"):
                in_code_fence = not in_code_fence
                continue

            if in_canonical and in_code_fence:
                canonical_lines.append(line)
            if in_visual and in_code_fence:
                visual_lines.append(line)

            if in_legend:
                if line.startswith("|") and "---" in line:
                    legend_header_seen = True
                    continue
                if line.startswith("|") and legend_header_seen:
                    cols = [c.strip() for c in line.split("|")[1:-1]]
                    if len(cols) >= 5:
                        result["activity_legend"].append({
                            "node": cols[0],
                            "actor": cols[1],
                            "activity": cols[2],
                            "tool_calls": cols[3],
                            "trace_evidence": cols[4],
                        })
                    elif len(cols) >= 3:
                        result["activity_legend"].append({
                            "node": cols[0],
                            "activity": cols[1],
                            "trace_evidence": cols[2],
                        })

    if canonical_lines:
        result["canonical"] = "\n".join(canonical_lines).strip()
    if visual_lines:
        result["visual_tree"] = "\n".join(visual_lines).strip()

    return result


def extract_steering_events(text: str) -> list[dict]:
    """Extract user steering events (╔═══ boxes and ⚠ USER STEERING headers)."""
    events = []
    lines = text.splitlines()
    steering_re = re.compile(r"⚠\s*USER STEERING\s*#?(\d+)?")

    for i, line in enumerate(lines):
        m = steering_re.search(line)
        if m:
            event_num = m.group(1) or str(len(events) + 1)
            # Collect context: source ref from the header line
            source_ref = ""
            ref_m = re.search(r"\(([^)]+)\)", line)
            if ref_m:
                source_ref = ref_m.group(1)

            # Look for the ╔═══ box content below
            box_lines = []
            for j in range(i + 1, min(i + 20, len(lines))):
                if "╔═" in lines[j]:
                    # Start collecting box content
                    for k in range(j + 1, min(j + 15, len(lines))):
                        if "╚═" in lines[k]:
                            break
                        box_lines.append(
                            lines[k].strip().lstrip("║").strip()
                        )
                    break

            events.append({
                "number": event_num,
                "source_ref": source_ref,
                "description": " ".join(box_lines) if box_lines else "",
            })

    return events


def extract_learnings(text: str) -> list[dict]:
    """Extract ## Learnings section entries."""
    learnings = []
    lines = text.splitlines()
    in_learnings = False
    learning_re = re.compile(r"^\*\*([^*]+)\*\*:?\s*(.*)")

    for i, line in enumerate(lines):
        if line.startswith("## Learnings"):
            in_learnings = True
            continue
        if in_learnings and line.startswith("## "):
            break
        if in_learnings:
            m = learning_re.match(line.strip())
            if m:
                learnings.append({
                    "id": m.group(1).strip(),
                    "body": m.group(2).strip(),
                })

    return learnings


def extract_fact_derivations(text: str) -> list[dict]:
    """Extract fact derivation entries (F-LK, F-ID tags with step refs)."""
    facts = []
    fact_re = re.compile(
        r"\*\*\[(F-(?:LK|ID|INF)):\s*(?:from\s+)?([^\]]*)\]\*\*\s*(.*)"
    )
    for line in text.splitlines():
        m = fact_re.search(line)
        if m:
            facts.append({
                "tag_type": m.group(1),
                "step_refs": m.group(2).strip(),
                "description": m.group(3).strip(),
            })
    return facts


def measure_complexity(steps, phases, steering_events) -> dict:
    """Compute complexity metrics."""
    boundary_count = sum(1 for s in steps if s["has_boundary_crossing"])
    return {
        "total_steps": len(steps),
        "phase_count": len(phases),
        "boundary_crossing_count": boundary_count,
        "steering_event_count": len(steering_events),
        "substep_count": sum(1 for s in steps if s["has_substeps"]),
        "key_line_count": sum(1 for s in steps if s["is_key_line"]),
    }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 extract-trace-structure.py <trace-file>",
              file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1]).resolve()
    if not path.exists():
        print(f"Error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    title = extract_title(lines)
    artifacts = extract_artifacts(text)
    steps = extract_steps(text)
    phases = extract_phases(text)
    process_tree = extract_process_tree(text)
    steering_events = extract_steering_events(text)
    learnings = extract_learnings(text)
    fact_derivations = extract_fact_derivations(text)
    complexity = measure_complexity(steps, phases, steering_events)

    result = {
        "source_file": str(path),
        "title": title,
        "artifacts": artifacts,
        "steps": steps,
        "phases": phases,
        "process_tree": process_tree,
        "steering_events": steering_events,
        "learnings": learnings,
        "fact_derivations": fact_derivations,
        "complexity": complexity,
        "has_process_tree": process_tree["canonical"] is not None,
        "has_activity_legend": len(process_tree["activity_legend"]) > 0,
    }

    json.dump(result, sys.stdout, indent=2)
    print()


if __name__ == "__main__":
    main()
