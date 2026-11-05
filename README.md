# short-form-script-writer-pro

An agent skill that writes natural, spoken-English voiceover scripts for short-form vertical videos (**Instagram Reels**, **TikTok**, **YouTube Shorts**) by combining optional recent-discourse research, structured 5-beat pacing, AI-tell removal, and deterministic validation into one workflow.

## Combined Skills

- **`last30days`** (`/mnt/skills/plugins/last30days/SKILL.md`) — optional research on what people are currently saying about the topic (used strictly to sharpen the Hook and angle without adding unapproved research facts).
- **`humanizer`** (`/mnt/skills/plugins/humanizer/SKILL.md`) — strips AI-sounding phrasing, contrast clichés, forced triads, and dash connectors so every line sounds natural read aloud.
- **`skill-creator`** (`/mnt/skills/examples/skill-creator/SKILL.md`) — used to build, test, validate, and refine this skill (`evals/`, `scripts/validate_script.py`).

If either `last30days` or `humanizer` is unavailable in the host environment, the skill automatically completes that step manually using the built-in rules in [`SKILL.md`](SKILL.md) and [`references/combined-skills-fallback.md`](references/combined-skills-fallback.md).

## Repository Layout

```text
.
├── SKILL.md                                 # Core skill definition, rules, checklist, and example
├── references/
│   └── combined-skills-fallback.md          # Manual fallback playbooks & proportional timing table
├── scripts/
│   └── validate_script.py                   # Deterministic beat, word-count, & AI-tell validator
├── evals/
│   ├── evals.json                           # Test prompts & expectations (with & without research)
│   ├── REPORT.md                            # Iteration 1 -> Iteration 2 test & refinement report
│   ├── iteration-1/                         # Initial test outputs & grading diagnostics
│   └── iteration-2/                         # Refined test outputs (100% pass rate)
└── short-form-script-writer-pro.skill       # Distributable .skill archive built with skill-creator
```

## Installation

### Claude.ai / Cowork
Upload **`short-form-script-writer-pro.skill`** in **Settings → Capabilities → Skills**.

### Claude Code
```bash
git clone https://github.com/Axmgill/short_form_script.git ~/.claude/skills/short-form-script-writer-pro
```

## Running the Deterministic Validator

```bash
python3 scripts/validate_script.py path/to/script.txt --duration 45
# With user-approved locked phrasing on a 30-second script:
python3 scripts/validate_script.py path/to/script.txt --duration 30 \
  --locked-text "Your morning coffee tastes bitter because the water is too hot, not because the beans are bad."
```
