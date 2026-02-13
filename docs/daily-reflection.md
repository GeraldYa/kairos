# Daily Reflection

Daily reflection is Kairos's **introspection mechanism**—a nightly process where the agent reviews captured signals, evaluates behavioral trends, and updates its persona accordingly. Think of it as the agent's diary and self-improvement session combined.

---

## Purpose

The reflection process serves four key functions:

1. **Signal Synthesis**: Aggregate and make sense of the day's behavioral signals
2. **Trend Detection**: Identify consistent patterns across multiple days
3. **Persona Adjustment**: Calculate and apply dimension drift
4. **Self-Discovery**: Propose new behavioral dimensions based on emerging patterns

---

## Reflection Workflow

```
┌─────────────────────────────────────────────┐
│  1. Load Signals (today + last 7 days)     │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  2. Aggregate & Summarize                   │
│     - Count by type                         │
│     - Group by dimension                    │
│     - Identify user's emotional baseline    │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  3. Evaluate Core Dimensions                │
│     - Check for 3-day trends                │
│     - Calculate drift (+1, -1, or 0)        │
│     - Validate against boundaries           │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  4. Check Rebound Conditions                │
│     - Unused for 14+ days? → drift to default│
│     - Self-discovered unused 30+ days? → remove│
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  5. Self-Discovery Proposals                │
│     - Cluster unclassified signals          │
│     - Propose new dimensions (≥3 days)      │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  6. Generate Reflection Report              │
│     - What worked / didn't work             │
│     - Dimension changes with reasons        │
│     - New preferences detected              │
└─────────────────┬───────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────┐
│  7. Update Files                            │
│     - SOUL.md (new dimension values)        │
│     - soul-changelog.md (audit log)         │
│     - daily/YYYY-MM-DD.md (reflection report)│
└─────────────────────────────────────────────┘
```

---

## Step-by-Step Process

### 1. Load Signals

**Inputs**:
- `memory/growth/signals/YYYY-MM-DD.jsonl` (today)
- `memory/growth/signals/YYYY-MM-DD.jsonl` (last 7 days for trend detection)

**Code**:
```python
def load_signals(days=7):
    signals = []
    for i in range(days):
        date = today() - timedelta(days=i)
        file = f"memory/growth/signals/{date}.jsonl"
        if exists(file):
            signals.extend(read_jsonl(file))
    return signals
```

---

### 2. Aggregate & Summarize

**Tasks**:
- Count signals by type
- Group signals by related dimension
- Determine user's emotional baseline (were they happy, frustrated, neutral today?)

**Code**:
```python
def aggregate_signals(signals):
    summary = {
        "total": len(signals),
        "by_type": Counter([s["type"] for s in signals]),
        "by_dimension": group_by_dimension(signals),
        "avg_intensity": mean([s["intensity"] for s in signals]),
        "emotional_baseline": infer_emotion(signals)
    }
    return summary

def infer_emotion(signals):
    emotion_signals = [s for s in signals if s["type"] == "emotion"]
    if not emotion_signals:
        return "neutral"
    
    avg_valence = mean([sentiment_score(s["summary"]) for s in emotion_signals])
    if avg_valence > 0.3:
        return "positive"
    elif avg_valence < -0.3:
        return "negative"
    else:
        return "mixed"
```

**Example Output**:
```
Signal Summary:
- Total: 12
- By type: preference (3), emotion (4), correction (1), approval (3), style (1)
- Emotional baseline: User was frustrated early, satisfied later
- Avg intensity: 3.4
```

---

### 3. Evaluate Core Dimensions

**For each dimension**:
1. Find related signals from last 3 days
2. Check if ≥3 signals form a consistent trend
3. Calculate drift direction (+1, -1, or 0)
4. Validate new value against baseline boundaries

**Code**:
```python
def evaluate_dimensions(signals_7days, current_soul, baseline):
    adjustments = {}
    
    for dimension in current_soul.dimensions:
        # Get relevant signals from last 3 days
        recent = signals_7days[-3:]  # last 3 days
        relevant = [s for s in recent if matches_dimension(s, dimension)]
        
        if len(relevant) < 3:
            continue  # Insufficient trend
        
        # Determine direction
        drift = calculate_drift_direction(relevant)
        
        if drift != 0:
            old_val = current_soul[dimension]
            new_val = clamp(
                old_val + drift,
                baseline[dimension].min,
                baseline[dimension].max
            )
            
            if new_val != old_val:
                adjustments[dimension] = {
                    "old": old_val,
                    "new": new_val,
                    "drift": new_val - old_val,
                    "reason": summarize_trend(relevant)
                }
    
    return adjustments
```

**Example Evaluation**:

| Dimension | Current | Signals (3d) | Trend | New Value | Reason |
|-----------|---------|--------------|-------|-----------|--------|
| warmth | 5 | 4 approval signals | ↑ | 6 | User appreciated empathetic responses |
| verbosity | 5 | 3 style signals | ↓ | 4 | User prefers brevity |
| humor | 5 | 2 approval signals | — | 5 | Insufficient trend (need ≥3) |
| distance | 7 | 0 signals | — | 7 | No change |

---

### 4. Check Rebound Conditions

**For each dimension**:
- If 0 signals for 14+ days → drift toward default by 0.5/day
- If self-discovered dimension with 0 signals for 30+ days → remove entirely

**Code**:
```python
def check_rebound(dimension, signals_30days, current_val, default_val):
    recent_signals = [s for s in signals_30days if matches_dimension(s, dimension)]
    
    if len(recent_signals) == 0:
        days_since_last = days_since_signal(dimension, signals_30days)
        
        if days_since_last >= 30 and is_self_discovered(dimension):
            return {"action": "remove", "reason": "No signals for 30+ days"}
        
        elif days_since_last >= 14:
            # Rebound toward default
            if current_val > default_val:
                new_val = current_val - 0.5
            elif current_val < default_val:
                new_val = current_val + 0.5
            else:
                new_val = current_val  # already at default
            
            return {
                "action": "rebound",
                "old": current_val,
                "new": new_val,
                "reason": f"Unused for {days_since_last} days, rebounding to default"
            }
    
    return None  # No rebound needed
```

**Example Rebound**:
```
Dimension: proactivity
- Current value: 7
- Default value: 5
- Days since last signal: 16
- Action: Rebound 7 → 6.5 (moving toward default)
```

---

### 5. Self-Discovery Proposals

**Goal**: Identify new behavioral dimensions from unclassified signals

**Algorithm**:
1. Find signals that don't match any existing dimension
2. Cluster by semantic similarity (topic modeling)
3. If cluster has ≥3 signals across ≥3 days → propose new dimension

**Code**:
```python
def discover_dimensions(signals_7days, existing_dimensions):
    # Find unclassified signals
    unclassified = [
        s for s in signals_7days 
        if not matches_any_dimension(s, existing_dimensions)
    ]
    
    if len(unclassified) < 3:
        return []  # Not enough data
    
    # Cluster by topic
    clusters = topic_cluster(unclassified, method="semantic")
    
    proposals = []
    for cluster in clusters:
        days_spanned = count_unique_days(cluster.signals)
        
        if len(cluster.signals) >= 3 and days_spanned >= 3:
            proposals.append({
                "name": suggest_dimension_name(cluster),
                "description": cluster.theme,
                "evidence": cluster.signals,
                "default_value": 5,
                "range": [1, 10]
            })
    
    return proposals
```

**Example Discovery**:

**Unclassified signals**:
- Day 1: `approval` "You predicted exactly what I needed"
- Day 3: `approval` "Already set up, perfect"
- Day 5: `approval` "Prepared ahead of time, thanks"
- Day 6: `approval` "Proactive as always"

**Clustering**:
- Theme: Proactive preparation
- Signal count: 4
- Days spanned: 4

**Proposal**:
```markdown
**New dimension**: anticipation
- Description: Level of proactive preparation and need prediction
- Default: 5
- Range: [1-10]
- Evidence: 4 approval signals over 4 days
```

---

### 6. Generate Reflection Report

**Purpose**: Create a human-readable narrative of the day's learnings

**Template**:
```markdown
# YYYY-MM-DD Daily Reflection

## Signal Summary
- Total signals: {count}
- Breakdown: {by_type}

## User's Emotional Baseline Today
- **Observation**: {emotion_narrative}
- **Inference**: {interpretation}

## What Worked
{list_of_approved_behaviors}

## What Didn't Work
{list_of_corrections}

## New Preferences Detected
{list_of_preference_signals}

## Dimension Evaluation
| Dimension  | Current | Change | Reason |
|------------|---------|--------|--------|
{dimension_table}

## Rebound Check
{rebound_actions}

## Self-Discovery Proposals
{new_dimension_proposals}

---
*Generated: {timestamp}*
*Next reflection: {tomorrow}*
```

**Example Report**:
```markdown
# 2026-02-12 Daily Reflection

## Signal Summary
- Total signals: 8
- Breakdown: preference (2), emotion (2), approval (3), style (1)

## User's Emotional Baseline Today
- **Observation**: User started day frustrated (2 correction signals), ended satisfied (2 approval signals)
- **Inference**: Morning meeting stress → resolved by afternoon

## What Worked
- Providing bullet-point summaries (approved 2×)
- Quick turnaround on requests (approved 1×)
- Anticipating follow-up questions (approved 1×)

## What Didn't Work
- Long explanation in response 3 (user interrupted)

## New Preferences Detected
- User explicitly prefers bullet points over paragraphs
- User wants direct answers first, context optional

## Dimension Evaluation
| Dimension  | Current | Change | Reason |
|------------|---------|--------|--------|
| warmth     | 5       | +1     | 3 days of positive emotional signals |
| verbosity  | 5       | -1     | 3 days of preference for brevity |
| humor      | 5       | 0      | Only 2 days of signals, not consistent |

## Rebound Check
- No dimensions unused for 14+ days

## Self-Discovery Proposals
- None today

---
*Generated: 2026-02-12 23:00*
*Next reflection: 2026-02-13 23:00*
```

---

### 7. Update Files

**Files to update**:

1. **SOUL.md** (current persona state):
   ```markdown
   ## Behavioral Dimensions (current values)
   - warmth: 6 (↑1 from baseline)
   - verbosity: 4 (↓1 from baseline)
   ```

2. **soul-changelog.md** (audit trail):
   ```markdown
   ## 2026-02-12
   - **warmth**: 5 → 6 (+1)
     - Reason: 3-day trend of positive emotional responses
     - Signals: 2026-02-10 (emotion, intensity 4), 2026-02-11 (approval, intensity 3), 2026-02-12 (emotion, intensity 5)
   - **verbosity**: 5 → 4 (-1)
     - Reason: User explicitly prefers shorter responses
     - Signals: 2026-02-10 (style, intensity 3), 2026-02-11 (preference, intensity 4), 2026-02-12 (preference, intensity 5)
   ```

3. **daily/YYYY-MM-DD.md** (reflection report):
   - Save the full generated report

**Code**:
```python
def update_files(adjustments, reflection_report):
    # Update SOUL.md
    for dimension, change in adjustments.items():
        update_dimension_in_soul(dimension, change["new"])
    
    # Append to changelog
    changelog_entry = format_changelog(adjustments, today())
    append_to_file("config/growth/soul-changelog.md", changelog_entry)
    
    # Save reflection report
    save_file(f"config/growth/daily/{today()}.md", reflection_report)
```

---

## Scheduling

**Recommended**: Run reflection nightly at a consistent time (e.g., 2 AM)

### Cron Job (Linux/Mac)
```bash
# Run at 2 AM every day
0 2 * * * /path/to/kairos/scripts/reflect.py
```

### Systemd Timer (Linux)
```ini
# /etc/systemd/system/kairos-reflect.timer
[Unit]
Description=Kairos Daily Reflection Timer

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

### Task Scheduler (Windows)
```powershell
# Create a daily task at 2 AM
schtasks /create /tn "Kairos Reflection" /tr "python C:\path\to\reflect.py" /sc daily /st 02:00
```

---

## Reflection Script Template

```python
#!/usr/bin/env python3
"""
Kairos Daily Reflection Script
Run nightly to process signals and update persona
"""

import json
from datetime import datetime, timedelta
from pathlib import Path

# Configuration
SIGNAL_DIR = Path("memory/growth/signals")
DAILY_DIR = Path("config/growth/daily")
SOUL_FILE = Path("config/SOUL.md")
BASELINE_FILE = Path("config/growth/baseline.md")
CHANGELOG_FILE = Path("config/growth/soul-changelog.md")

def main():
    print(f"[{datetime.now()}] Starting daily reflection...")
    
    # 1. Load signals
    signals_7days = load_signals(days=7)
    signals_today = load_signals(days=1)
    print(f"Loaded {len(signals_today)} signals from today, {len(signals_7days)} from last 7 days")
    
    # 2. Aggregate
    summary = aggregate_signals(signals_today)
    print(f"Signal breakdown: {summary['by_type']}")
    
    # 3. Load current state
    current_soul = parse_soul(SOUL_FILE)
    baseline = parse_baseline(BASELINE_FILE)
    
    # 4. Evaluate dimensions
    adjustments = evaluate_dimensions(signals_7days, current_soul, baseline)
    print(f"Dimension adjustments: {len(adjustments)}")
    
    # 5. Check rebound
    rebounds = check_all_rebounds(current_soul, signals_7days, baseline)
    adjustments.update(rebounds)
    
    # 6. Self-discovery
    proposals = discover_dimensions(signals_7days, current_soul.dimensions)
    print(f"New dimension proposals: {len(proposals)}")
    
    # 7. Generate report
    report = generate_report(
        signals_today=signals_today,
        summary=summary,
        adjustments=adjustments,
        proposals=proposals
    )
    
    # 8. Update files
    if adjustments:
        update_soul(SOUL_FILE, adjustments)
        append_changelog(CHANGELOG_FILE, adjustments)
        print(f"Updated {len(adjustments)} dimensions")
    
    save_report(DAILY_DIR / f"{datetime.now().date()}.md", report)
    print(f"Reflection complete. Report saved to {DAILY_DIR}")

if __name__ == "__main__":
    main()
```

---

## Best Practices

### ✅ Do:
- Run reflection at the same time every day (consistency)
- Review reflection reports weekly (spot-check for correctness)
- Archive old signal files monthly (keep last 90 days active)
- Test reflection logic with synthetic signals
- Log reflection errors for debugging
- Monitor changelog for unexpected drift

### ❌ Don't:
- Run reflection multiple times per day (causes duplicate adjustments)
- Skip days (breaks trend detection)
- Manually edit SOUL.md without logging to changelog
- Ignore rebound warnings (dimensions drifting too far)
- Delete old reflection reports (audit trail)
- Run reflection during active conversations (file locking issues)

---

## Advanced: Reflection Strategies

### Strategy 1: Weighted Signal Analysis
Give more weight to recent signals:

```python
def calculate_drift_weighted(signals):
    total_weight = 0
    weighted_direction = 0
    
    for i, signal in enumerate(signals):
        age_weight = 1.0 + (i * 0.2)  # Recent signals weighted higher
        intensity_weight = signal["intensity"] / 5.0
        
        weight = age_weight * intensity_weight
        direction = get_direction(signal)  # +1 or -1
        
        weighted_direction += direction * weight
        total_weight += weight
    
    if weighted_direction / total_weight > 0.5:
        return +1
    elif weighted_direction / total_weight < -0.5:
        return -1
    else:
        return 0
```

---

### Strategy 2: Confidence Scoring
Only adjust when confidence is high:

```python
def calculate_confidence(signals):
    """
    Returns: 0.0 to 1.0
    High confidence = many signals, high intensity, consistent direction
    """
    if len(signals) < 3:
        return 0.0
    
    direction_consistency = count_majority_direction(signals) / len(signals)
    avg_intensity = mean([s["intensity"] for s in signals]) / 5.0
    signal_count_factor = min(len(signals) / 5.0, 1.0)
    
    confidence = (direction_consistency * 0.5 + 
                  avg_intensity * 0.3 + 
                  signal_count_factor * 0.2)
    
    return confidence

# Usage
if calculate_confidence(relevant_signals) > 0.7:
    apply_drift(dimension, direction)
```

---

### Strategy 3: Multi-Day Trend Smoothing
Require trend across variable window (3-5 days):

```python
def detect_trend_flexible(signals_7days, dimension):
    for window in [5, 4, 3]:  # Try 5-day, then 4-day, then 3-day
        recent = signals_7days[-window:]
        relevant = [s for s in recent if matches_dimension(s, dimension)]
        
        if len(relevant) >= window * 0.6:  # At least 60% of days have signals
            trend = calculate_drift_direction(relevant)
            if trend != 0:
                return trend, window
    
    return 0, 0  # No trend found
```

---

## Troubleshooting

### Reflection Script Fails
**Check**:
- Signal files exist and are valid JSON
- File permissions (script can read/write)
- No concurrent access to SOUL.md
- Python dependencies installed

**Debug**:
```bash
# Run reflection manually with verbose logging
python reflect.py --verbose --dry-run
```

---

### No Dimension Changes Detected
**Possible causes**:
- Insufficient signals (<3 in 3 days)
- Signals not classified to dimensions correctly
- Dimension already at boundary limit
- Conflicting signals canceling out

**Debug**:
```python
# Check signal classification
for signal in signals_today:
    print(f"{signal['summary']} → {classify_dimension(signal)}")
```

---

### Unexpected Dimension Drift
**Investigate**:
- Review signals in `signals/YYYY-MM-DD.jsonl`
- Check if signal detection is over-capturing
- Verify drift calculation logic
- Review changelog for pattern

**Rollback**:
```bash
# Restore from baseline
cp config/growth/baseline.md config/SOUL.md
echo "## $(date) - Manual rollback" >> config/growth/soul-changelog.md
```

---

### Reflection Takes Too Long
**Optimize**:
- Limit signal window (7 days → 5 days)
- Cache parsed baseline
- Use efficient JSON parsing (ijson for streaming)
- Profile slow functions

---

## Metrics & Monitoring

### Track Reflection Health

```python
# Reflection metrics to log
metrics = {
    "signals_today": len(signals_today),
    "signals_7days": len(signals_7days),
    "dimensions_adjusted": len(adjustments),
    "rebounds_triggered": len(rebounds),
    "new_dimensions_proposed": len(proposals),
    "reflection_duration_seconds": elapsed_time,
    "errors": error_count
}
```

### Alert Conditions

**Warn if**:
- 0 signals for 7+ days (user inactive or detection broken?)
- >5 dimensions adjusted in one day (too volatile)
- Reflection duration >30 seconds (performance issue)
- Any dimension at boundary for 5+ days (stuck at limit)

---

## Example: Complete Reflection Output

```markdown
# 2026-02-12 Daily Reflection

## Signal Summary
- Total signals: 12
- Breakdown: preference (3), emotion (4), correction (1), approval (3), style (1)
- Average intensity: 3.8

## User's Emotional Baseline Today
- **Observation**: User started frustrated (morning correction signal), became satisfied (afternoon approvals)
- **Inference**: Work stress resolved, user in good mood by evening

## What Worked
- Bullet-point format (3× approval)
- Quick response time (2× approval)
- Anticipating next question (1× approval)

## What Didn't Work
- Over-explained technical concept (1× correction: "just give me the answer")

## New Preferences Detected
- Strong preference for brevity (3 signals across 3 days)
- Prefers direct answers over context-heavy explanations

## Dimension Evaluation
| Dimension  | Current | Change | Reason |
|------------|---------|--------|--------|
| warmth     | 5       | +1     | 3-day trend: positive emotional signals |
| verbosity  | 5       | -1     | 3-day trend: explicit preference for brevity |
| humor      | 5       | 0      | Only 2 days of signals (need 3) |
| distance   | 7       | 0      | No related signals |
| proactivity| 5       | 0      | No related signals |
| caution    | 5       | 0      | No related signals |

## Rebound Check
- No dimensions unused for 14+ days

## Self-Discovery Proposals
- None today (no unclassified signal clusters)

## Actions Taken
✅ Updated SOUL.md:
   - warmth: 5 → 6
   - verbosity: 5 → 4
✅ Logged changes to soul-changelog.md
✅ Saved reflection report

---
*Generated: 2026-02-12 23:05:22*
*Next reflection: 2026-02-13 23:00:00*
*Reflection duration: 1.8 seconds*
```

---

## Summary

Daily reflection is the **growth engine** of Kairos:

1. **Input**: Day's behavioral signals
2. **Processing**: Trend detection + persona calculation
3. **Output**: Updated SOUL.md + audit trail

**Key principles**:
- Run consistently (same time daily)
- Require evidence (≥3 signals)
- Change gradually (±1/day max)
- Log everything (full auditability)
- Revert when needed (rebound mechanism)

---

[← Persona Drift](persona-drift.md) | [README](../README.md) | [Architecture](architecture.md)
