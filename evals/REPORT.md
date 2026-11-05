# Skill Evaluation & Refinement Report (`short-form-script-writer-pro`)

Built, tested, and refined using the `skill-creator` workflow (`draft -> test -> grade -> refine -> re-test -> package`).

## Test Suite (`evals/evals.json`)

| ID | Name | Research? | Target Length | Key Rules Stress-Tested |
|---|---|---|---|---|
| 1 | `no-research-45s-meeting-index-card` | No | 45s (default) | Skips research, 100–120 spoken words, no invented team sizes/metrics, humanizer pass |
| 2 | `with-research-45s-junior-dev-ai-coding` | Yes | 45s (default) | `last30days` fallback research, sharpens Hook/angle only, zero unapproved research stats leaked |
| 3 | `scaled-30s-locked-hook-coffee` | No | 30s (scaled) | Proportional timing (`0-2s`, `2-13s`, `13-21s`, `21-28s`, `28-30s`), 67–80 spoken words, verbatim preservation of 17-word user-approved Hook, zero unprompted brewing temperature trivia |

---

## Iteration 1 Findings (`evals/iteration-1/`)

- **Eval 1 (5/7 expectations passed, 71%):**
  - Spoken word count landed at 115 words (`100-120`), all 5 beats present.
  - **Failures caught:** Hook used `"quietly"` (an AI watch word in `humanizer` §12 not yet flagged by `validate_script.py`), and Story embellished `"multitasking on Slack"` into `"answering Slack under the table"`.
- **Eval 2 (6/7 expectations passed, 86%):**
  - Live recent-discussion search surfaced recurring developer frustrations (shipping fast with AI then freezing when debugging your own merged code because skipping the struggle skipped building a mental model). External statistics (`59%`, `20%` Stanford figure, Anthropic white paper, tool names) were properly excluded.
  - **Failure caught:** Hook introduced unprompted rhetorical durations (`"in ten minutes"`, `"all afternoon"`) and Story added minor unprompted scene blocking (`"When we opened the file together"`).
- **Eval 3 (6/7 expectations passed, 86%):**
  - 30s proportional beat labels (`0-2s`, `2-13s`, `13-21s`, `21-28s`, `28-30s`) and locked 17-word Hook were intact.
  - **Failure caught:** Spoken word count reached **92 words** (`[FAIL]` against 30s target of `67-80` words) because drafting did not subtract the 17-word locked Hook from the 74-word midpoint budget before allocating words to the remaining four beats.

---

## Refinements Applied Before Iteration 2

1. **Pre-draft word budgeting (`SKILL.md` Step 3):** Added explicit instructions to compute the midpoint budget `round(110 * T / 45)` first, subtract any user-locked beat words upfront, and distribute only the remaining word budget across unlocked beats.
2. **Expanded `humanizer` watch-word enforcement (`SKILL.md` Step 4 & `scripts/validate_script.py`):** Added `quietly`, `additionally`, `enduring`, `enhance`, `robust`, `valuable`, `elevate`, and `deep dive` from `humanizer` §12 so `validate_script.py` flags them automatically.
3. **Sharpened Accuracy Rules (`SKILL.md`):** Explained why rhetorical clock times, technical trivia numbers, and micro-scene blocking count as invented details and break creator trust.

---

## Iteration 2 Results (`evals/iteration-2/`)

All 3 test cases passed **7/7 expectations (100%)** and passed `scripts/validate_script.py` with zero errors or warnings:

- **Eval 1 (`no-research-45s-meeting-index-card`):** `PASS` — **107 spoken words** (`target 100-120`), `{'Hook': 12, 'Story': 43, 'Turn': 26, 'Takeaway': 17, 'Closer': 9}`.
- **Eval 2 (`with-research-45s-junior-dev-ai-coding`):** `PASS` — **112 spoken words** (`target 100-120`), `{'Hook': 17, 'Story': 38, 'Turn': 28, 'Takeaway': 19, 'Closer': 10}`.
- **Eval 3 (`scaled-30s-locked-hook-coffee`):** `PASS` — **70 spoken words** (`target 67-80`), `{'Hook': 17, 'Story': 22, 'Turn': 11, 'Takeaway': 12, 'Closer': 8}`.
