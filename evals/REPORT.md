# Skill Evaluation & Refinement Report (`short-form-script-writer-pro`)

Built, tested, and refined using the `skill-creator` workflow (`draft -> test -> grade -> refine -> re-test -> package`).

## Current Test Suite (`evals/evals.json` — Iteration 3 Complexity Tiers)

| ID | Name | Research? | Duration Tier | Key Rules Stress-Tested |
|---|---|---|---|---|
| 1 | `auto-60s-standard-story-meeting-index-card` | No | **60s** *(auto-selected)* | Moderate multi-beat story -> 60s Standard Story Arc (`0-3s / 3-31s / 31-46s / 46-56s / 56-60s`, `133–160w`), skips research, zero invented metrics |
| 2 | `auto-90s-with-research-layered-junior-dev-ai` | Yes | **90s** *(auto-selected)* | High narrative + conceptual nuance -> 90s Layered Story (`0-4s / 4-50s / 50-72s / 72-85s / 85-90s`, `200–240w`), `last30days` fallback research sharpens Hook/angle only, zero unapproved stats |
| 3 | `explicit-30s-quick-insight-locked-hook-coffee` | No | **30s** *(explicit)* | 30s Quick Insight (`0-2s / 2-13s / 13-21s / 21-28s / 28-30s`, `67–80w`), verbatim preservation of 17-word user-approved Hook, zero unprompted brewing trivia |
| 4 | `auto-120s-deep-narrative-agency-pricing` | No | **120s** *(auto-selected)* | Very high multi-scene narrative + economic reframe -> 120s Deep Narrative (`0-4s / 4-68s / 68-98s / 98-115s / 115-120s`, `267–320w`), zero invented dollar figures |

---

## Iteration History

### Iteration 1 (`evals/iteration-1/` — Initial 45s Baseline)
- Caught `"quietly"` (`humanizer` §12 watch word) and minor scene embellishment in Eval 1.
- Caught unprompted rhetorical durations in Eval 2's Hook (`"in ten minutes"`, `"all afternoon"`).
- Caught a word-count overshoot on the 30s script in Eval 3 (92 words vs. 67–80 target) when a 17-word locked Hook wasn't subtracted from the budget upfront.

### Iteration 2 (`evals/iteration-2/` — Refined 45s & 30s Validation)
- Added pre-draft word budgeting, expanded `humanizer` watch words in `SKILL.md` and `scripts/validate_script.py`, and tightened Accuracy Rules.
- All 45s (`107w`, `112w`) and 30s (`70w`) test cases passed **7/7 expectations (100%)**.

### Iteration 3 (`evals/iteration-3/` — Complexity-Based Duration Options)
- Replaced the one-size-fits-all 45s default with **story-weighted Complexity-Based Duration Options** (`30s`, `45s`, `60s` narrative default, `75s`, `90s`, `120s`, plus custom schedules up to `180s`) so `Hook` (`2–4s`) and `Closer` (`2–5s`) stay crisp single sentences while added runtime goes into `Story` and `Turn`.
- Fixed a false-positive regex in `scripts/validate_script.py` where ordinary spoken phrases like `"delivered a launch cut to a repeat client"` triggered the `"cut to"` stage-direction check; scoped `"cut to"` detection to sentence/line openings and `"cut to:"` labels.
- Added `--duration auto` inference from `Closer` timing to `scripts/validate_script.py`.
- All 4 complexity-tier evaluations passed **7/7 expectations (100%)** with zero validator errors or warnings:
  - **Eval 1 (`60s` Standard Story Arc):** `PASS` — **135 spoken words** (`target 133–160`), `{'Hook': 12, 'Story': 67, 'Turn': 28, 'Takeaway': 19, 'Closer': 9}`
  - **Eval 2 (`90s` Layered Story, with research):** `PASS` — **214 spoken words** (`target 200–240`), `{'Hook': 17, 'Story': 110, 'Turn': 47, 'Takeaway': 27, 'Closer': 13}`
  - **Eval 3 (`30s` Quick Insight, locked Hook):** `PASS` — **70 spoken words** (`target 67–80`), `{'Hook': 17, 'Story': 22, 'Turn': 11, 'Takeaway': 12, 'Closer': 8}`
  - **Eval 4 (`120s` Deep Narrative):** `PASS` — **292 spoken words** (`target 267–320`), `{'Hook': 14, 'Story': 174, 'Turn': 65, 'Takeaway': 26, 'Closer': 13}`
