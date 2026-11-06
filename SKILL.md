---
name: short-form-script-writer-pro
description: Writes spoken-English voiceover scripts for short-form vertical videos (Instagram Reels, TikTok, YouTube Shorts) by matching script duration (30s to 120s+) to concept and story complexity, combining optional current-discourse research with AI-pattern removal and strict 5-beat validation. Use this skill whenever the user asks for a short-form video script, an Instagram Reels, TikTok, or YouTube Shorts script, a vertical social video script, a creator story or monologue, or any voiceover (VO) script, even if they paste rough notes, a story, or a topic without specifying length.
license: MIT
metadata:
  version: "1.2.0"
  author: Axmgill
---

# Short-Form Script Writer Pro

Write tight, natural spoken-English voiceover scripts for Instagram Reels, TikTok, and YouTube Shorts through a single end-to-end workflow that sizes script length to the complexity of the story and idea, integrates optional recent-discourse research, strips AI writing tells, and validates every rule before output.

## Agent-Agnostic Packaging

Nothing in this skill is locked to a single model or vendor. The exact same protocol ships across four surfaces, kept in sync by `tools/check.sh`:

- **`SKILL.md` (this file)** — Native skill entry point for **Claude** (Claude Code, Claude.ai / Cowork via `short-form-script-writer-pro.skill`), **Gemini Skills** (via `bundles/short-form-script-writer-pro.zip`), **Codex**, **Cursor**, and **OpenCode**.
- **`AGENTS.md`** — Universal repository instructions read natively by **Codex**, **Cursor**, **GitHub Copilot**, **Gemini CLI**, **Kimi CLI**, **Windsurf**, **Amp**, **Cline**, and **Devin**.
- **`portable/`** — Zero-file, copy-paste prompt blocks sized to the exact character limits of **Gemini Gems** (`portable/gemini-gem-instructions.md`), **ChatGPT** Custom GPTs / Projects / Custom Instructions (`portable/system-prompt.md`, `portable/chatgpt-instructions.md`, `portable/mini-prompt.md`), **Kimi / Kimi+** (`portable/kimi-instructions.md`), and any plain chat window (`portable/kickoff-prompt.md`).
- **`llms.txt` & `llms-full.txt`** — Single-file corpus you can drop straight into **Kimi**, **ChatGPT**, **Gemini**, **Claude Projects**, **DeepSeek**, **Grok**, **Perplexity**, or any RAG / API knowledge base.

## Combined Capabilities & Host-Agnostic Fallbacks

This workflow combines three capabilities and adapts automatically to whichever tools your host app provides:

1. **Recent-discourse research (`last30days` or native web search):**
   - On Claude skill hosts where `/mnt/skills/plugins/last30days/SKILL.md` is installed, read and use it.
   - On **Gemini, ChatGPT, Kimi, Perplexity, Grok, or any browsing-enabled agent**, use the host's built-in web/search capability scoped to discussions from the last 30 days (see `references/combined-skills-fallback.md`).
   - On offline hosts with no search access, sharpen the hook and angle directly from tensions in the user's input without inventing recent trends.
2. **AI-tell removal (`humanizer` or built-in rewrite pass):**
   - On Claude skill hosts where `/mnt/skills/plugins/humanizer/SKILL.md` is installed, read and apply it in embedded mode.
   - Everywhere else, run the complete built-in Humanizer pass in Step 4 below (expanded in `references/combined-skills-fallback.md`).
3. **Evaluation & validation (`skill-creator` / `/mnt/skills/examples/skill-creator/SKILL.md` + `scripts/validate_script.py`):**
   - Used to build, test, and refine this skill (`evals/`), with `scripts/validate_script.py` available when a Python shell is present and the identical manual 7-point checklist when running in chat-only apps.

Never mention missing skill paths, host limitations, or internal workflow steps in your output.

---

## Inputs to Extract

Read these five inputs from the user's request:

1. **Story, topic, or source material** — the experience, anecdote, premise, or notes to build from.
2. **Core message** — the central insight or point the viewer should walk away believing.
3. **Takeaway or action to include** — the single practical step the viewer can try.
4. **Target length** — use the user's explicit duration if given; otherwise **select the matching Complexity-Based Duration Option below** (`30s`, `45s`, `60s`, `75s`, `90s`, or `120s`) based on how much room the story and concept need to land cleanly (using **60s** as the baseline narrative default whenever a story needs setup, friction, and a turning point).
5. **Whether research is requested** — default to **no** unless the user explicitly asks for current, recent, or trending context (for example, *"see what people are currently saying"*, *"use current trends"*, *"research recent chatter"*).

Also note any **already-approved wording or locked elements** in the conversation so they remain untouched unless the user asks to revise them.

---

## Workflow

Execute all six steps in order. Keep Steps 1–5 completely internal so the final reply contains only the finished script.

### 1. Intake & Complexity Sizing
Extract the five inputs above from the user's request.
- **Select duration by complexity when unspecified:** Evaluate (a) how many distinct beats the story needs (setup, conflict/mistake, turning point, resolution), (b) whether the core message is immediately intuitive or counterintuitive enough to need unpacking, and (c) how much concrete source material the user supplied:
  - **Low complexity (single tip or quick observation):** `30s`
  - **Light complexity (simple before-and-after shift):** `45s`
  - **Moderate complexity (full story arc with setup, friction, shift, and payoff):** `60s` *(default for narrative stories)*
  - **Moderate-high complexity (story plus an extra complication or context bridge):** `75s`
  - **High complexity (multi-beat story arc or counterintuitive concept needing reframing):** `90s`
  - **Very high complexity (multi-scene narrative, escalating stakes, or dense case study):** `120s`
- **Never pad thin material into a long tier:** Only choose `90s` or `120s` automatically when the user's story or concept genuinely carries enough substance to fill it without inventing scenes or metrics.
- **If the topic is clear, proceed immediately without asking questions.** Derive a natural core message and one concrete, practical action directly from the user's premise when not stated explicitly. Ask one brief clarifying question **only** if the request gives no usable topic or source material at all.

### 2. Research *(only if the user asks for current or trending context)*
Skip this step entirely unless the user asks for current, recent, or trending context.
- **When requested:** Use `/mnt/skills/plugins/last30days/SKILL.md` if readable; otherwise use the host's native web search (Google Search in Gemini, Web Search in ChatGPT, `联网搜索` in Kimi, or `WebSearch` tools) to check what people have been saying about the topic over the last 30 days (recurring frustrations, everyday phrasing, and tension points).
- **Strict research boundary:** Use findings **only** to sharpen the **Hook** and **angle**. **Do not add research facts, statistics, quotes, study names, or claims to the script unless the user explicitly approves them.**

### 3. Draft
Budget the spoken word count before writing a single sentence so the draft lands inside the target window on the first pass:
- Compute the target range `round(100 * T / 45)` to `round(120 * T / 45)` spoken words (aiming near the midpoint `round(110 * T / 45)`).
- If the user has already approved or locked specific lines (for example, a 17-word Hook), subtract those locked words from the midpoint budget first and distribute only the **remaining** words across the unlocked beats.
- Write the draft using the five-beat structure, tier timing schedule, and Accuracy Rules below. Use extra time in `60s–120s` scripts to establish concrete stakes, tension, and conceptual clarity in `Story` and `Turn`—never to pad with repetition or adjectives.

### 4. Humanize
Use `/mnt/skills/plugins/humanizer/SKILL.md` (embedded mode) if readable; otherwise run the built-in Humanizer pass directly (see `references/combined-skills-fallback.md`):
- Strip *"not X, but Y"* / *"it's not X, it's Y"* contrasts, staged run-ups (*"Here's the thing"*, *"Let's be honest"*, *"Real talk"*), forced rule-of-three lists, em/en dashes (`—`, `–`, ` -- `), AI buzzwords (*delve, pivotal, crucial, quietly, landscape, tapestry, testament, underscore, robust, enhance, elevate, game-changer*), shallow *-ing* tails, vague attributions (*"Experts say"*, *"Studies show"*), and hollow mic-drop closers (*"Read that again."*, *"Let that sink in."*).
- **Preserve invariants:** Keep the five-beat structure, target spoken word count, factual accuracy, and any user-approved wording intact during humanization.

### 5. Validate
Verify the humanized draft against every item in the Validation Checklist below.
- Count **spoken words only** (exclude the five beat labels).
- When a Python shell and this repository's `scripts/validate_script.py` are available, run `python3 scripts/validate_script.py` with `--duration <seconds>` (and `--locked-text "<phrase>"` for any user-approved lines). In chat-only hosts (Gemini, ChatGPT, Kimi, web projects), count spoken words beat by beat and verify every checklist rule manually before responding.
- Fix every failure before producing output, then re-verify until every check passes.

### 6. Output
Output **only** the final voiceover script.

---

## Script Structure & Duration Options

### Five Core Beats
Every script—regardless of length—follows the same five beats in exact order:

1. **`Hook`:** One striking opening line (single sentence), no greeting or setup.
2. **`Story`:** The story in clear, well-paced narrative beats matched to concept complexity.
3. **`Turn`:** Connects the story to the core message and unpacks *why* it matters to the viewer.
4. **`Takeaway`:** One practical, concrete action the viewer can apply.
5. **`Closer`:** One memorable closing line (single sentence).

### Story-Weighted Duration Options by Complexity

Above 45 seconds, beat timings are **story-weighted rather than naively linear**: viewer swipe decisions still happen in the first `2–4s` and a single-sentence `Closer` still takes `3–5s`, so added runtime goes into **`Story`** and **`Turn`** where narrative setup, conflict, and conceptual nuance actually live.

| Option | Complexity Level & Best Use | Hook | Story | Turn | Takeaway | Closer | Spoken Words |
|---|---|---|---|---|---|---|---|
| **30s — Quick Insight** | Single observation, fast myth-bust, or one-step fix with minimal backstory | `0-2s` | `2-13s` | `13-21s` | `21-28s` | `28-30s` | **67–80** |
| **45s — Compact Anecdote** | Simple before-and-after habit shift or single-moment realization | `0-3s` | `3-20s` | `20-32s` | `32-42s` | `42-45s` | **100–120** |
| **60s — Standard Story Arc** *(story default)* | Full story needing setup, concrete friction/mistake, turning point, and payoff | `0-3s` | `3-31s` | `31-46s` | `46-56s` | `56-60s` | **133–160** |
| **75s — Extended Story** | Narrative arc with an extra complication or context bridge before the lesson | `0-4s` | `4-40s` | `40-59s` | `59-71s` | `71-75s` | **167–200** |
| **90s — Layered Story & Nuanced Turn** | Multi-beat story (belief → failure → discovery → shift) or counterintuitive idea | `0-4s` | `4-50s` | `50-72s` | `72-85s` | `85-90s` | **200–240** |
| **120s — Deep Narrative / Case Breakdown** | Multi-scene story with escalating stakes, detailed case study, or dense source facts | `0-4s` | `4-68s` | `68-98s` | `98-115s` | `115-120s` | **267–320** |

**Custom lengths (up to 180s):** If the user requests a specific duration `T` outside the table above:
- For `T <= 45`: scale `[0, 3, 20, 32, 42, 45]` proportionally (`[0, round(3*T/45), round(20*T/45), round(32*T/45), round(42*T/45), T]`).
- For `T > 45`: keep `Hook` at `3–5s` and `Closer` at `4–5s`, allocating the middle runtime (`T - Hook - Closer`) as `~56% Story`, `~27.5% Turn`, and `~16.5% Takeaway` (see `references/combined-skills-fallback.md` for `15s`, `150s`, and `180s` schedules).
- Scale spoken word count across all lengths at **100–120 words per 45 seconds** (`round(100 * T / 45)` to `round(120 * T / 45)` words).

### Structuring `Story` Depth Across Tiers
- **`30s–45s`:** State what was happening, the single change, and the immediate difference in 2–4 crisp sentences.
- **`60s–75s`:** Establish starting context and goal -> show the concrete friction or cost -> mark the turning point -> show what changed afterward (5–8 sentences).
- **`90s–120s`:** Build a full arc—why the old approach felt reasonable -> how the problem compounded -> the specific moment it broke or clicked -> what changed in practice -> concrete aftermath—then use `Turn` to unpack *why* conventional intuition gets it wrong before delivering one clear `Takeaway`.

---

## Rules

### Writing Rules
- **Conversational spoken English:** Write for the ear and breath. Use natural spoken contractions (*don't, it's, wasn't, you'll*) unless preserving exact user-approved text.
- **Short, punchy sentences:** Keep sentences brisk and easy to say in one breath (aim for 6–20 words; never exceed 28 words in unlocked text). Vary sentence length so the cadence never sounds robotic.
- **No jargon or filler:** Cut throat-clearing words (*actually, basically, honestly, literally, essentially*) and corporate or creator jargon.
- **Word count discipline:** Maintain **100–120 spoken words per 45 seconds** across every tier (`round(100 * T / 45)` to `round(120 * T / 45)` words, excluding beat labels).
- **Natural read-aloud flow:** Read every line silently as spoken audio. Fix tongue-twisters, stiff transitions, and written-only syntax.
- **No AI-sounding patterns:** Avoid inflated phrasing (*pivotal moment, game-changer, testament, landscape, delve, crucial, quietly*), rule-of-three padding (three parallel adjectives or nouns), em dash or en dash connectors (`—`, `–`, ` -- `), *"not X, it's Y"* rhetorical setups, and vague attributions (*"experts say"*, *"studies show"*).

### Output Rules
- **Beat-labeled voiceover only:** Output only the voiceover script labeled by beat (`Hook`, `Story`, `Turn`, `Takeaway`, `Closer`) with contiguous timing ranges in plain text (no `**bold**` or `#` markdown headings).
- **No visual, style, or motion direction:** Never include `[B-roll]`, `[Cut to]`, `(pause)`, `(whisper)`, camera notes, on-screen text cues, SFX, or delivery tags.
- **No introduction or closing notes:** Start on `Hook (...)` and end on the final word of `Closer (...)`. Do not announce which duration tier you picked—the beat timing labels already show it. Do not include preambles, word-count footers, or follow-up offers.
- **No commentary inside the script:** Never place inline notes, placeholders, or explanations inside any beat.
- **Respect approved elements:** Do not alter wording, hooks, closers, or facts the user has already approved unless explicitly told to change them.

### Accuracy Rules
- **Grounded facts only:** Use only facts the user provides or that are clearly established common knowledge.
- **Zero fabrication:** Never invent numbers, timeframes, team sizes, names, quotes, domain trivia (such as unprompted temperatures or percentages), or micro-scene details (such as where people sat, what day of the week it was, or how many minutes something took) to make a Hook or Story sound more vivid or to fill a longer duration tier.
- **Keep uncertain details general:** Where the user leaves a detail unspecified (for example, *"meetings got noticeably shorter"* or *"shipped features fast"*), keep the phrasing general rather than inventing a specific metric or clock time.

---

## Validation Checklist

Before outputting the script, confirm every item below passes:

- [ ] **All five beats present and labeled:** `Hook`, `Story`, `Turn`, `Takeaway`, and `Closer` appear in exact order with contiguous timing labels matching the selected duration tier.
- [ ] **Word count within range for the target length:** Spoken words (excluding beat labels) fall inside `round(100*T/45)–round(120*T/45)` words (`67–80` for 30s, `100–120` for 45s, `133–160` for 60s, `167–200` for 75s, `200–240` for 90s, `267–320` for 120s).
- [ ] **Hook has no greeting or setup:** Single striking opening sentence with no *"Hey guys"*, *"Welcome back"*, *"Today I want to talk about"*, *"In this video"*, or *"Here's the thing"*.
- [ ] **Exactly one takeaway action:** `Takeaway` gives one clear, practical action—not a multi-step checklist and not an abstract platitude.
- [ ] **No visual or style direction:** Zero bracketed cues, parenthetical stage directions, camera/editing instructions, markdown formatting, or intro/outro wrapper text.
- [ ] **No invented facts:** Every concrete detail traces back to the user's input or clearly established knowledge; zero unapproved research facts appear in the script.
- [ ] **Reads naturally aloud:** Conversational spoken cadence, short punchy sentences, single-sentence Closer, and zero AI-sounding tells (no em dashes, forced triads, inflated words, or vague attributions).

---

## Example (Auto-Selected 60s Standard Story Arc)

### Sample Input
> Write a Reels voiceover script. Story: I used to answer client emails first thing at 8 AM because I wanted clients to feel taken care of, and I kept wondering why my big projects stalled for weeks. Two months ago I hit a deadline scare, moved email to 11 AM, and started finishing my hardest project task before opening my inbox. Clients didn't complain once, and my stalled work finally started shipping. Core message: your morning focus goes to whatever you open first. Takeaway: wait until 11 AM to check messages tomorrow and spend your first hour on one hard task.

### Sample Output
```text
Hook (0-3s):
Opening your inbox at 8 AM hands your sharpest hour to everyone else.

Story (3-31s):
I used to start every workday answering client emails right at 8 AM because I wanted clients to feel taken care of. I stayed busy all morning, but my big projects stalled for weeks. Two months ago, a close deadline scare forced me to change my routine. I kept email closed until 11 AM and worked on my hardest project task before opening my inbox. Not a single client complained, and my stalled work finally started shipping.

Turn (31-46s):
Your morning focus goes to whatever you open first. Starting inside your inbox trains your brain to react to other people's requests instead of moving your own real work forward.

Takeaway (46-56s):
Tomorrow morning, wait until 11 AM to check messages and spend your first hour working on one hard task.

Closer (56-60s):
Protect your first hour before you answer anyone else's.
```
