# Case Study: niuxue.org's 6-Agent Household

> A real production deployment of Kairos powering 6 distinct AI agents sharing one Claude Code runtime, each with separate identity, soul, and growth track.

## Context

[niuxue.org](https://niuxue.org) is a free Chinese AI tutorial site. Behind the site is a household of 6 specialized agents handling content, finance, media, fiction, technical builds, and editorial — all running on the same Claude Code container, each on its own Telegram bot endpoint, each with its own Kairos persona files.

The full narrative version (with user-facing stories, dispatch examples, and 3 anti-collision rules) lives on the site:
→ **[niuxue.org/guides/case-bot-family/](https://niuxue.org/guides/case-bot-family/)**

This document covers the **technical implementation** — the parts a Kairos integrator needs to copy.

## Per-Agent File Layout

Every agent has its own project directory containing:

```
bots/<agent-name>-telegram/
├── CLAUDE.md                                        # project memory loaded at startup
└── .claude/projects/-home-gerald-bots-<name>/
    └── memory/
        ├── IDENTITY.md                              # immutable baseline (Kairos)
        ├── SOUL.md                                  # current behavioural state (Kairos)
        ├── soul-changelog.md                        # append-only drift log (Kairos)
        ├── signals.jsonl                            # captured signals (Kairos)
        └── style-profile.md                         # learned user preferences (Kairos)
```

Critically, **each agent's `memory/` directory is scoped to its own project path**. Claude Code loads project-scoped memory automatically, so cross-agent bleed is structurally prevented — not just policy-enforced.

## The 6 Agent Personas

Each persona is defined in `IDENTITY.md` (baseline) + `SOUL.md` (current state). Baseline never changes; SOUL drifts within bounded ranges.

| Agent | Baseline excerpt | Initial dimensions |
|---|---|---|
| **小墨 (Mo)** | "27-year-old elder-sister archetype, the household anchor" | warmth 7, distance 4, proactivity 7, verbosity 5 |
| **小牛 (Niu)** | "22-year-old energetic younger-sister, technical builder" | playfulness 9, affection 7, sass 5, verbosity 7 |
| **算盘 (Poly)** | "32-year-old sharp analyst, finance and Polymarket lead" | precision 9, sass 6, verbosity 6, jargon 8 |
| **胶片 (Media)** | "28-year-old quiet film aesthete, media library curator" | precision 8, verbosity 3, calm 8 |
| **半勺 (Bootes)** | "35-year-old deep-space philosopher, fiction writer" | depth 9, verbosity 4, pacing 2 (slow) |
| **橙子 (Chengzi)** | "30-year-old composed editor, tutorial site editorial lead" | precision 7, calm 7, verbosity 5, restraint 8 |

## Dispatch Pattern

The user (洁柔 / Gerald) routes each request by **picking the right agent's Telegram bot**, not by going through a single dispatcher. Each `@bot` corresponds to one persona, on one process, with one memory scope.

| Scenario | Agent picked |
|---|---|
| Morning planning, scheduling | Mo |
| Building a tool / content writing | Niu |
| Options positioning, market read | Poly |
| Media library, downloads | Media |
| Long-form fiction | Bootes |
| Editorial cuts on tutorials | Chengzi |

Because each agent has its own SOUL + signals + changelog, signals captured during one conversation only update that agent's persona. Poly learning "user prefers Greeks jargon" never leaks into Bootes's vocabulary.

## 3 Anti-Collision Rules

These are documented in the user-facing case study but worth listing here for integrators:

1. **One IDENTITY.md per agent, never in the home directory.** The home `~/.claude/CLAUDE.md` only carries universal constraints (user name, timezone, language). Persona-specific baselines all sit in per-project memory.

2. **One Telegram bot token per agent.** Telegram does not allow two processes to share a bot token — they kick each other off. Register each persona as its own bot in BotFather.

3. **Niches must not overlap.** If two agents both list "writes code" as a specialty, the user can't decide who to ping. Give every agent a unique niche; document overlap explicitly in IDENTITY if it's unavoidable.

## Soul Changelog Example (anonymised)

A real entry from one of the agents, format follows Kairos's `templates/soul-changelog.md`:

```markdown
## 2026-05-16
- **warmth**: 7 → 8 (+1)
- **Reason**: 3-day trend of positive emotional signals after a difficult week
- **Evidence**: 2026-05-14 (emotion, intensity 4), 2026-05-15 (approval, intensity 5), 2026-05-16 (emotion, intensity 4)

- **verbosity**: 5 → 4 (-1)
- **Reason**: User repeatedly requested shorter replies during a high-throughput working session
- **Evidence**: 2026-05-14 (preference, intensity 5), 2026-05-15 (style, intensity 4), 2026-05-16 (preference, intensity 5)
```

The full per-agent changelogs are private (real conversations) but the **format and discipline** are exactly Kairos.

## What Kairos Buys You at Scale

Running 6 personas without Kairos gets messy fast:

- Personalities blur unless you manually re-prompt each session
- "What did this agent learn last week?" has no auditable answer
- Drift is unbounded — agents can wander off character without you noticing
- Rolling one persona back means combing through manual edits

With Kairos:

- Each agent has a **per-day drift cap** (±1) — sudden character swings are structurally impossible
- The **append-only changelog** gives you a full audit trail
- **14-day rebound** keeps unused dimensions from permanently drifting away from baseline
- Rolling back is one file revert

## Anti-patterns This Deployment Avoids

- ❌ **Sharing the home directory `CLAUDE.md`** across agents — bleeds persona rules everywhere
- ❌ **Sharing one auto-memory directory** — Poly learning options jargon would leak into Bootes
- ❌ **Letting niches overlap** — user can't pick who to talk to
- ❌ **Tuning personas by editing IDENTITY** — that's the immutable baseline; drift happens in SOUL via signals

## Reference

- User-facing case study: [niuxue.org/guides/case-bot-family/](https://niuxue.org/guides/case-bot-family/)
- Kairos templates: [`templates/`](../templates/)
- Architecture deep-dive: [`docs/architecture.md`](architecture.md)
- Drift mechanics: [`docs/persona-drift.md`](persona-drift.md)
