# YYYY-MM-DD Daily Reflection

## Signal Summary
- Total signals: {{count}}
- Breakdown: preference ({{count}}), emotion ({{count}}), correction ({{count}}), approval ({{count}}), style ({{count}})
- Average intensity: {{avg}}

## User's Emotional Baseline Today
- **Observation**: {{describe_emotional_state}}
- **Inference**: {{interpret_context}}

## What Worked
- {{approved_behavior_1}}
- {{approved_behavior_2}}
- {{approved_behavior_3}}

## What Didn't Work
- {{corrected_behavior_1}}
- {{corrected_behavior_2}}

## New Preferences Detected
- {{new_preference_1}}
- {{new_preference_2}}

## Dimension Evaluation

| Dimension  | Current | Change | Reason |
|------------|---------|--------|--------|
| warmth     | {{val}} | {{change}} | {{reason}} |
| distance   | {{val}} | {{change}} | {{reason}} |
| proactivity| {{val}} | {{change}} | {{reason}} |
| humor      | {{val}} | {{change}} | {{reason}} |
| caution    | {{val}} | {{change}} | {{reason}} |
| verbosity  | {{val}} | {{change}} | {{reason}} |

## Rebound Check
- {{dimension}}: {{current}} → {{new}} ({{reason}})
- Or: No rebounds triggered today

## Self-Discovery Proposals
- **Proposed dimension**: {{name}}
  - **Description**: {{what_it_measures}}
  - **Evidence**: {{signal_count}} signals over {{day_count}} days
  - **Action**: {{add|defer|none}}

- Or: None today

## Actions Taken
✅ {{action_1}}
✅ {{action_2}}
❌ {{failed_action}} (reason: {{why}})

---

*Generated: {{timestamp}}*  
*Next reflection: {{tomorrow_timestamp}}*  
*Reflection duration: {{seconds}} seconds*

---

## Instructions:

This template is filled automatically by the daily reflection script. Example:

```markdown
# 2026-02-12 Daily Reflection

## Signal Summary
- Total signals: 8
- Breakdown: preference (2), emotion (2), correction (1), approval (3), style (0)
- Average intensity: 3.6

## User's Emotional Baseline Today
- **Observation**: User started day frustrated, ended satisfied
- **Inference**: Morning issue resolved by afternoon

## What Worked
- Bullet-point summaries (3× approval)
- Quick response time (1× approval)

## What Didn't Work
- Long technical explanation (1× correction: "just give me the answer")

## New Preferences Detected
- Strong preference for brevity (2 signals over 2 days)

## Dimension Evaluation

| Dimension  | Current | Change | Reason |
|------------|---------|--------|--------|
| warmth     | 5       | +1     | 3-day trend of positive emotional signals |
| verbosity  | 5       | -1     | 3-day trend: user prefers shorter responses |
| humor      | 5       | 0      | Only 2 days of signals (need 3) |
| distance   | 7       | 0      | No related signals |
| proactivity| 5       | 0      | No related signals |
| caution    | 5       | 0      | No related signals |

## Rebound Check
- No dimensions unused for 14+ days

## Self-Discovery Proposals
- None today

## Actions Taken
✅ Updated SOUL.md: warmth 5→6, verbosity 5→4
✅ Logged changes to soul-changelog.md
✅ Saved reflection report

---
*Generated: 2026-02-12 23:05:00*
*Next reflection: 2026-02-13 23:00:00*
*Reflection duration: 1.8 seconds*
```
