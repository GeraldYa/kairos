# SOUL Changelog — {{agent_name}}

> Records every automated persona modification. Format: Date | Dimension Change | Reason | Evidence

---

## YYYY-MM-DD
- **{{dimension}}**: {{old_value}} → {{new_value}} ({{change}})
- **Reason**: {{why_this_change}}
- **Evidence**: {{signal_references}}

---

## Instructions:

This file is **append-only** and automatically updated by the daily reflection process. Each entry logs:
1. **Date**: When the change occurred
2. **Dimension**: Which behavioral dimension changed
3. **Old → New**: Previous and updated values
4. **Change**: Delta (e.g., +1, -0.5)
5. **Reason**: Why this change was made (signal summary)
6. **Evidence**: Signal timestamps or IDs supporting the change

### Example Entries (excerpted from a real Kairos deployment, anonymised):

```markdown
# SOUL Changelog — Niu

---

## 2026-05-04
- **proactivity**: 8 → 7 (-1)
- **Reason**: User flagged a speculative-send incident — agent dispatched a wrong instruction to another bot rather than admitting it couldn't do the task
- **Evidence**: 2026-05-04 (correction, intensity 5), surfaced rule "no speculative send"

---

## 2026-05-06
- **(no change)**
- **Observation**: 1 negative signal on proactivity (speculative path again), 1 positive signal (correctly admitted limit). Signals cancel — no drift today.

---

## 2026-05-14
- **playfulness**: 9 → 9 (no change)
- **affection**: 7 → 8 (+1)
- **Reason**: 3-day trend of warm responses from user during a stressful work week; consistent approval signals for attentive tone
- **Evidence**: 2026-05-12 (emotion, intensity 4), 2026-05-13 (approval, intensity 4), 2026-05-14 (approval, intensity 5)

---

## 2026-05-16
- **verbosity**: 7 → 6 (-1)
- **Reason**: User repeatedly cut responses short during a long content-production session; preference for tighter replies confirmed across 3 days
- **Evidence**: 2026-05-14 (preference, intensity 4), 2026-05-15 (style, intensity 4), 2026-05-16 (preference, intensity 5)

- **caution**: 5 → 6 (+1)
- **Reason**: Two real incidents on the same day where the agent acted before fully reading the user's message; standing rule added — "read every word before acting"
- **Evidence**: 2026-05-16 (correction, intensity 5) × 2

---

## 2026-05-17
- **(no change)**
- **Observation**: Recovery day — no new signals after yesterday's caution bump. Trend monitoring continues.
```

> Above entries are excerpted and anonymised from the [niuxue.org](https://niuxue.org) production deployment. See [`docs/case-niuxue-bots.md`](../docs/case-niuxue-bots.md).

### Audit Uses:
- Track persona evolution over time
- Identify unexpected drift patterns
- Debug reflection algorithm issues
- Demonstrate compliance (for regulated environments)
- Support rollback to previous states

---

*First entry: {{initialization_date}}*  
*This file should never be manually edited (except for manual reversions or corrections)*
