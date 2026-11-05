# short-form-script-writer-pro

An agent skill that writes natural, spoken-English voiceover scripts for short-form vertical videos (**Instagram Reels**, **TikTok**, **YouTube Shorts**) by matching script duration to story and concept complexity, integrating optional recent-discourse research, stripping AI writing tells, and running deterministic validation before output.

## Complexity-Based Duration Options

Instead of forcing every story into 45 seconds, the skill selects the matching story-weighted duration tier when the user does not specify a length—keeping `Hook` (`2–4s`) and `Closer` (`2–5s`) as sharp single sentences while giving `Story` and `Turn` the room needed to establish real narrative tension and conceptual clarity:

| Tier | Complexity Fit | Beat Timings (`Hook / Story / Turn / Takeaway / Closer`) | Spoken Words |
|---|---|---|---|
| **30s — Quick Insight** | Single observation, fast myth-bust, or one-step tip | `0-2s / 2-13s / 13-21s / 21-28s / 28-30s` | **67–80** |
| **45s — Compact Anecdote** | Simple before-and-after habit shift | `0-3s / 3-20s / 20-32s / 32-42s / 42-45s` | **100–120** |
| **60s — Standard Story Arc** *(story default)* | Full story needing setup, friction, turning point, and payoff | `0-3s / 3-31s / 31-46s / 46-56s / 56-60s` | **133–160** |
| **75s — Extended Story** | Story arc with an extra complication or context bridge | `0-4s / 4-40s / 40-59s / 59-71s / 71-75s` | **167–200** |
| **90s — Layered Story & Nuanced Turn** | Multi-beat arc or counterintuitive concept needing reframing | `0-4s / 4-50s / 50-72s / 72-85s / 85-90s` | **200–240** |
| **120s — Deep Narrative / Case Breakdown** | Multi-scene story with escalating stakes or dense source facts | `0-4s / 4-68s / 68-98s / 98-115s / 115-120s` | **267–320** |

Custom user-requested durations up to `180s` are also supported (`references/combined-skills-fallback.md`).

## Combined Skills

- **`last30days`** (`/mnt/skills/plugins/last30days/SKILL.md`) — optional research on what people are currently saying about the topic (used strictly to sharpen the Hook and angle without adding unapproved research facts).
- **`humanizer`** (`/mnt/skills/plugins/humanizer/SKILL.md`) — strips AI-sounding phrasing, contrast clichés, forced triads, and dash connectors so every line sounds natural read aloud.
- **`skill-creator`** (`/mnt/skills/examples/skill-creator/SKILL.md`) — used to build, test, validate, and refine this skill (`evals/`, `scripts/validate_script.py`).

If either `last30days` or `humanizer` is unavailable in the host environment, the skill automatically completes that step manually using the built-in rules in [`SKILL.md`](SKILL.md) and [`references/combined-skills-fallback.md`](references/combined-skills-fallback.md).

## Repository Layout

```text
.
├── SKILL.md                                 # Core skill definition, duration tiers, rules, and example
├── references/
│   └── combined-skills-fallback.md          # Manual fallback playbooks & full 15s–180s tier guide
├── scripts/
│   └── validate_script.py                   # Deterministic beat, tier-timing, word-count, & AI-tell validator
├── evals/
│   ├── evals.json                           # Complexity-tier test prompts & expectations (30s–120s)
│   ├── REPORT.md                            # Iteration 1 -> Iteration 3 test & refinement report
│   ├── iteration-1/                         # Initial baseline diagnostics
│   ├── iteration-2/                         # Refined 45s & 30s outputs
│   └── iteration-3/                         # Complexity-tier outputs (30s, 60s, 90s, 120s — 100% pass)
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
# Auto-detects duration tier from Closer timing:
python3 scripts/validate_script.py path/to/script.txt

# Or assert an explicit duration tier and locked user-approved phrasing:
python3 scripts/validate_script.py path/to/script.txt --duration 90
python3 scripts/validate_script.py path/to/script.txt --duration 30 \
  --locked-text "Your morning coffee tastes bitter because the water is too hot, not because the beans are bad."
```
