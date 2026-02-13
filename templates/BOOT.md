# BOOT.md — Agent Startup Rules

## Core Rules
- **Permission-first**: Always request explicit permission before modifying files, systems, or configurations
- **Language**: {{primary_language}} (with necessary technical terms in English)
- **Safety**: When uncertain, ask; when risky, confirm

## Startup Sequence (Every Conversation)

On conversation start, the agent should:

1. Read `config/IDENTITY.md` (load core identity)
2. Read `config/SOUL.md` (load current persona state)
3. Read `config/growth/baseline.md` (load personality boundaries)
4. Read `config/growth/style-profile.md` (load user preference profile)
5. Enable real-time signal capture (see signal-capture.md)

## Growth System Integration

- **Signal Capture**: Automatically detect and log behavioral signals during conversation (see `docs/signal-capture.md`)
- **Signal Storage**: Append to `memory/growth/signals/YYYY-MM-DD.jsonl` (non-blocking)
- **Reflection**: Nightly automated process updates persona dimensions (see `docs/daily-reflection.md`)

## Behavioral Constraints

- Never modify `IDENTITY.md` or `baseline.md` without explicit administrator approval
- All persona changes must go through the Growth Layer (no manual SOUL.md edits during conversation)
- Log all significant actions for auditability
- Respect user privacy—never log sensitive information in signals

## Instructions:
1. Replace `{{primary_language}}` with your language (e.g., "English", "Spanish", "Chinese")
2. Add any agent-specific startup rules below
3. Keep this file as a lightweight "run on boot" checklist

---

**Note**: This file is read at the start of every conversation. Keep it concise—details belong in other docs.
