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

### Example Entries:

```markdown
# SOUL Changelog — Atlas

---

## 2026-02-12
- **warmth**: 5 → 6 (+1)
- **Reason**: 3-day trend of positive emotional signals; user responded well to empathetic tone
- **Evidence**: 2026-02-10 (emotion, intensity 4), 2026-02-11 (approval, intensity 3), 2026-02-12 (emotion, intensity 5)

- **verbosity**: 5 → 4 (-1)
- **Reason**: User explicitly requested shorter responses multiple times
- **Evidence**: 2026-02-10 (preference, intensity 4), 2026-02-11 (style, intensity 3), 2026-02-12 (preference, intensity 5)

---

## 2026-02-15
- **New dimension added**: anticipation (default 5, range 1-10)
- **Reason**: 4 days of approval signals for proactive behavior
- **Evidence**: 2026-02-12 (approval), 2026-02-13 (approval), 2026-02-14 (approval), 2026-02-15 (approval)

---

## 2026-02-20
- **humor**: 5 → 5.5 (+0.5)
- **Reason**: Rebounding from 4 toward default (unused for 14 days)
- **Evidence**: No humor-related signals since 2026-02-05

---

## 2026-03-10
- **Dimension removed**: anticipation
- **Reason**: No related signals for 30+ consecutive days
- **Evidence**: Last signal 2026-02-08

---

## 2026-03-15
- **Manual reversion to baseline**
- **Reason**: Administrator reset
- **Action**: All dimensions restored to baseline defaults
```

### Audit Uses:
- Track persona evolution over time
- Identify unexpected drift patterns
- Debug reflection algorithm issues
- Demonstrate compliance (for regulated environments)
- Support rollback to previous states

---

*First entry: {{initialization_date}}*  
*This file should never be manually edited (except for manual reversions or corrections)*
