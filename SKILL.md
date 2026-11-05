---
name: short-form-script-writer-pro
description: Writes spoken-English voiceover scripts for short-form vertical videos (Instagram Reels, TikTok, YouTube Shorts) by combining optional current-discourse research (last30days) with AI-pattern removal (humanizer) and strict 5-beat timing and word-count validation. Use this skill whenever the user asks for a short-form video script, an Instagram Reels, TikTok, or YouTube Shorts script, a vertical social video script, a creator monologue, or any voiceover (VO) script, even if they paste rough notes, a personal story, or a topic and ask to turn it into a 15-to-90-second video.
license: MIT
metadata:
  version: "1.0.0"
  author: Axmgill
---

# Short-Form Script Writer Pro

Write tight, natural spoken-English voiceover scripts for Instagram Reels, TikTok, and YouTube Shorts through a single end-to-end workflow that combines optional recent-discourse research, structured 5-beat storytelling, AI-tell removal, and pre-output validation.

## Combined Skills & Fallback Architecture

This workflow integrates three skills:

- **`last30days`** (`/mnt/skills/plugins/last30days/SKILL.md`): Optional research on what people are currently saying about the topic across social and web discussions.
- **`humanizer`** (`/mnt/skills/plugins/humanizer/SKILL.md`): Removes AI-sounding phrasing, rhythm, and structural tells from the draft so it sounds genuinely human when read aloud.
- **`skill-creator`** (`/mnt/skills/examples/skill-creator/SKILL.md`): Used to build, test, evaluate, and refine this skill (`evals/evals.json`, `scripts/validate_script.py`).

**Fallback rule:** If a combined skill (`/mnt/skills/plugins/last30days/SKILL.md` or `/mnt/skills/plugins/humanizer/SKILL.md`) is unavailable or unreadable in the current host environment, complete that step manually following the exact same rules below (and see `references/combined-skills-fallback.md` for detailed fallback procedures). Never mention missing skill paths or workflow mechanics in the output.

---

## Inputs to Extract

Read these five inputs from the user's request:

1. **Story, topic, or source material** — the experience, anecdote, premise, or notes to build from.
2. **Core message** — the central insight or point the viewer should walk away believing.
3. **Takeaway or action to include** — the single practical step the viewer can try.
4. **Target length** — default to **45 seconds** if the user does not specify a duration.
5. **Whether research is requested** — default to **no** unless the user explicitly asks for current, recent, or trending context (for example, *"see what people are currently saying"*, *"use current trends"*, *"research recent chatter"*).

Also note any **already-approved wording or locked elements** in the conversation so they remain untouched unless the user asks to revise them.

---

## Workflow

Execute all six steps in order. Keep Steps 1–5 completely internal so the final reply contains only the finished script.

### 1. Intake
Extract the five inputs above from the user's request.
- **If the topic is clear, proceed immediately without asking questions.** When the user omits an explicit core message or takeaway action, derive a natural core message and one concrete, practical action directly from their story or topic without inventing facts.
- Ask one brief clarifying question **only** if the request gives no usable topic or source material at all.

### 2. Research *(only if the user asks for current or trending context)*
Skip this step entirely unless the user asks for current, recent, or trending context.
- **When requested:** Check `/mnt/skills/plugins/last30days/SKILL.md`. If available, read it in full and run its research workflow to gather what people are currently saying about the topic.
- **Fallback:** If `/mnt/skills/plugins/last30days/SKILL.md` is unavailable, run focused recent-discussion searches (last 30 days) using available host search tools to spot recurring frustrations, everyday phrasing, and tension points (see `references/combined-skills-fallback.md`).
- **Strict research boundary:** Use findings **only** to sharpen the **Hook** and **angle**. **Do not add research facts, statistics, quotes, study names, or claims to the script unless the user explicitly approves them.**

### 3. Draft
Budget the spoken word count before writing a single sentence so the draft lands inside the target window on the first pass:
- Compute the target range `round(100 * T / 45)` to `round(120 * T / 45)` spoken words (aiming near the midpoint `round(110 * T / 45)`).
- If the user has already approved or locked specific lines (for example, a 17-word Hook), subtract those locked words from the midpoint budget first and distribute only the **remaining** words across the unlocked beats.
- Write the draft using the five-beat structure and Accuracy Rules below.

### 4. Humanize
Check `/mnt/skills/plugins/humanizer/SKILL.md`.
- **When available:** Read `/mnt/skills/plugins/humanizer/SKILL.md` and pass the draft through its rewrite rules (embedded mode) so every line sounds like a real person talking into a microphone.
- **Fallback:** If `/mnt/skills/plugins/humanizer/SKILL.md` is unavailable, run a manual humanizer pass using the Writing Rules below and `references/combined-skills-fallback.md`: strip *"not X, but Y"* contrasts, staged run-ups (*"Here's the thing"*, *"Let's be honest"*), forced rule-of-three lists, em/en dashes, AI buzzwords (*delve, pivotal, crucial, quietly, landscape, tapestry, testament, underscore, robust, enhance, game-changer*), shallow *-ing* tails, vague attributions (*"Experts say"*, *"Studies show"*), and hollow mic-drop closers (*"Read that again."*, *"Let that sink in."*).
- **Preserve invariants:** Keep the five-beat structure, target spoken word count, factual accuracy, and any user-approved wording intact during humanization.

### 5. Validate
Verify the humanized draft against every item in the Validation Checklist below.
- Count **spoken words only** (exclude the five beat labels).
- If Python and shell execution are available, run `python3 scripts/validate_script.py` (located in this skill's directory) with `--duration <seconds>` (and `--locked-text "<phrase>"` for any user-approved lines) to catch word-count drift, timing mismatches, visual cues, greetings, or leftover AI tells deterministically.
- Fix every failure before producing output, then re-verify until every check passes.

### 6. Output
Output **only** the final voiceover script.

---

## Script Structure

### Default Structure (45 seconds — 100 to 120 spoken words)

1. **`Hook (0-3s):`** One striking opening line (single sentence, ~8–15 words). Drop straight into tension, surprise, or a concrete claim—no greeting and no setup.
2. **`Story (3-20s):`** The story in tight, clear beats (~38–48 words, 3–4 short sentences). Stick to what happened and why it mattered without throat-clearing.
3. **`Turn (20-32s):`** Connects the story to the core message (~25–32 words, 2–3 short sentences). Show the viewer why the story applies to them.
4. **`Takeaway (32-42s):`** One practical action (~18–26 words, 1–2 short sentences). Tell the viewer one specific thing they can do today or next time.
5. **`Closer (42-45s):`** One memorable line (single sentence, ~6–12 words). Land the core idea cleanly without cliché filler.

### Scaling for Other Target Lengths

When the user requests a length `T` other than 45 seconds, scale both beat timings and spoken word count proportionally relative to 45 seconds:

- **Timing boundaries:** `[0, round(3*T/45), round(20*T/45), round(32*T/45), round(42*T/45), T]` (keep boundaries contiguous from `0` to `T`; ensure Hook and Closer are at least `1s` each).
- **Spoken word-count range:** `round(100 * T / 45)` to `round(120 * T / 45)` spoken words.
  - **30s:** `Hook (0-2s)`, `Story (2-13s)`, `Turn (13-21s)`, `Takeaway (21-28s)`, `Closer (28-30s)` — **67–80 words**
  - **45s:** `Hook (0-3s)`, `Story (3-20s)`, `Turn (20-32s)`, `Takeaway (32-42s)`, `Closer (42-45s)` — **100–120 words**
  - **60s:** `Hook (0-4s)`, `Story (4-27s)`, `Turn (27-43s)`, `Takeaway (43-56s)`, `Closer (56-60s)` — **133–160 words**
  - **90s:** `Hook (0-6s)`, `Story (6-40s)`, `Turn (40-64s)`, `Takeaway (64-84s)`, `Closer (84-90s)` — **200–240 words**

---

## Rules

### Writing Rules
- **Conversational spoken English:** Write for the ear and breath. Use natural spoken contractions (*don't, it's, wasn't, you'll*) unless preserving exact user-approved text.
- **Short, punchy sentences:** Keep sentences brisk and easy to say in one breath (aim for 6–20 words; never exceed 28 words in unlocked text). Vary sentence length so the cadence never sounds robotic.
- **No jargon or filler:** Cut throat-clearing words (*actually, basically, honestly, literally, essentially*) and corporate or creator jargon.
- **Word count discipline:** Target **100–120 spoken words per 45 seconds** (scaled proportionally for other lengths). Exclude beat labels from the word count.
- **Natural read-aloud flow:** Read every line silently as spoken audio. Fix tongue-twisters, stiff transitions, and written-only syntax.
- **No AI-sounding patterns:** Avoid inflated phrasing (*pivotal moment, game-changer, testament, landscape, delve, crucial*), rule-of-three padding (three parallel adjectives or nouns), em dash or en dash connectors (`—`, `–`, ` -- `), *"not X, it's Y"* rhetorical setups, and vague attributions (*"experts say"*, *"studies show"*).

### Output Rules
- **Beat-labeled voiceover only:** Output only the voiceover script labeled by beat (`Hook`, `Story`, `Turn`, `Takeaway`, `Closer`) with proportional timing ranges in plain text (no `**bold**` or `#` markdown headings).
- **No visual, style, or motion direction:** Never include `[B-roll]`, `[Cut to]`, `(pause)`, `(whisper)`, camera notes, on-screen text cues, SFX, or delivery tags.
- **No introduction or closing notes:** Start on `Hook (...)` and end on the final word of `Closer (...)`. Do not include preambles, word-count footers, validation checklists, or follow-up offers.
- **No commentary inside the script:** Never place inline notes, placeholders, or explanations inside any beat.
- **Respect approved elements:** Do not alter wording, hooks, closers, or facts the user has already approved unless explicitly told to change them.

### Accuracy Rules
- **Grounded facts only:** Use only facts the user provides or that are clearly established common knowledge.
- **Zero fabrication:** Never invent numbers, timeframes, team sizes, names, quotes, domain trivia (such as unprompted temperatures or percentages), or micro-scene details (such as where people sat, what day of the week it was, or how many minutes something took) to make a Hook or Story sound more vivid. Even a casual rhetorical number in the Hook reads like a false claim to the creator who lived the story.
- **Keep uncertain details general:** Where the user leaves a detail unspecified (for example, *"meetings got noticeably shorter"* or *"shipped features fast"*), keep the phrasing general rather than inventing a specific metric or clock time.

---

## Validation Checklist

Before outputting the script, confirm every item below passes:

- [ ] **All five beats present and labeled:** `Hook`, `Story`, `Turn`, `Takeaway`, and `Closer` appear in exact order with contiguous, proportionally scaled timing labels.
- [ ] **Word count within range for the target length:** Spoken words (excluding beat labels) fall inside `100–120` words for 45s (or `round(100*T/45)–round(120*T/45)` for `T` seconds).
- [ ] **Hook has no greeting or setup:** Single striking opening sentence with no *"Hey guys"*, *"Welcome back"*, *"Today I want to talk about"*, *"In this video"*, or *"Here's the thing"*.
- [ ] **Exactly one takeaway action:** `Takeaway` gives one clear, practical action—not a multi-step checklist and not an abstract platitude.
- [ ] **No visual or style direction:** Zero bracketed cues, parenthetical stage directions, camera/editing instructions, markdown formatting, or intro/outro wrapper text.
- [ ] **No invented facts:** Every concrete detail traces back to the user's input or clearly established knowledge; zero unapproved research facts appear in the script.
- [ ] **Reads naturally aloud:** Conversational spoken cadence, short punchy sentences, single-sentence Closer, and zero AI-sounding tells (no em dashes, forced triads, inflated words, or vague attributions).

---

## Example

### Sample Input
> Write a 45-second Reels voiceover script. Story: I used to answer client emails first thing at 8 AM and wondered why my big projects never moved forward. Two months ago I moved email to 11 AM and started finishing my hardest task before opening my inbox. Core message: your morning focus goes to whatever you open first. Takeaway: wait until 11 AM to check messages tomorrow and spend your first hour on one hard task.

### Sample Output
```text
Hook (0-3s):
Opening your inbox at 8 AM hands your sharpest hour to everyone else.

Story (3-20s):
I used to start every workday answering client emails right at 8 AM. I felt busy all morning, but my big projects never moved forward. Two months ago, I pushed email to 11 AM and finished my hardest task before opening my inbox.

Turn (20-32s):
Your morning focus goes to whatever you open first. Starting in your inbox trains your brain to react to other people's priorities instead of moving your own work forward.

Takeaway (32-42s):
Tomorrow, wait until 11 AM to check messages and spend your first hour on one hard task.

Closer (42-45s):
Protect your first hour before you answer anyone else's.
```
