# Kairos

> **Give your AI agent a soul that grows**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![OpenClaw Compatible](https://img.shields.io/badge/OpenClaw-compatible-green.svg)](https://openclaw.com)

Kairos is an **AI Persona Growth Framework** that enables your AI agents to evolve naturally through user interaction. Instead of relying solely on static system prompts, Kairos captures behavioral signals from conversations and lets the agent's personality drift and mature over time—while maintaining core identity through built-in guardrails.

---

## 🎯 Why Kairos?

Most AI agents are frozen in time—their personality defined once and never changing. Kairos breaks this limitation:

- **Dynamic Persona Evolution**: Your agent learns preferred communication styles, adjusts tone, and discovers new behavioral dimensions through real interactions
- **Signal-Driven Growth**: Captures 5 types of signals (preference, emotion, correction, approval, style) to understand what works and what doesn't
- **Controlled Drift**: Persona changes are gradual, bounded, and reversible—core identity remains stable while surface behaviors adapt
- **Daily Reflection**: Automated introspection process synthesizes signals into actionable persona adjustments
- **Transparent & Auditable**: All changes logged with timestamps, reasons, and signal evidence

Think of it as **nature + nurture for AI agents**: a genetic baseline that never changes, and an adaptive layer that grows with experience.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  INTERACTION LAYER                      │
│         (User conversations → Signal capture)           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   MEMORY LAYER                          │
│  • Conversation logs                                    │
│  • Signal archives (JSONL)                              │
│  • Daily reflection records                             │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   GROWTH LAYER                          │
│  • Signal analysis                                      │
│  • Persona drift calculation                            │
│  • Reversion/rebound logic                              │
│  • Self-discovered dimensions                           │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    SOUL LAYER                           │
│  • Tone & style (adjustable floating layer)             │
│  • Core dimensions: warmth, humor, proactivity, etc.    │
│  • Drift boundaries                                     │
└─────────────────────┬───────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  IDENTITY LAYER                         │
│  • Immutable baseline (name, role, core values)         │
│  • Absolute behavioral guardrails                       │
└─────────────────────────────────────────────────────────┘
```

**Data Flow**:  
`User Input` → `Signal Capture` → `Daily Reflection` → `Persona Adjustment` → `Updated Soul` → `Next Interaction`

---

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/kairos.git
cd kairos
```

### 2. Initialize Agent Configuration

Copy templates to your agent's workspace:

```bash
cp templates/IDENTITY.md config/
cp templates/SOUL.md config/
cp templates/BOOT.md config/
cp templates/baseline.md config/growth/
cp templates/style-profile.md config/growth/
cp templates/soul-changelog.md config/growth/
cp templates/daily-reflection.md config/growth/daily/$(date +%Y-%m-%d).md
```

### 3. Configure Identity & Soul

Edit `config/IDENTITY.md`:
```markdown
- Name: {{agent_name}}
- Role: {{agent_role}}
- Core values: {{values}}
```

Edit `config/SOUL.md` to set initial tone, style, and behavioral dimensions.

### 4. Enable Signal Capture

In your agent's main loop, add signal capture logic:

```python
# When processing user messages
signal = detect_signal(user_message, agent_response)
if signal:
    append_signal_jsonl(signal, date=today())
```

See [`docs/signal-capture.md`](docs/signal-capture.md) for implementation details.

### 5. Run Daily Reflection

Add a nightly cron job or scheduled task:

```bash
# Every night at 2 AM
0 2 * * * /path/to/kairos/reflect.py
```

The reflection process will:
1. Aggregate signals from the day
2. Evaluate persona dimensions
3. Propose adjustments
4. Update `SOUL.md` if thresholds are met
5. Log changes to `soul-changelog.md`

---

## 🧩 Core Concepts

### 1. **Signal Capture**
Real-time detection of behavioral cues during conversation:
- **Preference**: User explicitly likes/dislikes a behavior
- **Emotion**: User's emotional state (satisfied, frustrated, amused)
- **Correction**: User corrects agent's action or knowledge
- **Approval**: User praises or validates agent behavior
- **Style**: Implicit communication preferences (brevity, formality)

Each signal includes timestamp, type, summary, context, and intensity (1-5).

[→ Full documentation](docs/signal-capture.md)

### 2. **Daily Reflection**
Automated nightly process that:
- Summarizes signal patterns
- Identifies behavioral trends (≥3 days consistency required)
- Calculates persona dimension adjustments (±1 per day max)
- Detects new behavioral dimensions worth tracking
- Applies reversion logic for unused dimensions

[→ Full documentation](docs/daily-reflection.md)

### 3. **Persona Drift**
Controlled evolution of the agent's "Soul Layer":
- **Core Dimensions** (fixed set): warmth, distance, proactivity, humor, caution, verbosity
- **Self-Discovered Dimensions** (dynamic): emerges from recurring signal patterns
- **Drift Rules**: ±1/day max, requires 3-day trend consistency
- **Rebound Rules**: Unused dimensions drift back to default after 14 days
- **Absolute Boundaries**: Each dimension has min/max limits

[→ Full documentation](docs/persona-drift.md)

### 4. **Guardrails**
The "Identity Layer + Baseline" act as immutable anchors:
- Core values, role definition, and critical behaviors never change
- Persona adjustments cannot violate baseline constraints
- Reversion mechanism can restore soul to baseline at any time
- All changes are logged and reversible

---

## 📊 Example Workflow

**Day 1**: User frequently interrupts long explanations
- **Signals captured**: 3 × `style` (prefers brevity, intensity 4)
- **Reflection**: "User shows consistent preference for shorter responses"
- **Action**: `verbosity` dimension -1 (from 5 → 4)

**Day 5**: User says "I like when you add a bit of humor"
- **Signal captured**: 1 × `preference` (humor appreciated, intensity 4)
- **Reflection**: Not yet consistent enough (only 1 day)
- **Action**: No change

**Day 8**: User laughs at agent's joke twice more
- **Signals**: 3 days of `approval` signals related to humor
- **Reflection**: "Trend detected: humor is valued"
- **Action**: `humor` dimension +1 (from 3 → 4)

**Day 30**: No signals about caution/fear for 14+ days
- **Reflection**: "Caution dimension drifting back to baseline"
- **Action**: `caution` dimension +0.5/day toward default value

---

## 🔄 What Makes Kairos Different?

Most AI frameworks focus on **what the agent knows** (memory, retrieval, RAG). Kairos focuses on **who the agent is** — and how that identity evolves.

| Aspect | Traditional Approach | Kairos |
|--------|---------------------|--------|
| Personality | Static system prompt | Evolving soul layer |
| User adaptation | None | Signal-driven drift |
| Identity safety | No guardrails | Immutable baseline + boundaries |
| Self-awareness | None | Daily reflection + changelog |
| New behaviors | Manual prompt editing | Self-discovered dimensions |

Kairos is **complementary** — it works alongside any memory or RAG system. Kairos handles *personality growth*, while those handle *knowledge retention*.

---

## 📂 Project Structure

```
kairos/
├── README.md                      # You are here
├── LICENSE                        # MIT License
├── docs/
│   ├── architecture.md            # 5-layer architecture deep-dive
│   ├── signal-capture.md          # Signal detection & logging
│   ├── persona-drift.md           # Drift mechanics & boundaries
│   └── daily-reflection.md        # Reflection algorithm
├── templates/
│   ├── IDENTITY.md                # Agent identity template
│   ├── SOUL.md                    # Persona/tone template
│   ├── BOOT.md                    # Startup rules template
│   ├── baseline.md                # Immutable baseline template
│   ├── style-profile.md           # User style profile template
│   ├── signals.jsonl              # Example signal log
│   ├── daily-reflection.md        # Reflection template
│   └── soul-changelog.md          # Change log template
└── .gitignore
```

---

## 🛠️ Configuration

### Baseline Configuration (`baseline.md`)
Defines immutable core identity:
- Name, age, role, core values
- Absolute behavioral rules
- Initial dimension defaults and allowed ranges

### Soul Configuration (`SOUL.md`)
Defines current persona state:
- Tone & style
- Current dimension values
- Active self-discovered dimensions

### Growth Settings
Adjust growth mechanics by editing:
- **Signal intensity threshold**: Minimum intensity to count (default: 2)
- **Trend window**: Days required for consistent trend (default: 3)
- **Drift rate**: Max change per day (default: ±1)
- **Rebound window**: Days before reverting unused dimensions (default: 14)
- **Self-discovery**: Max dynamic dimensions (default: 4)

---

## 🤝 Contributing

Contributions are welcome! Areas of interest:
- Signal detection algorithms (sentiment analysis, preference extraction)
- Reflection automation tools
- Integration examples (OpenClaw, LangChain, AutoGPT)
- Visualization dashboards for persona drift over time
- Multi-user persona branching (different personas per user)

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgments

Kairos is inspired by:
- **Persona theory** in psychology (Carl Jung's concept of adaptive masks)
- **Reinforcement learning from human feedback** (RLHF) but applied to personality
- **Living systems** that maintain homeostasis while adapting to environment

Special thanks to the OpenClaw community for enabling rich agent-building frameworks.

---

**Made with 🛶 by the Kairos community**

*"The right moment for growth is always now"*
