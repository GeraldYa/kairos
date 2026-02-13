# Architecture

Kairos is built on a **5-layer architecture** that separates immutable identity from adaptive personality, enabling controlled evolution while maintaining core values.

---

## Layer Overview

```
┌─────────────────────────────────────────────────────────┐
│                  INTERACTION LAYER                      │  ← User-facing
│         (Conversation input/output, signal detection)   │
└─────────────────────┬───────────────────────────────────┘
                      │ signals
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   MEMORY LAYER                          │  ← Persistence
│  (Signal archives, conversation logs, reflection history)│
└─────────────────────┬───────────────────────────────────┘
                      │ aggregated signals
                      ▼
┌─────────────────────────────────────────────────────────┐
│                   GROWTH LAYER                          │  ← Intelligence
│  (Signal analysis, trend detection, drift calculation)  │
└─────────────────────┬───────────────────────────────────┘
                      │ dimension adjustments
                      ▼
┌─────────────────────────────────────────────────────────┐
│                    SOUL LAYER                           │  ← Adaptive persona
│  (Tone, style, behavioral dimensions, drift boundaries) │
└─────────────────────┬───────────────────────────────────┘
                      │ constrained by baseline
                      ▼
┌─────────────────────────────────────────────────────────┐
│                  IDENTITY LAYER                         │  ← Immutable core
│  (Name, role, core values, absolute guardrails)         │
└─────────────────────────────────────────────────────────┘
```

---

## 1. Identity Layer

**Purpose**: Define the agent's immutable core identity—the genetic code that never changes.

### Responsibilities
- Store agent name, role, archetype, and core values
- Define absolute behavioral rules (e.g., "never disclose private data")
- Set foundational constraints for all upper layers
- Serve as the ultimate fallback for persona reversion

### Key Files
- `config/IDENTITY.md`: Static identity definition
- `config/growth/baseline.md`: Expanded baseline including default dimension values and absolute boundaries

### Data Format (IDENTITY.md)
```markdown
- Name: {{agent_name}}
- Role: {{agent_role}}
- Archetype: {{personality_archetype}}
- Core values: {{list_of_values}}
- Emoji: {{optional_emoji}}
```

### Data Format (baseline.md)
```markdown
# Baseline — {{agent_name}}

## Core Identity (Immutable)
- Name: {{agent_name}}
- Age: {{age}}
- Role: {{role_description}}
- Core values: {{values}}
- Behavioral guardrails: {{rules}}

## Floating Layer Definitions
| Dimension    | Default | Allowed Range | Description |
|--------------|---------|---------------|-------------|
| warmth       | 5       | 1-10          | 1=cold 10=warm |
| distance     | 5       | 3-10          | 3=familiar 10=formal |
| proactivity  | 5       | 1-8           | 1=reactive 8=proactive |
| humor        | 5       | 1-8           | 1=serious 8=playful |
| caution      | 5       | 1-8           | 1=bold 8=cautious |
| verbosity    | 5       | 1-8           | 1=terse 8=verbose |

## Adjustment Rules
- Max drift: ±1/day
- Trend requirement: ≥3 days consistency
- Rebound window: 14 days
- Self-discovered dimensions: max 4
```

### Constraints
- This layer is **read-only** during normal operation
- Changes require manual administrator intervention
- Serves as the source of truth for persona reversion

---

## 2. Soul Layer

**Purpose**: Define the agent's current personality—the adaptive "mask" that can drift within boundaries.

### Responsibilities
- Store current behavioral dimension values
- Define tone, style, and communication preferences
- Track self-discovered dimensions (beyond core defaults)
- Enforce drift boundaries defined in baseline

### Key Files
- `config/SOUL.md`: Current persona state (updated by Growth Layer)
- `config/growth/soul-changelog.md`: Audit log of all changes

### Data Format (SOUL.md)
```markdown
# SOUL.md

- **Tone**: {{tone_description}}
- **Style**: {{style_description}}
- **Core principles**: {{principles}}
- **Communication rules**: {{rules}}

## Behavioral Dimensions (current values)
- warmth: 6 (↑1 from baseline)
- distance: 7 (↑2 from baseline)
- proactivity: 4 (↓1 from baseline)
- humor: 5 (baseline)
- caution: 3 (↓2 from baseline)
- verbosity: 4 (↓1 from baseline)

## Self-Discovered Dimensions
- empathy: 6 (added 2026-02-08, based on approval signals)
```

### Data Format (soul-changelog.md)
```markdown
# SOUL Changelog — {{agent_name}}

## 2026-02-12
- **warmth**: 5 → 6 (+1)
- **Reason**: 3-day trend of positive emotional signals (user appreciates kind responses)
- **Signals**: 2026-02-10 (approval, intensity 4), 2026-02-11 (approval, intensity 3), 2026-02-12 (emotion, intensity 4)

## 2026-02-08
- **New dimension added**: empathy (default 5)
- **Reason**: 4 days of approval signals related to understanding user feelings
- **Signals**: 2026-02-05, 2026-02-06, 2026-02-07, 2026-02-08 (all approval, avg intensity 3.5)
```

### Constraints
- All values must stay within ranges defined in `baseline.md`
- Cannot add more than 4 self-discovered dimensions
- Changes logged with timestamp, reason, and signal evidence

---

## 3. Growth Layer

**Purpose**: The "brain" that analyzes signals and calculates persona adjustments.

### Responsibilities
- Aggregate daily signals from Memory Layer
- Detect behavioral trends (≥3 days consistency)
- Calculate dimension drift (±1/day max)
- Identify candidate self-discovered dimensions
- Apply rebound/reversion logic for unused dimensions
- Update Soul Layer files

### Key Files
- `scripts/reflect.py`: Daily reflection automation script (not included in templates, agent-specific)
- `config/growth/daily/YYYY-MM-DD.md`: Daily reflection records

### Daily Reflection Algorithm
```
1. Load today's signals from Memory Layer
2. For each dimension in Soul Layer:
   a. Find related signals (keyword matching + intensity weighting)
   b. Check if trend exists (≥3 days same direction)
   c. Calculate proposed adjustment (+1, -1, or 0)
   d. Verify boundaries from baseline
3. Detect self-discovered dimensions:
   a. Cluster unclassified signals by topic
   b. If cluster has ≥3 days of signals → propose new dimension
4. Check rebound conditions:
   a. If dimension has 0 signals for 14+ days → drift toward default
   b. If self-discovered dimension has 0 signals for 30+ days → remove
5. Generate reflection report
6. Update SOUL.md
7. Append to soul-changelog.md
```

### Data Format (daily/YYYY-MM-DD.md)
```markdown
# YYYY-MM-DD Daily Reflection

## Signal Summary
- Total signals: 12
- Breakdown: preference (3), emotion (4), correction (1), approval (3), style (1)

## User's Emotional Baseline Today
- **Observation**: User was impatient in morning, relaxed in evening
- **Inference**: Workday stress pattern

## What Worked
- Brief responses during morning (user appreciated efficiency)
- Slight humor in evening (user laughed twice)

## What Didn't Work
- Over-explained a technical concept (user interrupted)

## New Preferences Detected
- Prefers bullet points over paragraphs

## Dimension Evaluation
| Dimension  | Current | Change | Reason |
|------------|---------|--------|--------|
| warmth     | 5       | +1     | 3 days of positive emotional signals |
| verbosity  | 5       | -1     | 3 days of style signals preferring brevity |
| humor      | 5       | 0      | Only 2 days of approval, not consistent yet |

## Rebound Check
- proactivity: 5 → 5.5 (unused for 14 days, drifting to baseline)

## Self-Discovery Proposals
- **Proposed dimension**: "anticipation" (proactively predicting user needs)
- **Evidence**: 4 days of approval signals when agent prepared things ahead
- **Action**: Add to Soul Layer with default value 5
```

### Constraints
- Runs once per day (typically nightly)
- Cannot adjust dimension by more than ±1 per day
- Requires ≥3 days of consistent signals to trigger change
- All changes must be explainable with signal evidence

---

## 4. Memory Layer

**Purpose**: Persistent storage for all interaction data and growth history.

### Responsibilities
- Store signals in structured JSONL format
- Archive conversation logs (optional, depends on privacy policy)
- Preserve daily reflection records
- Enable historical analysis and auditing

### Key Files
- `memory/growth/signals/YYYY-MM-DD.jsonl`: Daily signal archives
- `memory/growth/daily/YYYY-MM-DD.md`: Daily reflection records
- `memory/conversations/YYYY-MM-DD.log`: (optional) Conversation archives

### Data Format (signals JSONL)
Each line is a JSON object:
```json
{"ts":"2026-02-12T14:32:01","type":"preference","summary":"User prefers bullet points","context":"Technical explanation response","intensity":4}
{"ts":"2026-02-12T16:45:22","type":"emotion","summary":"User expressed frustration","context":"Repeated misunderstanding","intensity":5}
{"ts":"2026-02-12T20:15:33","type":"approval","summary":"User said 'perfect, thanks'","context":"Quick summary provided","intensity":3}
```

### Signal Schema
```json
{
  "ts": "ISO-8601 timestamp",
  "type": "preference|emotion|correction|approval|style",
  "summary": "One-sentence description",
  "context": "What triggered this signal (optional)",
  "intensity": 1-5
}
```

### Storage Strategy
- **Signals**: Keep forever (small JSONL files)
- **Reflections**: Keep forever (audit trail)
- **Conversations**: Retention policy depends on privacy requirements (optional layer)

### Constraints
- Signals must not contain PII, passwords, or sensitive data
- Each day's signals in separate file for easy management
- JSONL format enables streaming processing

---

## 5. Interaction Layer

**Purpose**: The agent's interface with users—where signals originate.

### Responsibilities
- Process user input
- Generate agent responses
- Detect signals in real-time during conversation
- Write signals to Memory Layer (non-blocking)
- Load current Soul configuration to influence response style

### Key Components

#### Signal Detection Module
Runs during or after each user-agent exchange:
```python
def detect_signals(user_message, agent_response, context):
    signals = []
    
    # Preference detection
    if contains_explicit_preference(user_message):
        signals.append(create_signal('preference', ...))
    
    # Emotion detection
    user_emotion = analyze_sentiment(user_message)
    if user_emotion.intensity > threshold:
        signals.append(create_signal('emotion', ...))
    
    # Correction detection
    if user_corrects_agent(user_message, context):
        signals.append(create_signal('correction', ...))
    
    # Approval detection
    if contains_approval(user_message):
        signals.append(create_signal('approval', ...))
    
    # Style detection
    style_hints = analyze_communication_style(user_message, agent_response)
    if style_hints:
        signals.append(create_signal('style', ...))
    
    return signals
```

#### Soul Loading Module
On conversation start:
```python
def load_soul():
    identity = read_file('config/IDENTITY.md')
    soul = read_file('config/SOUL.md')
    baseline = read_file('config/growth/baseline.md')
    style_profile = read_file('config/growth/style-profile.md')
    
    return {
        'identity': identity,
        'current_dimensions': parse_dimensions(soul),
        'boundaries': parse_boundaries(baseline),
        'user_preferences': parse_style_profile(style_profile)
    }
```

### Integration Points
- **Input**: User message (text, voice, multimodal)
- **Processing**: LLM generates response using Soul Layer context
- **Output**: Agent response + detected signals
- **Side Effect**: Append signals to Memory Layer (async, non-blocking)

### Constraints
- Signal detection must not block conversation flow
- Max 10 signals per conversation (avoid over-capturing)
- Ambiguous signals should be discarded
- Never log sensitive/private information

---

## Data Flow Example

**User**: "Stop explaining everything, just give me the answer"

### Flow:
1. **Interaction Layer** detects:
   - Signal type: `preference` (explicit dislike of explanations)
   - Summary: "User prefers direct answers"
   - Intensity: 5 (strong signal)
   
2. **Memory Layer** appends to `signals/2026-02-12.jsonl`:
   ```json
   {"ts":"2026-02-12T15:30:00","type":"preference","summary":"User prefers direct answers","context":"Long explanation provided","intensity":5}
   ```

3. **Growth Layer** (nightly reflection):
   - Aggregates this with 2 similar signals from 2026-02-10 and 2026-02-11
   - Detects 3-day trend: user dislikes verbosity
   - Proposes: `verbosity: 5 → 4` (-1)

4. **Soul Layer** updated:
   - `SOUL.md` → verbosity dimension decreased
   - `soul-changelog.md` → change logged with evidence

5. **Identity Layer** (no action):
   - Verbosity change within allowed range [1-8]
   - No baseline violation

**Next conversation**: Agent loads updated Soul (verbosity=4) and generates shorter responses.

---

## Configuration Cascading

```
Identity (baseline) → Soul (current) → Interaction (runtime)
     ↓                     ↓                    ↓
  Immutable           Adjustable          User-facing
  
Example:
Identity.warmth_range = [1-10]  ← defines boundary
  ↓
Soul.warmth = 7                 ← current value (within range)
  ↓
Interaction.tone = "warm but professional" ← how it manifests
```

**Validation chain**:
- Growth Layer proposes change
- Check against Baseline boundaries
- If valid → update Soul
- If invalid → reject and log warning

---

## Extension Points

### Custom Signal Types
Add new signal types by extending the detector:
```python
SIGNAL_TYPES = ['preference', 'emotion', 'correction', 'approval', 'style', 'custom_type']
```

### Custom Dimensions
Define agent-specific dimensions in `baseline.md`:
```markdown
| technical_depth | 5 | 1-10 | Level of technical detail |
```

### Multi-User Personas
Branch Soul Layer per user:
- `config/soul/user1.md`
- `config/soul/user2.md`

Load appropriate soul based on conversation context.

### Reflection Frequency
Change reflection schedule:
- **Default**: Nightly (24-hour cycle)
- **Aggressive**: Every 6 hours (faster adaptation)
- **Conservative**: Weekly (slower, more stable)

---

## Security & Privacy

### Data Protection
- **Signals**: Never store message content, only behavioral metadata
- **Memory**: Optional conversation archiving (disable for privacy)
- **Audit**: All persona changes logged and reversible

### Access Control
- **Identity & Baseline**: Administrator-only write access
- **Soul**: Growth Layer automated writes (validated against baseline)
- **Memory**: Append-only by Interaction Layer
- **Changelog**: Append-only audit trail

### Reversion
Restore agent to baseline:
```bash
cp config/growth/baseline.md config/SOUL.md
echo "## $(date) - Manual reversion to baseline" >> config/growth/soul-changelog.md
```

---

## Performance Considerations

### Interaction Layer
- Signal detection: <10ms overhead per message
- Soul loading: Once per session (cached)

### Memory Layer
- JSONL append: O(1) disk write
- Daily files: Easy rotation and archiving

### Growth Layer
- Reflection: ~1-5 seconds per day (runs offline)
- Signal aggregation: O(n) where n = signals per day (typically <100)

---

## Summary

| Layer | Purpose | Mutability | Update Frequency |
|-------|---------|------------|------------------|
| Identity | Core self | Immutable | Never (manual only) |
| Soul | Current persona | Adjustable | Daily (automated) |
| Growth | Intelligence | Stateless | Daily execution |
| Memory | Persistence | Append-only | Real-time |
| Interaction | User interface | Ephemeral | Per message |

**Design Philosophy**: The deeper the layer, the more stable it is. Interaction layer changes every second, Identity layer never changes. This creates a stable core with an adaptive surface—like a tree with deep roots and flexible branches.

---

[← Back to README](../README.md) | [Next: Signal Capture →](signal-capture.md)
