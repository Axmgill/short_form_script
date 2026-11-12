# Portable Mode — Use `short-form-script-writer-pro` in Every App

`SKILL.md` and `AGENTS.md` work automatically in agents that read local folders (Google Antigravity, Claude Code, Codex, Cursor, Gemini CLI, Kimi CLI, GitHub Copilot, Windsurf, OpenCode). **Portable mode exists for every app that does not**—**Gemini** on the web/mobile, **ChatGPT**, **Kimi** (`kimi.ai` / `kimi.moonshot.cn`), **Claude Projects**, **DeepSeek**, **Grok**, **Perplexity**, **Qwen**, or any LLM API.

Every portable file carries the **exact same self-contained workflow**—complexity-based duration options (`30s` to `120s+`), optional 30-day research via the host's built-in web search, AI-tell humanization, and the 7-point pre-output check—with **zero repository or Python dependency**.

---

## Pick the Right File for Your App

| App / Surface | File to Use | Field Limit |
|---|---|---|
| **Google Antigravity (App / IDE / CLI)** | Workspace: [`.agents/skills/short-form-script-writer-pro/`](../.agents/skills/short-form-script-writer-pro/); global: [`../bundles/antigravity/short-form-script-writer-pro.zip`](../bundles/antigravity/short-form-script-writer-pro.zip) | Native `SKILL.md` |
| **Gemini Skills (web)** | Unzip [`../bundles/short-form-script-writer-pro.zip`](../bundles/short-form-script-writer-pro.zip) → upload folder | 100 MB / 1,024-char desc |
| **Gemini Gems (web)** | [`gemini-gem-instructions.md`](gemini-gem-instructions.md) | ~4,000 chars |
| **ChatGPT — Custom GPT / Projects** | [`system-prompt.md`](system-prompt.md) *(+ `../llms-full.txt` as Knowledge)* | 8,000 chars |
| **ChatGPT — Custom Instructions (Paid)** | [`chatgpt-instructions.md`](chatgpt-instructions.md) | 5,000 chars |
| **ChatGPT — Custom Instructions (Free)** | [`mini-prompt.md`](mini-prompt.md) | 1,500 chars |
| **Kimi — Kimi+ Custom Assistant (`创建 Kimi+`)** | [`kimi-instructions.md`](kimi-instructions.md) *(+ `../llms-full.txt` in `知识库`)* | ~4,000 chars |
| **Kimi — Any Chat (file drop)** | Drag & drop [`../llms-full.txt`](../llms-full.txt) into the chat | Long context |
| **Claude.ai / Cowork** | Upload [`../short-form-script-writer-pro.skill`](../short-form-script-writer-pro.skill) *(or `system-prompt.md` in Projects)* | Native `.skill` |
| **DeepSeek / Grok / Perplexity / Qwen / Mobile Chats** | [`kickoff-prompt.md`](kickoff-prompt.md) *(or attach `../llms-full.txt`)* | Pasted per chat |
| **Cursor / GitHub Copilot / Windsurf rules** | [`chatgpt-instructions.md`](chatgpt-instructions.md) | No fixed cap |
| **Any API** (OpenAI, Gemini, Anthropic, Moonshot/Kimi, xAI, OpenRouter) | [`system-prompt.md`](system-prompt.md) | System message |

Each file in `portable/` contains **one fenced code block**. Copy **only the text inside the block**—the notes above the block are setup instructions for you.

---

## Quick Setup by App

### Google Antigravity (App / IDE / CLI)
- **Workspace:** This repository already includes `.agents/skills/short-form-script-writer-pro/`; open the repository root and Antigravity will discover the skill.
- **Install from the bundle:** Extract [`../bundles/antigravity/short-form-script-writer-pro.zip`](../bundles/antigravity/short-form-script-writer-pro.zip) into `<workspace>/.agents/skills/` for one project or `~/.gemini/config/skills/` for all projects.
- **Use it:** Antigravity selects it automatically for a matching script-writing task. Use `/short-form-script-writer-pro` where slash commands are supported. In the CLI, run `/skills reload` after adding it to an active session; in the App/IDE, check **Customizations** or start a new conversation.
- See [Google's Antigravity skill documentation](https://antigravity.google/docs/skills) for current locations and discovery behavior.

### 1. Google Gemini (`gemini.google.com`)
- **Recommended — Gemini Skills:**
  1. Download [`bundles/short-form-script-writer-pro.zip`](../bundles/short-form-script-writer-pro.zip) and **unzip it** so you have the `short-form-script-writer-pro/` folder.
  2. Open `gemini.google.com` → **Customize** → **Skills** → **Create** → **Upload**.
  3. Select the unzipped `short-form-script-writer-pro` folder and click **Create**.
- **Alternative — Gemini Gem:**
  - Go to **Gems → New Gem**, paste the block from [`gemini-gem-instructions.md`](gemini-gem-instructions.md) into **Instructions**, and optionally upload [`llms-full.txt`](../llms-full.txt) under **Knowledge**. Gemini automatically uses Google Search when you ask for current chatter.
- **No setup (plain chat):** Paste [`kickoff-prompt.md`](kickoff-prompt.md) as your first message.

### 2. ChatGPT (`chatgpt.com`)
- **Custom GPT (best reusable setup):**
  - **My GPTs → Create a GPT → Configure**: paste [`system-prompt.md`](system-prompt.md) into **Instructions**, upload [`llms-full.txt`](../llms-full.txt) into **Knowledge**, and leave **Web Search** checked.
- **ChatGPT Projects:**
  - Paste [`system-prompt.md`](system-prompt.md) into **Project Instructions** and add [`llms-full.txt`](../llms-full.txt) to **Project Files**.
- **Custom Instructions:**
  - Paid accounts: [`chatgpt-instructions.md`](chatgpt-instructions.md). Free accounts: [`mini-prompt.md`](mini-prompt.md).

### 3. Kimi (`kimi.ai` / `kimi.moonshot.cn`)
- **Kimi+ Custom Assistant (`创建 Kimi+`):**
  1. Create a new Kimi+ assistant.
  2. Paste the block from [`kimi-instructions.md`](kimi-instructions.md) into **Instructions / Prompt (`设定`)**.
  3. Upload [`llms-full.txt`](../llms-full.txt) under **Knowledge (`知识库`)** and leave **Web Search (`联网搜索`)** switched **On**.
- **Instant Chat (zero setup):**
  - Drop [`llms-full.txt`](../llms-full.txt) straight into any Kimi chat window and write your topic/story, **or** paste [`kickoff-prompt.md`](kickoff-prompt.md) on mobile/web.

### 4. Claude (`claude.ai` / Desktop / Claude Code)
- **Skills:** Upload [`short-form-script-writer-pro.skill`](../short-form-script-writer-pro.skill) in **Settings → Capabilities → Skills**.
- **Claude Projects:** Paste [`system-prompt.md`](system-prompt.md) into **Project Instructions** and add [`llms-full.txt`](../llms-full.txt) to **Project Knowledge**.

### 5. Grok, Perplexity, DeepSeek, Qwen & Other Chat Apps
- **Spaces / Custom Assistants** (Perplexity Spaces, Grok Workspaces, Qwen Agents): Paste [`system-prompt.md`](system-prompt.md) into the custom instructions field and attach [`llms-full.txt`](../llms-full.txt).
- **Any single chat:** Paste [`kickoff-prompt.md`](kickoff-prompt.md) with your request at the bottom.

---

## Keeping Every Surface in Sync

Run `tools/build.sh` after editing `SKILL.md`, `AGENTS.md`, `references/`, or `portable/`, then run `tools/check.sh` to verify character budgets, file references, bundle freshness, and guardrail parity across all surfaces.
