#!/usr/bin/env python3
"""
Deterministic validator for short-form-script-writer-pro outputs.

Checks every item on the skill's validation checklist across all complexity-based
duration tiers (30s, 45s, 60s, 75s, 90s, 120s, and custom durations up to 180s):
  1. All five beats present in order (Hook, Story, Turn, Takeaway, Closer) with
     story-weighted beat timings contiguous from 0s to target duration
  2. Spoken word count within proportional target range (100-120 words per 45s)
  3. Hook is a single striking opening line with no greeting or staged setup
  4. Takeaway gives one clear practical action (no multi-step action lists)
  5. Closer is a single memorable line without hollow AI mic-drop cliches
  6. No visual, style, camera, or delivery direction; no intro/outro wrapper or inline commentary
  7. Natural spoken English free of common AI tells (em/en dashes, AI buzzwords, vague attributions,
     "not X, it's Y" rhetorical contrasts), while respecting user-approved locked text.

Usage:
  python3 scripts/validate_script.py <script_file>                     # auto-detects tier from Closer timing
  python3 scripts/validate_script.py <script_file> --duration 90       # enforces exact 90s tier
  cat draft.txt | python3 scripts/validate_script.py - --duration 60
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

BEATS = ["Hook", "Story", "Turn", "Takeaway", "Closer"]

# Story-weighted canonical boundaries by complexity tier:
# Hook and Closer stay crisp single-sentence beats (2-5s), while extra runtime
# goes into Story and Turn where narrative setup, tension, and conceptual nuance live.
CANONICAL_TIER_BOUNDARIES: dict[int, list[int]] = {
    15: [0, 1, 7, 11, 14, 15],
    30: [0, 2, 13, 21, 28, 30],
    45: [0, 3, 20, 32, 42, 45],
    60: [0, 3, 31, 46, 56, 60],
    75: [0, 4, 40, 59, 71, 75],
    90: [0, 4, 50, 72, 85, 90],
    120: [0, 4, 68, 98, 115, 120],
    150: [0, 5, 86, 124, 145, 150],
    180: [0, 5, 105, 150, 175, 180],
}

TIER_NAMES: dict[int, str] = {
    15: "Micro Hook-and-Point (15s)",
    30: "Quick Insight (30s)",
    45: "Compact Anecdote (45s)",
    60: "Standard Story Arc (60s)",
    75: "Extended Story (75s)",
    90: "Layered Story & Nuanced Turn (90s)",
    120: "Deep Narrative / Case Breakdown (120s)",
    150: "Extended Case Breakdown (150s)",
    180: "Full 3-Minute Narrative (180s)",
}

GREETING_PATTERNS = [
    r"^(hey|hi|hello|yo|welcome|sup|greetings)\b",
    r"^what'?s up\b",
    r"^good (morning|afternoon|evening)\b",
    r"^(hey|hi) (guys|everyone|folks|friends|y'all|there)\b",
]

SETUP_PATTERNS = [
    r"^today (i want|i'm going|we're going|we are going|let's)\b",
    r"^in this (video|reel|short|tiktok)\b",
    r"^(let's|i want to) talk about\b",
    r"^let's (dive in|break this down|explore|be honest|get into it)\b",
    r"^here'?s (the thing|what you need to know|why|a quick story)\b",
    r"^(real talk|honestly|quick note|story time)\b",
    r"^have you ever wondered\b",
    r"^so today\b",
]

CLICHE_CLOSERS = [
    r"\bread that again\b",
    r"\blet that sink in\b",
    r"\bthat'?s it\.?\s*that'?s the post\b",
    r"\bfull stop\.?$",
    r"\bperiod\.?$",
    r"\band that changes everything\b",
]

MULTI_ACTION_PATTERNS = [
    r"\bfirst\b.*\b(second|then|next)\b",
    r"\bstep (one|1)\b.*\bstep (two|2)\b",
    r"(?:^|\s)1[\.\)]\s+.*(?:^|\s)2[\.\)]\s+",
    r"\balso make sure to\b",
    r"\band don't forget to\b",
]

VISUAL_DIRECTION_PATTERNS = [
    r"\[[^\]]*\]",
    r"\{[^\}]*\}",
    r"\([^)]*\)",
    r"\bb-roll\b",
    r"(?:^|[.!?]\s+)cut to\b",
    r"\bcut to\s*:",
    r"\btext on screen\b",
    r"\bon-screen text\b",
    r"\bsfx\b",
    r"\bsound effect\b",
    r"\bzoom in\b",
    r"\bzoom out\b",
    r"\bfade in\b",
    r"\bfade out\b",
    r"\bvoiceover\s*:",
    r"\bvo\s*:",
    r"\bcamera\s*:",
]

AI_BUZZWORDS = [
    "additionally",
    "delve",
    "delves",
    "delving",
    "deep dive",
    "tapestry",
    "pivotal",
    "crucial",
    "enduring",
    "enhance",
    "enhances",
    "enhancing",
    "underscores",
    "underscore",
    "underscoring",
    "testament",
    "meticulous",
    "meticulously",
    "intricate",
    "intricacies",
    "vibrant",
    "bolstered",
    "garner",
    "interplay",
    "quietly",
    "robust",
    "valuable",
    "elevate",
    "elevates",
    "elevating",
    "game-changer",
    "game changer",
    "supercharge",
    "unleash",
    "seamlessly",
    "landscape",
    "showcase",
    "showcasing",
    "fostering",
    "cultivating",
    "encompassing",
]

VAGUE_ATTRIBUTIONS = [
    r"\bexperts (say|agree|argue|believe|note)\b",
    r"\bstudies (show|prove|suggest|indicate)\b",
    r"\bresearch (shows|proves|suggests)\b",
    r"\bscientists say\b",
    r"\bindustry (leaders|reports|experts)\b",
    r"\bobservers (have cited|note|say)\b",
    r"\bit is widely believed\b",
]

CONTRAST_CLICHES = [
    r"\bit'?s not (just |only |merely )?about [^.,;!?]+[,;—-]+\s*it'?s about\b",
    r"\bthis isn'?t (just |only |merely )?about [^.,;!?]+[,;.]+\s*it'?s about\b",
    r"\bnot (only|merely) [^.,;!?]+,\s*but\b",
    r"\bit'?s not [^.,;!?]+,\s*it'?s\b",
]

CHATBOT_RESIDUE = [
    r"\bi hope this helps\b",
    r"\blet me know if you'?d like\b",
    r"\bwould you like me to\b",
    r"\bhere is (your|the|a) (script|voiceover|draft)\b",
    r"\bgreat question\b",
    r"\bcertainly!\b",
    r"\bof course!\b",
]


def expected_boundaries(duration: int) -> list[int]:
    if duration in CANONICAL_TIER_BOUNDARIES:
        return list(CANONICAL_TIER_BOUNDARIES[duration])
    if duration <= 45:
        b1 = max(1, round(3 * duration / 45))
        b2 = max(b1 + 1, round(20 * duration / 45))
        b3 = max(b2 + 1, round(32 * duration / 45))
        b4 = min(duration - 1, max(b3 + 1, round(42 * duration / 45)))
        return [0, b1, b2, b3, b4, duration]
    # Story-weighted scaling for custom durations > 45s:
    # Keep Hook (3-5s) and Closer (4-5s) concise, routing added time to Story & Turn.
    hook_dur = 3 if duration <= 60 else (4 if duration <= 120 else 5)
    closer_dur = 4 if duration <= 75 else 5
    middle = duration - hook_dur - closer_dur
    story_dur = round(middle * 0.56)
    turn_dur = round(middle * 0.275)
    b1 = hook_dur
    b2 = b1 + story_dur
    b3 = b2 + turn_dur
    b4 = duration - closer_dur
    return [0, b1, b2, b3, b4, duration]


def expected_word_range(duration: int) -> tuple[int, int]:
    low = round(100 * duration / 45)
    high = round(120 * duration / 45)
    return low, high


def count_words(text: str) -> int:
    tokens = re.findall(r"[A-Za-z0-9]+(?:['’-][A-Za-z0-9]+)*", text)
    return len(tokens)


def split_sentences(text: str) -> list[str]:
    protected = re.sub(
        r"\b(Mr|Mrs|Ms|Dr|Prof|St|vs|etc|a\.m|p\.m|A\.M|P\.M|U\.S)\.",
        lambda m: m.group(0).replace(".", "<DOT>"),
        text.strip(),
    )
    parts = [p.strip() for p in re.split(r"(?<=[.!?])\s+", protected) if p.strip()]
    return [p.replace("<DOT>", ".") for p in parts]


def strip_locked_spans(text: str, locked_texts: list[str]) -> str:
    cleaned = text
    for locked in locked_texts:
        if locked.strip():
            cleaned = cleaned.replace(locked.strip(), " ")
    return cleaned


def parse_script(raw: str) -> tuple[list[dict], list[str]]:
    errors: list[str] = []
    lines = raw.strip().splitlines()
    if not lines:
        return [], ["Script output is empty."]

    if raw.strip().startswith("```"):
        errors.append("Output is wrapped in markdown code fences; output only the plain script.")

    header_re = re.compile(
        r"^(?P<beat>Hook|Story|Turn|Takeaway|Closer)"
        r"(?:\s*\((?P<start>\d+)\s*[-–]\s*(?P<end>\d+)\s*s\))?"
        r"\s*:\s*(?P<inline>.*)$"
    )

    sections: list[dict] = []
    preamble: list[str] = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        match = header_re.match(stripped)
        if match:
            inline = match.group("inline").strip()
            sections.append(
                {
                    "beat": match.group("beat"),
                    "start": int(match.group("start")) if match.group("start") is not None else None,
                    "end": int(match.group("end")) if match.group("end") is not None else None,
                    "lines": [inline] if inline else [],
                }
            )
        else:
            if not sections:
                preamble.append(stripped)
            else:
                sections[-1]["lines"].append(stripped)

    if preamble:
        errors.append(
            f"Found introductory text before the first beat label: {preamble[0]!r}. "
            "Output only the voiceover script."
        )

    return sections, errors


def infer_duration_from_sections(sections: list[dict]) -> int:
    if sections and sections[-1].get("end") is not None and sections[-1]["end"] > 0:
        return int(sections[-1]["end"])
    return 60


def validate_script(
    raw: str,
    duration: int | None = None,
    locked_texts: list[str] | None = None,
) -> dict:
    locked_texts = locked_texts or []
    errors: list[str] = []
    warnings: list[str] = []

    sections, parse_errors = parse_script(raw)
    errors.extend(parse_errors)

    resolved_duration = duration if duration is not None else infer_duration_from_sections(sections)

    found_beats = [s["beat"] for s in sections]
    if found_beats != BEATS:
        errors.append(
            f"Beats must appear in exact order {BEATS}; found {found_beats}."
        )

    bounds = expected_boundaries(resolved_duration)
    tolerance = 0 if resolved_duration in CANONICAL_TIER_BOUNDARIES else 2

    beat_word_counts: dict[str, int] = {}
    all_spoken_lines: list[str] = []

    for idx, section in enumerate(sections):
        beat = section["beat"]
        body = " ".join(section["lines"]).strip()
        if not body:
            errors.append(f"Beat '{beat}' has no spoken voiceover text.")
        beat_word_counts[beat] = count_words(body)
        all_spoken_lines.append(body)

        if idx < len(BEATS) and found_beats == BEATS:
            exp_start, exp_end = bounds[idx], bounds[idx + 1]
            if section["start"] is None or section["end"] is None:
                errors.append(
                    f"Beat '{beat}' is missing its timing label; expected '{beat} ({exp_start}-{exp_end}s):'."
                )
            else:
                if (
                    abs(section["start"] - exp_start) > tolerance
                    or abs(section["end"] - exp_end) > tolerance
                ):
                    errors.append(
                        f"Beat '{beat}' timing ({section['start']}-{section['end']}s) does not match "
                        f"expected tier timing ({exp_start}-{exp_end}s) for a {resolved_duration}s script."
                    )

    if len(sections) == 5 and all(s["start"] is not None and s["end"] is not None for s in sections):
        if sections[0]["start"] != 0:
            errors.append(f"Hook timing must start at 0s (got {sections[0]['start']}s).")
        if sections[-1]["end"] != resolved_duration:
            errors.append(
                f"Closer timing must end at {resolved_duration}s (got {sections[-1]['end']}s)."
            )
        for i in range(len(sections) - 1):
            if sections[i]["end"] != sections[i + 1]["start"]:
                errors.append(
                    f"Timing gap/overlap between {sections[i]['beat']} (ends {sections[i]['end']}s) "
                    f"and {sections[i + 1]['beat']} (starts {sections[i + 1]['start']}s)."
                )

    spoken_text = "\n".join(all_spoken_lines)
    unlocked_spoken_text = strip_locked_spans(spoken_text, locked_texts)

    total_words = sum(beat_word_counts.values())
    min_words, max_words = expected_word_range(resolved_duration)
    if not (min_words <= total_words <= max_words):
        diff = min_words - total_words if total_words < min_words else total_words - max_words
        direction = "add" if total_words < min_words else "trim"
        errors.append(
            f"Spoken word count is {total_words} words, outside target range "
            f"{min_words}-{max_words} words for {resolved_duration}s ({direction} at least {diff} words)."
        )

    by_beat = {s["beat"]: " ".join(s["lines"]).strip() for s in sections}

    # Hook checks
    hook_text = by_beat.get("Hook", "")
    if hook_text:
        hook_sentences = split_sentences(hook_text)
        hook_is_locked = any(hook_text.strip() == lt.strip() for lt in locked_texts)
        if len(hook_sentences) != 1 and not hook_is_locked:
            errors.append(
                f"Hook must be one striking opening line (1 sentence); found {len(hook_sentences)} sentences."
            )
        if not hook_is_locked:
            lowered_hook = hook_text.lower().strip("\"' ")
            for pat in GREETING_PATTERNS:
                if re.search(pat, lowered_hook):
                    errors.append(f"Hook starts with a greeting (matched {pat!r}).")
                    break
            for pat in SETUP_PATTERNS:
                if re.search(pat, lowered_hook):
                    errors.append(f"Hook starts with a staged setup (matched {pat!r}).")
                    break

    # Takeaway checks
    takeaway_text = by_beat.get("Takeaway", "")
    if takeaway_text:
        takeaway_unlocked = strip_locked_spans(takeaway_text, locked_texts).lower()
        for pat in MULTI_ACTION_PATTERNS:
            if re.search(pat, takeaway_unlocked, flags=re.IGNORECASE | re.DOTALL):
                errors.append(
                    "Takeaway appears to stack multiple actions; include exactly one practical action."
                )
                break

    # Closer checks
    closer_text = by_beat.get("Closer", "")
    if closer_text:
        closer_sentences = split_sentences(closer_text)
        closer_is_locked = any(closer_text.strip() == lt.strip() for lt in locked_texts)
        if len(closer_sentences) != 1 and not closer_is_locked:
            errors.append(
                f"Closer must be one memorable line (1 sentence); found {len(closer_sentences)} sentences."
            )
        if not closer_is_locked:
            for pat in CLICHE_CLOSERS:
                if re.search(pat, closer_text.lower()):
                    errors.append(f"Closer uses a hollow AI cliche ({pat!r}).")
                    break
        if len(sections) == 5 and len(sections[-1]["lines"]) > 1:
            last_line = sections[-1]["lines"][-1].lower()
            if "word count" in last_line or "note:" in last_line or "hope this" in last_line:
                errors.append(
                    f"Trailing note found after Closer: {sections[-1]['lines'][-1]!r}. "
                    "Output only the voiceover script."
                )

    for pat in VISUAL_DIRECTION_PATTERNS:
        m = re.search(pat, unlocked_spoken_text, flags=re.IGNORECASE)
        if m:
            errors.append(
                f"Found visual, delivery, or inline commentary marker {m.group(0)!r}; "
                "output only spoken voiceover lines."
            )
            break

    if "**" in raw or re.search(r"^#{1,6}\s", raw, flags=re.MULTILINE):
        errors.append(
            "Found markdown bolding (**) or headings (#); keep beat labels plain (e.g. 'Hook (0-3s):') and prose unadorned."
        )

    if re.search(r"^\s*[-*•]\s+", spoken_text, flags=re.MULTILINE):
        errors.append("Found bullet points inside spoken script; write continuous spoken sentences.")

    if "—" in unlocked_spoken_text or "–" in unlocked_spoken_text or " -- " in unlocked_spoken_text:
        errors.append(
            "Found em dash (—), en dash (–), or spaced double-hyphen (--) in unlocked text; "
            "rewrite with periods or commas for natural spoken cadence."
        )

    lowered_unlocked = unlocked_spoken_text.lower()
    for word in AI_BUZZWORDS:
        if re.search(rf"\b{re.escape(word)}\b", lowered_unlocked):
            errors.append(f"Found AI-sounding buzzword {word!r}; replace with plain spoken English.")

    for pat in VAGUE_ATTRIBUTIONS:
        m = re.search(pat, unlocked_spoken_text, flags=re.IGNORECASE)
        if m:
            errors.append(
                f"Found vague attribution {m.group(0)!r}; use only user-provided facts or direct phrasing."
            )

    for pat in CONTRAST_CLICHES:
        m = re.search(pat, lowered_unlocked)
        if m:
            errors.append(
                f"Found AI-sounding 'not X, it's Y' contrast {m.group(0)!r}; state the point directly."
            )

    for pat in CHATBOT_RESIDUE:
        m = re.search(pat, raw.lower())
        if m:
            errors.append(f"Found chatbot wrapper phrase {m.group(0)!r}; output only the script.")

    for beat_name, body in by_beat.items():
        for sent in split_sentences(strip_locked_spans(body, locked_texts)):
            wc = count_words(sent)
            if wc > 28:
                errors.append(
                    f"Sentence in '{beat_name}' is {wc} words long ({sent!r}); "
                    "split into shorter, punchier spoken sentences (<= 28 words)."
                )
            elif wc > 22:
                warnings.append(
                    f"Sentence in '{beat_name}' is {wc} words; check that it reads comfortably in one breath."
                )

    tier_label = TIER_NAMES.get(resolved_duration, f"Custom Duration ({resolved_duration}s)")

    return {
        "valid": len(errors) == 0,
        "duration_seconds": resolved_duration,
        "tier": tier_label,
        "expected_boundaries": bounds,
        "spoken_word_count": total_words,
        "target_word_range": [min_words, max_words],
        "beat_word_counts": beat_word_counts,
        "errors": errors,
        "warnings": warnings,
    }


def parse_duration_arg(value: str) -> int | None:
    if value.strip().lower() == "auto":
        return None
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("--duration must be a positive integer or 'auto'.")
    return parsed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a short-form voiceover script against short-form-script-writer-pro rules."
    )
    parser.add_argument(
        "script_path",
        help="Path to the plain-text script file, or '-' to read from stdin.",
    )
    parser.add_argument(
        "--duration",
        type=parse_duration_arg,
        default=None,
        help="Target video length in seconds (e.g. 30, 45, 60, 75, 90, 120) or 'auto' to infer from Closer timing (default: auto).",
    )
    parser.add_argument(
        "--locked-text",
        action="append",
        default=[],
        help="Exact user-approved wording to exempt from style/contrast rewrites (repeatable).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print validation result as JSON.",
    )
    args = parser.parse_args()

    if args.script_path == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(args.script_path).read_text(encoding="utf-8")

    result = validate_script(raw, duration=args.duration, locked_texts=args.locked_text)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "PASS" if result["valid"] else "FAIL"
        low, high = result["target_word_range"]
        print(
            f"[{status}] {result['tier']} | {result['spoken_word_count']} spoken words "
            f"(target {low}-{high} for {result['duration_seconds']}s) | "
            f"beats={result['beat_word_counts']}"
        )
        for err in result["errors"]:
            print(f"  ERROR: {err}")
        for warn in result["warnings"]:
            print(f"  WARN:  {warn}")

    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
