# Persona Drift

Persona drift is Kairos's mechanism for **controlled, gradual personality evolution**. Unlike static system prompts, agents with persona drift can adapt their communication style and behavioral tendencies based on accumulated user feedback—while always staying anchored to their core identity.

---

## Core Concept

Every agent has two personality layers:

1. **Baseline (Identity Layer)**: Immutable core—who the agent fundamentally is
2. **Floating Layer (Soul Layer)**: Adjustable dimensions that can drift within boundaries

Think of it like this:
- **Baseline** = Your genetics and core values (unchangeable)
- **Floating Layer** = Your mood, habits, and social masks (adaptive)

The floating layer can shift based on signals, but it's always tethered to the baseline by elastic constraints.

---

## Dimension System

Persona is quantified using **behavioral dimensions**—numeric scales (1-10) representing traits.

### Core Dimensions (Fixed Set)

These dimensions are defined in `baseline.md` and cannot be removed:

| Dimension | Default | Range | Description |
|-----------|---------|-------|-------------|
| **warmth** | 5 | 1-10 | Emotional temperature: 1=cold/distant, 10=warm/nurturing |
| **distance** | 5 | 3-10 | Social proximity: 3=casual/familiar, 10=formal/respectful |
| **proactivity** | 5 | 1-8 | Initiative level: 1=reactive only, 8=anticipates needs |
| **humor** | 5 | 1-8 | Playfulness: 1=serious/professional, 8=frequent jokes |
| **caution** | 5 | 1-8 | Risk appetite: 1=bold/direct, 8=careful/hesitant |
| **verbosity** | 5 | 1-8 | Response length: 1=terse/minimal, 8=detailed/explanatory |

**Design rationale**:
- **Default = 5**: Neutral starting point
- **Range limits**: Prevent extreme personality shifts (e.g., distance can't go below 3 to maintain minimum professionalism)
- **Core set**: Covers most common behavioral axes

### Self-Discovered Dimensions (Dynamic)

Beyond the core 6, agents can **discover new dimensions** based on recurring signal patterns:

**Example discovered dimensions**:
- `empathy`: How attuned to user's emotional state (discovered from approval signals when agent validates feelings)
- `technical_depth`: Level of technical jargon (discovered from correction signals about complexity)
- `anticipation`: Proactively preparing things (discovered from approval signals when agent predicts needs)
- `assertiveness`: Confidence in recommendations (discovered from preference signals about decisiveness)

**Discovery rules**:
1. ≥3 days of related signals within 7-day window
2. Signals must form a coherent theme (not random)
3. Maximum 4 self-discovered dimensions at a time (total ≤10 dimensions)
4. New dimension defaults to value 5, range 1-10

**Retirement rules**:
- If a self-discovered dimension receives 0 signals for 30 consecutive days → remove
- Retirement logged in `soul-changelog.md`

---

## Drift Mechanics

### Adjustment Rules

**Trigger**: Daily reflection detects consistent signal trend

**Requirement**: ≥3 days of signals pointing in the same direction

**Magnitude**: ±1 per day maximum

**Validation**: New value must stay within dimension's allowed range

### Example: Decreasing Verbosity

**Scenario**: User repeatedly asks for shorter responses

**Day 1**:
- Signals: 2 × `style` (user sent short messages)
- Action: None (need 3-day trend)

**Day 2**:
- Signals: 1 × `preference` ("just give me the answer"), 1 × `style`
- Action: None (only 2 days)

**Day 3**:
- Signals: 1 × `preference` ("stop explaining"), intensity 5
- Action: ✅ 3-day trend detected → `verbosity: 5 → 4` (-1)

**Day 4**:
- Signals: 0 (user satisfied with shorter responses)
- Action: None (no further adjustment)

**Result**: Agent now generates shorter responses by default

---

### Adjustment Algorithm

```python
def calculate_drift(dimension, signals_3_days):
    """
    Returns: -1, 0, or +1
    """
    related_signals = filter_by_dimension(signals_3_days, dimension)
    
    if len(related_signals) < 3:
        return 0  # Insufficient trend
    
    # Calculate direction
    positive_signals = [s for s in related_signals if is_positive(s)]
    negative_signals = [s for s in related_signals if is_negative(s)]
    
    pos_weight = sum([s.intensity for s in positive_signals])
    neg_weight = sum([s.intensity for s in negative_signals])
    
    if pos_weight > neg_weight * 1.5:  # Strong positive trend
        return +1
    elif neg_weight > pos_weight * 1.5:  # Strong negative trend
        return -1
    else:
        return 0  # Mixed signals, no change

def apply_drift(current_value, drift, min_val, max_val):
    new_value = current_value + drift
    return clamp(new_value, min_val, max_val)
```

---

## Rebound Mechanism

**Problem**: Dimensions might drift away from baseline due to temporary user preferences, then become obsolete.

**Solution**: **Elastic rebound**—unused dimensions gradually return to default.

### Rebound Rules

| Condition | Action |
|-----------|--------|
| Dimension has 0 related signals for 14 days | Drift toward default by 0.5/day |
| Dimension has 0 related signals for 30 days | Reset to default value |
| Self-discovered dimension: 0 signals for 30 days | Remove dimension entirely |

### Example: Humor Rebound

**Scenario**: User initially enjoyed humor, agent increased `humor: 5 → 7`. Then user stopped responding to jokes.

**Day 1-13**: No humor-related signals
- Action: None (monitoring)

**Day 14**: Still no signals
- Action: `humor: 7 → 6.5` (-0.5, drifting toward default 5)

**Day 16**: Still no signals
- Action: `humor: 6.5 → 6` (-0.5)

**Day 18**: Still no signals
- Action: `humor: 6 → 5.5` (-0.5)

**Day 20**: User laughs at a joke (approval signal)
- Action: ✅ Stop rebound (dimension is active again)

**Result**: Dimension rebounds unless user re-engages with that behavior.

---

## Boundaries & Constraints

### Absolute Boundaries

Each dimension has **hard limits** defined in `baseline.md`:

```markdown
| warmth | 5 | 1-10 | Cannot exceed range |
```

**Enforcement**: Growth Layer rejects any adjustment that would violate limits.

```python
if new_value < min_allowed or new_value > max_allowed:
    log_warning(f"Drift rejected: {dimension} cannot go to {new_value}")
    return current_value
```

### Relative Boundaries (Soft)

Some dimensions have **contextual relationships**:

**Example**: `distance` and `warmth` are inversely related
- High distance (formal) + high warmth = professional but caring
- Low distance (casual) + low warmth = cold and rude ❌

**Validation rule**:
```python
if distance <= 4 and warmth <= 3:
    raise ValueError("Cannot be both casual AND cold")
```

---

## Drift Strategies

### Strategy 1: Conservative (Default)
- Require 3-day trend
- Max ±1/day drift
- 14-day rebound window
- 4 self-discovered dimensions max

**Best for**: Stable, predictable agents in professional settings

---

### Strategy 2: Aggressive
- Require 2-day trend
- Max ±2/day drift
- 7-day rebound window
- 6 self-discovered dimensions max

**Best for**: Experimental agents, rapid personalization

---

### Strategy 3: Ultra-Stable
- Require 5-day trend
- Max ±0.5/day drift
- 21-day rebound window
- 2 self-discovered dimensions max

**Best for**: Mission-critical agents, regulated environments

---

## Implementation Example

### Daily Reflection: Dimension Evaluation

```python
def evaluate_dimensions(signals_today, signals_7days, current_soul):
    adjustments = {}
    
    for dimension in current_soul.dimensions:
        # Get relevant signals from last 3 days
        relevant = get_relevant_signals(signals_7days[-3:], dimension)
        
        if len(relevant) >= 3:
            # Trend detected
            drift = calculate_drift(dimension, relevant)
            
            if drift != 0:
                new_val = apply_drift(
                    current_soul[dimension],
                    drift,
                    baseline[dimension].min,
                    baseline[dimension].max
                )
                adjustments[dimension] = {
                    "old": current_soul[dimension],
                    "new": new_val,
                    "reason": summarize_signals(relevant)
                }
        
        elif no_signals_for_n_days(dimension, signals_7days, n=14):
            # Rebound trigger
            default_val = baseline[dimension].default
            current_val = current_soul[dimension]
            
            if current_val != default_val:
                rebound = move_toward_default(current_val, default_val, step=0.5)
                adjustments[dimension] = {
                    "old": current_val,
                    "new": rebound,
                    "reason": "Rebounding to baseline (unused for 14+ days)"
                }
    
    return adjustments
```

### Applying Adjustments

```python
def apply_adjustments(adjustments, soul_file, changelog_file):
    for dimension, change in adjustments.items():
        # Update SOUL.md
        update_dimension_in_file(soul_file, dimension, change["new"])
        
        # Log to changelog
        log_entry = f"""
## {today()}
- **{dimension}**: {change["old"]} → {change["new"]} ({change["new"] - change["old"]:+.1f})
- **Reason**: {change["reason"]}
"""
        append_to_file(changelog_file, log_entry)
```

---

## Self-Discovery Process

### Discovery Algorithm

```python
def discover_new_dimensions(signals_7days, current_dimensions):
    # Cluster unclassified signals by topic
    unclassified = [s for s in signals_7days if not matches_any_dimension(s, current_dimensions)]
    
    clusters = topic_cluster(unclassified)
    
    proposals = []
    for cluster in clusters:
        if len(cluster.signals) >= 3 and cluster.spans_days >= 3:
            # Potential new dimension
            proposals.append({
                "name": cluster.topic_name,
                "description": cluster.description,
                "evidence": cluster.signals,
                "default_value": 5,
                "range": [1, 10]
            })
    
    return proposals
```

### Example: Discovering "Anticipation"

**Signals over 5 days**:
- Day 1: `approval` "Great that you already prepared the report"
- Day 3: `approval` "You read my mind, I was about to ask for that"
- Day 4: `approval` "Love that you set this up ahead of time"
- Day 5: `approval` "Proactive as always, thanks"

**Clustering**:
- Topic: "Proactive preparation"
- Theme: User appreciates when agent anticipates needs
- Proposed dimension: `anticipation`

**Action**:
- Add to `SOUL.md`: `anticipation: 5` (default)
- Add to `baseline.md` under "Self-Discovered Dimensions"
- Log to `soul-changelog.md`:
  ```
  ## 2026-02-15
  - **New dimension**: anticipation (default 5, range 1-10)
  - **Reason**: 4 days of approval signals for proactive behavior
  - **Evidence**: [signal IDs]
  ```

---

## Visualization

### Dimension Drift Over Time

```
warmth
  10 ┤                                          
   9 ┤                                          
   8 ┤                                          
   7 ┤                    ╭──────╮              
   6 ┤          ╭─────────╯      ╰────╮        
   5 ┼──────────╯                     ╰────────  ← baseline
   4 ┤                                          
   3 ┤                                          
   2 ┤                                          
   1 ┤                                          
     └┬────┬────┬────┬────┬────┬────┬────┬────
      Feb10  12   14   16   18   20   22   24

Legend:
- Solid line = current value
- Dotted line (5) = baseline default
- Drift range: [1-10]
```

---

## Testing Persona Drift

### Unit Tests

```python
def test_drift_within_bounds():
    current = 8
    drift = +1
    min_val, max_val = 1, 10
    result = apply_drift(current, drift, min_val, max_val)
    assert result == 9  # within bounds

def test_drift_clamped_at_boundary():
    current = 10
    drift = +1
    min_val, max_val = 1, 10
    result = apply_drift(current, drift, min_val, max_val)
    assert result == 10  # clamped at max

def test_rebound_toward_default():
    current = 8
    default = 5
    result = move_toward_default(current, default, step=0.5)
    assert result == 7.5
```

### Integration Tests

```python
def test_3day_trend_triggers_drift():
    signals = [
        {"type": "preference", "dimension": "verbosity", "direction": "decrease", "intensity": 4},
        {"type": "style", "dimension": "verbosity", "direction": "decrease", "intensity": 3},
        {"type": "preference", "dimension": "verbosity", "direction": "decrease", "intensity": 5}
    ]
    
    adjustment = calculate_drift("verbosity", signals)
    assert adjustment == -1

def test_mixed_signals_no_drift():
    signals = [
        {"dimension": "humor", "direction": "increase", "intensity": 3},
        {"dimension": "humor", "direction": "decrease", "intensity": 3},
        {"dimension": "humor", "direction": "increase", "intensity": 2}
    ]
    
    adjustment = calculate_drift("humor", signals)
    assert adjustment == 0  # conflicting signals
```

---

## Advanced: Multi-User Personas

**Problem**: A single agent serves multiple users with different preferences.

**Solution**: Branch Soul Layer per user:

```
config/
├── IDENTITY.md          (shared)
├── baseline.md          (shared)
├── soul/
│   ├── user_alice.md    (warmth: 7, humor: 4)
│   ├── user_bob.md      (warmth: 3, humor: 7)
│   └── user_charlie.md  (warmth: 5, humor: 5)
```

**Loading logic**:
```python
def load_soul(user_id):
    user_soul_file = f"config/soul/user_{user_id}.md"
    if exists(user_soul_file):
        return parse_soul(user_soul_file)
    else:
        # Initialize from baseline
        return copy_baseline_to_soul(user_id)
```

**Signal capture**: Tag signals with user_id:
```json
{"ts":"...","type":"preference","user":"alice","summary":"...", "intensity":4}
```

**Reflection**: Run separately per user's signal file

---

## Best Practices

### ✅ Do:
- Start with default values (5) for all dimensions
- Require consistent trends (≥3 days) before adjusting
- Implement rebound to prevent drift from temporary preferences
- Log all changes with evidence
- Test boundary enforcement
- Review changelog regularly for unexpected drift

### ❌ Don't:
- Allow unbounded drift (always enforce min/max)
- React to single signals (wait for trends)
- Adjust by more than ±1/day (prevents whiplash)
- Ignore rebound logic (dimensions will drift forever)
- Remove core dimensions (only self-discovered ones)
- Let self-discovered dimensions accumulate indefinitely (cap at 4)

---

## Troubleshooting

### Dimension Drifts Too Fast
- Increase trend requirement (3 days → 5 days)
- Decrease max drift rate (±1 → ±0.5)
- Increase signal intensity threshold (only count intensity ≥4)

### Dimension Won't Change
- Check if signals are being captured correctly
- Verify signals are classified to correct dimension
- Lower trend requirement (3 days → 2 days)
- Check boundary constraints (might be at limit)

### Unwanted Rebound
- Extend rebound window (14 days → 21 days)
- Check if signals are properly tagged to dimension
- User might genuinely want baseline behavior (rebound is correct)

### Persona Feels Unstable
- Implement drift rate limiting (max 2 dimensions/day)
- Increase trend requirement
- Add signal intensity weighting (favor intensity 4-5 signals)

---

## Summary

| Concept | Description | Example |
|---------|-------------|---------|
| **Dimension** | Behavioral trait on 1-10 scale | `warmth: 7` |
| **Drift** | Gradual adjustment based on signals | `warmth: 5 → 6` (+1/day) |
| **Rebound** | Return to baseline when unused | `warmth: 7 → 5` over 4 days |
| **Boundary** | Hard limit on dimension range | `warmth: [1-10]` |
| **Self-Discovery** | New dimensions from signal patterns | Discover `anticipation` |
| **Trend** | ≥3 days consistent signals | 3 days of "prefer brevity" |

**Key Insight**: Persona drift enables **growth without chaos**. The baseline anchors identity, the floating layer adapts to user, and rebound prevents runaway drift. It's personality with a safety net.

---

[← Signal Capture](signal-capture.md) | [README](../README.md) | [Daily Reflection →](daily-reflection.md)
