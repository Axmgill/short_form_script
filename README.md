# short-form-script-writer-pro — Agent-Agnostic Short-Form Voiceover Skill

A model- and platform-agnostic skill that writes natural, spoken-English voiceover scripts for **Instagram Reels**, **TikTok**, and **YouTube Shorts**—packaged so **every app and agent** can run it (**Google Gemini**, **ChatGPT**, **Kimi**, **Claude**, **DeepSeek**, **Grok**, **Perplexity**, **Qwen**, **Codex**, **Cursor**, **GitHub Copilot**, **Windsurf**, and any API).

---

## Why It Works Across Every App

The entire workflow—complexity-based duration sizing (`30s` to `120s+`), optional 30-day discourse research, AI-tell humanization, and 7-point pre-output validation—lives in plain Markdown rather than relying on one vendor's proprietary runtime:

| Layer | File(s) | Read / Used By |
|---|---|---|
| **Universal Agent Standard** | [`AGENTS.md`](AGENTS.md) | Codex, Cursor, GitHub Copilot, Gemini CLI, Kimi CLI, Windsurf, OpenCode, Amp, Cline, Devin |
| **Native Skill Package** | [`SKILL.md`](SKILL.md), [`bundles/short-form-script-writer-pro.zip`](bundles/short-form-script-writer-pro.zip), [`short-form-script-writer-pro.skill`](short-form-script-writer-pro.skill) | **Gemini Skills** (unzip & upload folder), **Claude.ai / Cowork** (`.skill`), **Claude Code**, **Codex** |
| **Portable Paste Prompts** | [`portable/`](portable/README.md) | **Gemini Gems**, **ChatGPT** (Custom GPTs, Projects, Paid & Free Custom Instructions), **Kimi / Kimi+**, **Grok**, **DeepSeek**, **Perplexity**, **Qwen**, **APIs** |
| **Single-File Corpus** | [`llms-full.txt`](llms-full.txt), [`llms.txt`](llms.txt) | Drag-and-drop into **Kimi**, **ChatGPT**, **Gemini**, **Claude Projects**, or any RAG knowledge store |

`tools/build.sh` regenerates every bundle from source, and `tools/check.sh` verifies character limits, file links, Gemini upload rules, and rule parity across all surfaces.

---

## Install & Use in Every App

### Google Gemini (`gemini.google.com`)
- **Gemini Skills (recommended):** Download [`bundles/short-form-script-writer-pro.zip`](bundles/short-form-script-writer-pro.zip), **unzip it**, then go to `gemini.google.com` → **Customize** → **Skills** → **Create** → **Upload** → select the unzipped `short-form-script-writer-pro` folder.
- **Gemini Gems:** Paste [`portable/gemini-gem-instructions.md`](portable/gemini-gem-instructions.md) into *Gem Instructions* (and optionally upload [`llms-full.txt`](llms-full.txt) to *Knowledge*).
- **Plain Gemini Chat:** Paste [`portable/kickoff-prompt.md`](portable/kickoff-prompt.md) as your first message.

### ChatGPT (`chatgpt.com`)
- **Custom GPT / Projects:** Paste [`portable/system-prompt.md`](portable/system-prompt.md) into *Instructions*, upload [`llms-full.txt`](llms-full.txt) to *Knowledge / Project Files*, and keep *Web Search* enabled.
- **Custom Instructions:** Use [`portable/chatgpt-instructions.md`](portable/chatgpt-instructions.md) (Paid, `<5,000` chars) or [`portable/mini-prompt.md`](portable/mini-prompt.md) (Free tier, `<1,500` chars).
- **Plain Chat:** Paste [`portable/kickoff-prompt.md`](portable/kickoff-prompt.md) or attach [`llms-full.txt`](llms-full.txt).

### Kimi (`kimi.ai` / `kimi.moonshot.cn`)
- **Kimi+ Custom Assistant (`创建 Kimi+`):** Paste [`portable/kimi-instructions.md`](portable/kimi-instructions.md) into **Instructions (`设定`)**, upload [`llms-full.txt`](llms-full.txt) to **Knowledge (`知识库`)**, and keep **Web Search (`联网搜索`)** enabled.
- **Instant Kimi Chat (zero setup):** Drag and drop [`llms-full.txt`](llms-full.txt) straight into any Kimi chat and type your story/topic—or paste [`portable/kickoff-prompt.md`](portable/kickoff-prompt.md) on mobile/web.

### Claude (`claude.ai` / Cowork / Claude Code)
- **Claude.ai / Cowork:** Upload [`short-form-script-writer-pro.skill`](short-form-script-writer-pro.skill) under **Settings → Capabilities → Skills**.
- **Claude Projects:** Paste [`portable/system-prompt.md`](portable/system-prompt.md) into *Project Instructions* + attach [`llms-full.txt`](llms-full.txt).
- **Claude Code / `skills` CLI:**
  ```bash
  npx skills add Axmgill/short_form_script --skill short-form-script-writer-pro -g
  # or without Node.js:
  gh repo clone Axmgill/short_form_script ~/.claude/skills/short-form-script-writer-pro
  ```

### DeepSeek, Grok, Perplexity, Qwen & Mobile Chats
- **Spaces / Custom Assistants:** Paste [`portable/system-prompt.md`](portable/system-prompt.md) + attach [`llms-full.txt`](llms-full.txt).
- **Any Chat Window:** Paste [`portable/kickoff-prompt.md`](portable/kickoff-prompt.md) and put your topic at the bottom.

### Codex, Cursor, GitHub Copilot, Gemini CLI, Kimi CLI, Windsurf
- Clone this repo into your workspace—[`AGENTS.md`](AGENTS.md) at the root is picked up automatically.
- For global Cursor/Copilot rules, copy the block from [`portable/chatgpt-instructions.md`](portable/chatgpt-instructions.md) into `.cursor/rules/` or `.github/copilot-instructions.md`.

---

## Complexity-Based Duration Options

Instead of forcing every story into 45 seconds, the workflow selects the matching story-weighted duration tier when the user does not specify a length—keeping `Hook` (`2–4s`) and `Closer` (`2–5s`) as sharp single sentences while expanding `Story` and `Turn`:

| Tier | Complexity Fit | Beat Timings (`Hook / Story / Turn / Takeaway / Closer`) | Spoken Words |
|---|---|---|---|
| **30s — Quick Insight** | Single observation, fast myth-bust, or one-step tip | `0-2s / 2-13s / 13-21s / 21-28s / 28-30s` | **67–80** |
| **45s — Compact Anecdote** | Simple before-and-after habit shift | `0-3s / 3-20s / 20-32s / 32-42s / 42-45s` | **100–120** |
| **60s — Standard Story Arc** *(story default)* | Full story needing setup, friction, turning point, and payoff | `0-3s / 3-31s / 31-46s / 46-56s / 56-60s` | **133–160** |
| **75s — Extended Story** | Story arc with an extra complication or context bridge | `0-4s / 4-40s / 40-59s / 59-71s / 71-75s` | **167–200** |
| **90s — Layered Story & Nuanced Turn** | Multi-beat arc or counterintuitive concept needing reframing | `0-4s / 4-50s / 50-72s / 72-85s / 85-90s` | **200–240** |
| **120s — Deep Narrative / Case Breakdown** | Multi-scene story with escalating stakes or dense source facts | `0-4s / 4-68s / 68-98s / 98-115s / 115-120s` | **267–320** |

---

## Repository Layout & Maintenance

```text
.
├── AGENTS.md                                # Universal agent instructions (AGENTS.md standard)
├── SKILL.md                                 # Native skill entry point + worked 60s example
├── llms.txt / llms-full.txt                 # Machine-readable map & full single-file corpus
├── portable/                                # Paste-ready prompts for Gemini, ChatGPT, Kimi, etc.
│   ├── README.md
│   ├── system-prompt.md                     # Custom GPTs, Projects, APIs (<7,900 chars)
│   ├── gemini-gem-instructions.md           # Gemini Gems (<3,900 chars)
│   ├── kimi-instructions.md                 # Kimi+ Custom Assistants (<3,900 chars)
│   ├── chatgpt-instructions.md              # ChatGPT Paid / Cursor / Copilot (<4,900 chars)
│   ├── mini-prompt.md                       # ChatGPT Free & small persona boxes (<1,450 chars)
│   └── kickoff-prompt.md                    # Zero-setup first message for any chat
├── bundles/
│   └── short-form-script-writer-pro.zip     # Plain-text Gemini Skill / folder upload bundle
├── short-form-script-writer-pro.skill       # Claude.ai / Cowork .skill archive
├── references/
│   └── combined-skills-fallback.md          # Host-agnostic research/humanizer playbooks & 15s–180s tiers
├── scripts/
│   └── validate_script.py                   # Optional zero-dependency Python CLI validator
├── tools/
│   ├── build.sh                             # Rebuilds llms-full.txt, .zip bundle, and .skill
│   └── check.sh                             # Verifies budgets, links, sync, & validator checks
└── evals/                                   # Multi-tier test & refinement suite (30s–120s)
```

```bash
bash tools/build.sh   # regenerate llms-full.txt, bundles/*.zip, and *.skill
bash tools/check.sh   # verify all cross-agent budgets, bundles, and evals
```
