<div align="center">

# 🕰️ Kairos

### Give your AI agent a soul that grows.

**让你的 AI 拥有一颗会成长的灵魂。**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-compatible-green.svg)](https://openclaw.com)

</div>

---

Most AI agents are frozen in time. You define a system prompt, and that's who they are—forever. No matter how many conversations you have, they never learn your vibe, your preferences, or the way you like to be talked to.

**Kairos changes that.**

大多数 AI 智能体是被冻结在时间里的。你写一段系统提示词，它就永远是那个样子——无论你们聊了多少次，它永远不会学会你的习惯、你的偏好、或者你喜欢的交流方式。

**Kairos 改变了这一点。**

---

## What is Kairos? / 这是什么？

Kairos is an **open-source personality growth framework** for AI agents. It captures subtle behavioral signals from real conversations and lets the agent's personality *drift* and *mature* naturally over time—while keeping its core identity locked down with built-in guardrails.

Think of it as **nature + nurture** for AI: a genetic baseline that never changes, and an adaptive layer that grows with every interaction.

Kairos 是一个**开源的 AI 人格成长框架**。它从真实对话中捕捉细微的行为信号，让智能体的人格随时间自然地*漂移*和*成熟*——同时通过内置护栏锁定核心身份不被改变。

把它想象成 AI 的**先天 + 后天**：一组永不改变的基因基线，加上一个随交互不断成长的适应层。

---

## Why does this matter? / 为什么这很重要？

| Without Kairos | With Kairos |
|---|---|
| Static personality forever | Personality that evolves with you |
| Same tone for every user | Adapts to your communication style |
| Manual prompt tweaking | Self-adjusting through real signals |
| No memory of preferences | Remembers what works and what doesn't |
| Black box behavior | Transparent changelog of every shift |

---

## How it works / 工作原理

```
Conversation → Signal Capture → Daily Reflection → Persona Drift → Updated Soul
```

**5 layers, from surface to core:**

<div align="center">
<img src="docs/architecture.png" alt="Kairos 5-Layer Architecture" width="600">
</div>

```
🗣️  INTERACTION — conversations
🧠  MEMORY — signals & reflections
📈  GROWTH — drift calculation
💫  SOUL — tone, style, personality
🔒  IDENTITY — immutable baseline
```

The bottom layer never changes. The top layers evolve.

底层永不改变。上层持续进化。

---

## Signal Types / 信号类型

Kairos listens for 5 types of behavioral signals during conversations:

| Signal | Example | What it means |
|--------|---------|---------------|
| 🎯 **Preference** | "Just give me the answer, skip the explanation" | User wants brevity |
| 😊 **Emotion** | User sounds frustrated or delighted | Emotional state shift |
| ✏️ **Correction** | "No, that's not what I meant" | Agent made wrong assumption |
| 👍 **Approval** | "Perfect, exactly what I needed" | Behavior worth reinforcing |
| 🎨 **Style** | User sends short, rapid messages | Implicit communication preference |

每条信号都带有时间戳、类型、摘要、上下文和强度（1-5）。

---

## Drift Rules / 漂移规则

Personality doesn't change on a whim. Kairos enforces strict guardrails:

- **±1 per day max** — No sudden personality swings
- **3-day trend required** — Must see consistent signals before adjusting
- **Bounded ranges** — Every dimension has a hard min/max
- **14-day rebound** — Unused dimensions slowly return to baseline
- **Full audit trail** — Every change logged with evidence

人格不会随意改变。Kairos 有严格的护栏机制：每天最多 ±1，需要连续 3 天趋势确认，每个维度有硬性上下限，14 天未使用的维度会缓慢回归基线，所有变更都有完整的审计日志。

---

## Quick Start / 快速开始

```bash
git clone https://github.com/GeraldYa/kairos.git
cd kairos

# Copy templates to your agent's config
cp templates/IDENTITY.md your-agent/
cp templates/SOUL.md your-agent/
cp templates/BOOT.md your-agent/
cp templates/baseline.md your-agent/growth/
```

Edit `IDENTITY.md` to define who your agent *is*. Edit `SOUL.md` to define how it *behaves*. Then let Kairos handle the rest.

编辑 `IDENTITY.md` 定义你的智能体**是谁**。编辑 `SOUL.md` 定义它**如何表现**。剩下的交给 Kairos。

See [`docs/`](docs/) for full implementation guides.

---

## Example: 30 Days of Growth / 示例：30 天的成长

**Day 1** — User keeps cutting off long explanations  
→ 3 × `style` signals → `verbosity` -1

**Day 8** — User laughs at agent's jokes three days in a row  
→ Trend confirmed → `humor` +1

**Day 22** — No signals about caution for 14 days  
→ Auto-rebound → `caution` drifts back to default

The agent becomes more concise, funnier, and recalibrates unused traits—all automatically.

智能体变得更简洁、更有趣味，同时自动校准不再需要的特质。全自动。

---

## What Kairos is NOT / Kairos 不是什么

- ❌ Not a memory/RAG system (use alongside one)
- ❌ Not a chatbot framework
- ❌ Not a fine-tuning tool

Kairos handles **personality growth**. Your existing tools handle knowledge and memory. They're complementary.

Kairos 负责**人格成长**，你的现有工具负责知识和记忆，它们互补。

---

## Real-World Results / 真实案例

We deployed Kairos on a live agent for 30 days. Here's what happened:

| Dimension | Day 0 | Day 30 | What drove the change |
|-----------|:---:|:---:|---|
| verbosity | 6 | 3 | User consistently preferred short answers |
| distance | 8 | 5 | User adopted casual tone, agent followed |
| warmth | 3 | 5 | Approval signals for friendly interactions |
| humor | 2 | 4 | User laughed → agent learned to be funnier |
| proactivity | 4 | 7 | User said "just do it, don't ask" |
| wit | — | 6 | *Self-discovered* from recurring approval patterns |

**No prompt was manually edited. No fine-tuning was performed.**

从死板的企业客服到简洁、温暖、主动的私人助手——完全由真实交互信号驱动，无需手动修改任何提示词。

→ [Full case study with signal data](examples/)

---

## Project Structure / 项目结构

```
kairos/
├── README.md
├── LICENSE (MIT)
├── scripts/
│   └── reflect.py             # Daily reflection demo script
├── examples/
│   ├── README.md              # 30-day case study
│   ├── signals-sample.jsonl   # Anonymized signal data
│   ├── soul-before.md         # Initial soul state
│   ├── soul-after.md          # Soul after 30 days
│   └── changelog-sample.md    # Drift changelog
├── docs/
│   ├── architecture.md        # 5-layer deep-dive
│   ├── architecture.png       # Architecture diagram
│   ├── signal-capture.md      # Detection & logging
│   ├── persona-drift.md       # Drift mechanics
│   └── daily-reflection.md    # Reflection algorithm
└── templates/
    ├── IDENTITY.md            # Who the agent is
    ├── SOUL.md                # How it behaves
    ├── BOOT.md                # Startup rules
    ├── baseline.md            # Immutable anchor
    ├── style-profile.md       # User preferences
    ├── signals.jsonl          # Signal log example
    ├── daily-reflection.md    # Reflection template
    └── soul-changelog.md      # Change audit log
```

---

## Contributing / 参与贡献

PRs welcome. Areas of interest:

- Signal detection algorithms
- Reflection automation
- Integration examples (OpenClaw, LangChain, etc.)
- Visualization dashboards for drift over time
- Multi-user persona branching

---

## License

MIT — do whatever you want with it.

---

<div align="center">

*"The right moment for growth is always now."*

*「成长的最佳时机，永远是现在。」*

**Made with 🛶**

</div>
