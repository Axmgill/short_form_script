# Combined Skills Integration & Fallback Playbook

This reference details how `short-form-script-writer-pro` invokes its combined skills when installed and how to complete each step manually when a combined skill is unavailable.

---

## 1. `last30days` Research Integration & Manual Fallback

### Primary path (when installed)
- **Skill location:** `/mnt/skills/plugins/last30days/SKILL.md`
- **Gate:** Run **only** when the user asks for current, recent, or trending context (for example: *"see what people are currently saying"*, *"use current trends"*, *"research recent Reddit/X/TikTok chatter first"*). Skip completely otherwise.
- **Procedure:** Read `/mnt/skills/plugins/last30days/SKILL.md` in full and follow its topic-research workflow to gather what people have been saying over the past 30 days.

### Manual fallback (when `/mnt/skills/plugins/last30days/SKILL.md` is unavailable or cannot run)
1. **Check available search tools:** If the host provides web search (`WebSearch`, `web_search`, or connector search), run 1–3 focused queries scoped to recent discussions from the last 30 days:
   - Common complaints, pushback, or frustrations people voice about the topic
   - Everyday phrases, comparisons, or tension points recurring in threads and comments
   - Contrarian angles versus tired conventional advice
2. **Offline / no-search host:** If no search tool exists either, identify the sharpest tension already implicit in the user's request without fabricating recent trends or claims.

### Strict usage boundary (applies to BOTH primary and fallback paths)
- **Sharpen only the Hook and angle:** Use research findings solely to frame the opening tension (`Hook`) and the perspective of the `Turn`.
- **Never inject unapproved research facts:** Do **not** add statistics, study citations, dates, named people/companies, quotes, or factual claims discovered during research into the voiceover script unless the user explicitly approves them first.
- **Keep research invisible in final output:** Never include a research summary, citations, or notes before or after the script unless the user explicitly asked to review candidate facts prior to scripting.

---

## 2. `humanizer` Rewrite Integration & Manual Fallback

### Primary path (when installed)
- **Skill location:** `/mnt/skills/plugins/humanizer/SKILL.md`
- **Gate:** Run on **every** draft in Step 4.
- **Procedure:** Read `/mnt/skills/plugins/humanizer/SKILL.md` and run its rewrite workflow in **embedded mode** (returning only cleaned text) while preserving:
  - the 5-beat structure and beat labels,
  - the target word-count window, and
  - any wording or facts the user has already approved.

### Manual fallback (when `/mnt/skills/plugins/humanizer/SKILL.md` is unavailable)
Read the draft aloud beat by beat and strip every AI-writing tell below (derived from Wikipedia's *"Signs of AI writing"* and the `humanizer` pattern set):

1. **Staging contrasts ("Not X, but Y"):**
   - *Watch for:* *"It's not about willpower, it's about systems."*, *"This isn't X. It's Y."*, *"not merely X, but Y."*
   - *Fix:* Cut the invented negative half and state the actual point directly, unless correcting a specific belief central to the user's story.
2. **Staged run-ups and fake candor:**
   - *Watch for:* *"Here's the thing"*, *"Let's be honest"*, *"Real talk"*, *"Let's dive in"*, *"Here's what nobody tells you"*.
   - *Fix:* Delete the run-up and start on the concrete claim.
3. **Hollow one-line closers and dramatic fragments:**
   - *Watch for:* *"Read that again."*, *"Let that sink in."*, *"Full stop."*, *"Period."*, *"every. single. day."*, or rows of choppy verbless fragments.
   - *Fix:* Write a real spoken sentence that lands a memorable thought tied to the story.
4. **Rule-of-three padding (forced triads):**
   - *Watch for:* Three near-synonymous adjectives, three parallel mini-examples, or three abstract nouns (*"clarity, focus, and momentum"*).
   - *Fix:* Keep the single sharpest concrete word or two genuinely distinct points.
5. **Dash connectors:**
   - *Watch for:* Em dashes (`—`), en dashes (`–`), or spaced double hyphens (` -- `) stitching clauses together.
   - *Fix:* Replace with a period, a comma, or two crisp spoken sentences (leave user-locked wording untouched).
6. **Inflated phrasing and stock AI vocabulary:**
   - *Watch for:* *delve, tapestry, pivotal, crucial, landscape, testament, underscore, showcase, vibrant, meticulous, intricate, interplay, game-changer, supercharge, unleash, elevate, seamlessly*, or replacing *is/are/has* with *serves as / stands as / boasts*.
   - *Fix:* Use everyday spoken words and plain verbs (*is, are, has, did, quit, kept, built*).
7. **Vague attributions and borrowed authority:**
   - *Watch for:* *"Experts say"*, *"Studies show"*, *"Industry leaders agree"*, *"Research proves"*.
   - *Fix:* Delete unnamed authorities; rely only on the user's story or direct plain statements.
8. **Shallow `-ing` riders:**
   - *Watch for:* Participial tails bolted onto facts (*"...highlighting why focus matters"*, *"...ensuring better outcomes"*).
   - *Fix:* Cut the tail or state the real cause-and-effect in its own short sentence.
9. **Spoken cadence check:**
   - Use natural contractions (*don't, it's, you'll, wasn't, couldn't*) unless they clash with user-approved phrasing.
   - Vary sentence lengths so three identical-length sentences never stack robotically.
   - Keep sentences comfortable to speak in a single breath (aim for 6–20 words; never over 28 words).

---

## 3. Proportional Timing & Spoken Word-Count Reference Table

Base rate: **100–120 spoken words per 45 seconds** (~2.22–2.67 words/sec), excluding beat headers.

Beat proportions of total duration `T`:
- `Hook`: `0` to `round(3 * T / 45)` (~6.7%) — 1 sentence
- `Story`: `round(3 * T / 45)` to `round(20 * T / 45)` (~37.8%)
- `Turn`: `round(20 * T / 45)` to `round(32 * T / 45)` (~26.7%)
- `Takeaway`: `round(32 * T / 45)` to `round(42 * T / 45)` (~22.2%) — 1 practical action
- `Closer`: `round(42 * T / 45)` to `T` (~6.7%) — 1 sentence

| Target Length | Hook | Story | Turn | Takeaway | Closer | Total Spoken Words |
|---|---|---|---|---|---|---|
| **15s** | `0-1s` | `1-7s` | `7-11s` | `11-14s` | `14-15s` | **33–40 words** |
| **30s** | `0-2s` | `2-13s` | `13-21s` | `21-28s` | `28-30s` | **67–80 words** |
| **45s (default)** | `0-3s` | `3-20s` | `20-32s` | `32-42s` | `42-45s` | **100–120 words** |
| **60s** | `0-4s` | `4-27s` | `27-43s` | `43-56s` | `56-60s` | **133–160 words** |
| **75s** | `0-5s` | `5-33s` | `33-53s` | `53-70s` | `70-75s` | **167–200 words** |
| **90s** | `0-6s` | `6-40s` | `40-64s` | `64-84s` | `84-90s` | **200–240 words** |
