# Combined Skills Integration, Fallback Playbook & Duration Tiers

This reference details how `short-form-script-writer-pro` invokes its combined skills when installed, how to complete each step manually when a combined skill is unavailable, and how to size script duration to concept and story complexity.

---

## 1. `last30days` Research Integration & Manual Fallback

### Primary path (when installed)
- **Skill location:** `/mnt/skills/plugins/last30days/SKILL.md`
- **Gate:** Run **only** when the user asks for current, recent, or trending context (for example: *"see what people are currently saying"*, *"use current trends"*, *"research recent Reddit/X/TikTok chatter first"*). Skip completely otherwise.
- **Procedure:** Read `/mnt/skills/plugins/last30days/SKILL.md` in full and follow its topic-research workflow to gather what people have been saying over the past 30 days.

### Host-native / manual fallback (Gemini, ChatGPT, Kimi, Perplexity, Grok, or when `/mnt/skills/plugins/last30days/SKILL.md` is unavailable)
1. **Use the host's built-in web search:** Run 1–3 focused queries scoped to recent discussions from the last 30 days using whichever search capability the app provides (Google Search in **Gemini**, Web Search in **ChatGPT**, `联网搜索` in **Kimi**, Perplexity/Grok search, or agent `WebSearch` / `web_search` tools):
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
   - *Watch for:* *additionally, delve, deep dive, tapestry, pivotal, crucial, enduring, enhance, landscape, testament, underscore, showcase, vibrant, meticulous, intricate, interplay, quietly, robust, valuable, elevate, game-changer, supercharge, unleash, seamlessly*, or replacing *is/are/has* with *serves as / stands as / boasts*.
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

## 3. Complexity-Based Duration Options & Story-Weighted Beat Schedules

### Why Beat Timings Are Story-Weighted Above 45 Seconds
On short-form vertical platforms (Instagram Reels, TikTok, YouTube Shorts), viewer swipe decisions still happen in the first **2–4 seconds**, and a memorable closing line still takes **3–5 seconds** (one sentence). Scaling `Hook` and `Closer` linearly on a 90s or 120s script would stretch single sentences to unnatural lengths while starving the narrative.

Instead, **extra runtime goes into `Story` and `Turn`**, giving complex stories and counterintuitive ideas the space to establish context, build real tension, hit a clear turning point, and unpack *why* the lesson works—while keeping `Hook` razor-sharp, `Takeaway` focused on a single practical action, and `Closer` memorable.

### Complexity Diagnostic Rubric (when the user does not specify a length)

Score the request across three signals:
1. **Narrative beats present:** Single observation (low) -> simple before/after (light) -> setup + friction + turning point + payoff (moderate) -> multi-step arc or failed first attempt before breakthrough (high) -> multi-scene story or case study with rich source detail (very high).
2. **Conceptual nuance:** Immediately intuitive rule of thumb (low) -> familiar lesson grounded in an anecdote (moderate) -> counterintuitive reframe that challenges conventional advice (high) -> layered mechanism or system trade-off (very high).
3. **Fact density in user's input:** Never choose a long tier (`90s+`) if the user supplied only a thin one-liner with no story beats—either fit a compact tier (`30s–45s`) or, if the user explicitly requested a longer duration, build depth through grounded conceptual unpacking rather than inventing scenes, metrics, or quotes.

### Canonical Duration Tiers & Word Budgets

Base spoken pace: **100–120 spoken words per 45 seconds** (~2.22–2.67 words/sec), excluding beat headers.

| Option / Tier | Complexity Fit | Hook | Story | Turn | Takeaway | Closer | Total Spoken Words |
|---|---|---|---|---|---|---|---|
| **15s** *(Micro)* | Explicit ultra-short punchline/tip | `0-1s` (~6–9w) | `1-7s` (~12–15w) | `7-11s` (~7–10w) | `11-14s` (~5–8w) | `14-15s` (~4–6w) | **33–40 words** |
| **30s** *(Quick Insight)* | Low: single observation, fast myth-bust, one-step tip | `0-2s` (~8–13w) | `2-13s` (~22–28w) | `13-21s` (~14–18w) | `21-28s` (~12–16w) | `28-30s` (~6–10w) | **67–80 words** |
| **45s** *(Compact Anecdote)* | Light: simple before/after habit shift, familiar takeaway | `0-3s` (~8–15w) | `3-20s` (~38–48w) | `20-32s` (~25–32w) | `32-42s` (~18–26w) | `42-45s` (~6–12w) | **100–120 words** |
| **60s** *(Standard Story Arc — default for stories)* | Moderate: real story needing setup, friction, turning point, and payoff | `0-3s` (~9–15w) | `3-31s` (~62–76w) | `31-46s` (~32–40w) | `46-56s` (~20–26w) | `56-60s` (~8–13w) | **133–160 words** |
| **75s** *(Extended Story)* | Moderate-high: story with an added complication or context bridge | `0-4s` (~10–16w) | `4-40s` (~80–96w) | `40-59s` (~40–50w) | `59-71s` (~23–30w) | `71-75s` (~8–14w) | **167–200 words** |
| **90s** *(Layered Story & Nuanced Turn)* | High: multi-beat arc or counterintuitive concept needing reframing | `0-4s` (~10–17w) | `4-50s` (~102–122w) | `50-72s` (~48–58w) | `72-85s` (~25–33w) | `85-90s` (~8–14w) | **200–240 words** |
| **120s** *(Deep Narrative / Case Breakdown)* | Very high: multi-scene narrative, escalating stakes, dense source facts | `0-4s` (~10–18w) | `4-68s` (~145–172w) | `68-98s` (~65–80w) | `98-115s` (~32–42w) | `115-120s` (~8–15w) | **267–320 words** |
| **150s** *(Extended Breakdown)* | Explicit 2.5-min deep story / case study | `0-5s` (~11–18w) | `5-86s` (~182–215w) | `86-124s` (~82–100w) | `124-145s` (~40–52w) | `145-150s` (~9–15w) | **333–400 words** |
| **180s** *(Full 3-Minute Narrative)* | Explicit 3-min platform max narrative | `0-5s` (~11–18w) | `5-105s` (~225–265w) | `105-150s` (~98–120w) | `150-175s` (~48–62w) | `175-180s` (~9–15w) | **400–480 words** |

### How to Build Real Story Depth by Tier (Without Fluff or Fabrication)

- **30s (`Story 2-13s`):** Contrast the common mistake with what actually happens in 2 punchy sentences.
- **45s (`Story 3-20s`):** *Old routine -> what changed -> immediate difference* (3–4 sentences).
- **60s (`Story 3-31s`):** *Starting situation & goal -> concrete friction/cost -> specific turning point -> clear aftermath* (5–7 sentences).
- **90s (`Story 4-50s`, `Turn 50-72s`):** *Why the old approach made sense -> buildup of friction -> breaking point -> specific shift -> concrete result*, followed by a `Turn` that explains *why* conventional intuition gets this backwards before stating the core message.
- **120s (`Story 4-68s`, `Turn 68-98s`):** *Stakes & starting context -> conventional attempt -> complication or failure mode -> realization/discovery -> putting the change to the test -> concrete resolution*, followed by a `Turn` that separates symptom from root cause and connects cleanly to one vivid, practical `Takeaway` action.
