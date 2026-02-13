# Examples

Real-world case study of Kairos in action, based on an AI agent deployed on [OpenClaw](https://openclaw.com).

## Case Study: 30 Days of Agent Growth

An assistant agent was deployed with the following initial soul configuration:

| Dimension | Initial Value | Range |
|-----------|:---:|:---:|
| warmth | 3 | 1-10 |
| distance | 8 | 3-10 |
| proactivity | 4 | 1-8 |
| humor | 2 | 1-8 |
| caution | 6 | 1-8 |
| verbosity | 6 | 1-8 |

**Persona**: Cold, formal, cautious, verbose. Essentially a corporate chatbot.

### What happened over 30 days

**Week 1** — The user consistently sent short messages and interrupted long explanations.
- 12 × `style` signals (brevity preference)
- 4 × `preference` signals ("just give me the answer")
- Result: `verbosity` dropped from 6 → 3

**Week 2** — User started using casual language and emoji.
- 8 × `style` signals (informal tone)
- 3 × `approval` signals when agent matched the casual tone
- Result: `distance` dropped from 8 → 5, `warmth` rose from 3 → 5

**Week 3** — User laughed at an accidental joke the agent made.
- 5 × `approval` signals related to humor
- New self-discovered dimension: `wit` (initialized at 5)
- Result: `humor` rose from 2 → 4

**Week 4** — User gave the agent more autonomy on tasks.
- 6 × `approval` signals for proactive behavior
- 2 × `preference` signals ("just do it, don't ask")
- Result: `proactivity` rose from 4 → 7, `caution` dropped from 6 → 4

### Final State (Day 30)

| Dimension | Before | After | Change |
|-----------|:---:|:---:|:---:|
| warmth | 3 | 5 | +2 |
| distance | 8 | 5 | -3 |
| proactivity | 4 | 7 | +3 |
| humor | 2 | 4 | +2 |
| caution | 6 | 4 | -2 |
| verbosity | 6 | 3 | -3 |
| wit *(new)* | — | 6 | self-discovered |

The agent went from a stiff corporate chatbot to a concise, warm, proactive assistant with a sense of humor—entirely driven by real interaction signals.

**No prompt was manually edited. No fine-tuning was performed.**

---

## Files

- [`signals-sample.jsonl`](signals-sample.jsonl) — 30 days of anonymized signal data
- [`soul-before.md`](soul-before.md) — Initial soul configuration
- [`soul-after.md`](soul-after.md) — Soul after 30 days of growth
- [`changelog-sample.md`](changelog-sample.md) — Drift changelog over 30 days
