# Signal Capture

Signal capture is the foundation of Kairos—the mechanism by which agents "hear" and record behavioral cues from user interactions. Signals are **lightweight metadata** about what worked, what didn't, and how the user feels.

---

## Design Principles

1. **Non-intrusive**: Signal capture must not interrupt conversation flow
2. **Privacy-first**: Never log message content, only behavioral patterns
3. **Selective**: Capture clear signals, discard ambiguous ones
4. **Structured**: Use consistent schema for downstream analysis
5. **Real-time**: Write signals as they occur, don't batch

---

## Signal Types

Kairos defines **5 core signal types**:

### 1. Preference Signal
**When to capture**: User explicitly states a preference about how the agent should behave.

**Examples**:
- ✅ "Please just send me the link directly next time"
- ✅ "I don't need explanations, just the answer"
- ✅ "I like when you add emojis"
- ❌ "I prefer coffee" (not about agent behavior)

**Detection strategy**:
- Look for imperative phrases: "please do X", "don't do Y", "I prefer when you..."
- Look for evaluative language: "better", "worse", "I like", "I don't like"
- High confidence signals only (avoid false positives)

**Example signal**:
```json
{
  "ts": "2026-02-12T14:32:01",
  "type": "preference",
  "summary": "User prefers direct links without explanation",
  "context": "Provided a link with context paragraph",
  "intensity": 4
}
```

---

### 2. Emotion Signal
**When to capture**: User's emotional state is clearly expressed or inferred.

**Examples**:
- ✅ "Thanks so much! This is exactly what I needed!" (satisfaction, intensity 5)
- ✅ "This is frustrating" (frustration, intensity 4)
- ✅ "lol" (amusement, intensity 3)
- ❌ "ok" (neutral, too ambiguous)

**Detection strategy**:
- Sentiment analysis on user message (positive/negative/neutral)
- Exclamation marks, ALL CAPS, emojis as intensity amplifiers
- Threshold: Only capture emotions with intensity ≥ 3
- Track emotional transitions (e.g., frustrated → relieved)

**Example signal**:
```json
{
  "ts": "2026-02-12T16:45:22",
  "type": "emotion",
  "summary": "User frustrated (repeated misunderstanding)",
  "context": "Agent misunderstood request twice",
  "intensity": 5
}
```

---

### 3. Correction Signal
**When to capture**: User corrects the agent's behavior, knowledge, or assumption.

**Examples**:
- ✅ "No, X is not Y" (factual correction)
- ✅ "You misunderstood—I meant Z" (interpretation correction)
- ✅ "Don't do that, do this instead" (behavioral correction)
- ❌ "Actually, I changed my mind" (not a correction of agent)

**Detection strategy**:
- Look for negation phrases: "no", "not", "wrong", "incorrect"
- Look for clarification phrases: "actually", "I meant", "to clarify"
- Follow-up messages that contradict agent's previous statement
- High priority: Corrections are critical learning signals

**Example signal**:
```json
{
  "ts": "2026-02-12T10:15:00",
  "type": "correction",
  "summary": "User corrected: X is not Y (agent assumed wrong)",
  "context": "Agent suggested X is a type of Y",
  "intensity": 4
}
```

---

### 4. Approval Signal
**When to capture**: User explicitly approves, praises, or validates agent behavior.

**Examples**:
- ✅ "Perfect, thanks!" (approval, intensity 4)
- ✅ "Good job" (approval, intensity 3)
- ✅ "Exactly what I needed" (approval, intensity 5)
- ✅ 👍 emoji (approval, intensity 2)
- ❌ "ok" (too neutral, not clear approval)

**Detection strategy**:
- Look for praise words: "perfect", "great", "good", "nice", "exactly", "love it"
- Look for gratitude: "thanks", "thank you", "appreciate"
- Positive emojis: ✅, 👍, ❤️, 😊, 🎉
- Combine with context: what did agent just do?

**Example signal**:
```json
{
  "ts": "2026-02-12T20:15:33",
  "type": "approval",
  "summary": "User praised quick summary format",
  "context": "Provided bullet-point summary instead of paragraph",
  "intensity": 4
}
```

---

### 5. Style Signal
**When to capture**: User's communication style reveals preferences about interaction patterns.

**Examples**:
- ✅ User sends 5 short messages in a row → prefers brevity
- ✅ User mirrors agent's emoji usage → comfortable with emojis
- ✅ User switches to very formal language → prefers professional tone
- ✅ User responds immediately → high engagement, prefers real-time interaction

**Detection strategy**:
- Message length analysis (user prefers short vs. long)
- Response time patterns (immediate vs. delayed)
- Punctuation habits (formal vs. casual)
- Emoji usage (none, rare, frequent)
- Language complexity (simple vs. technical)
- Implicit signals—requires pattern analysis over multiple messages

**Example signal**:
```json
{
  "ts": "2026-02-12T18:22:10",
  "type": "style",
  "summary": "User sent 4 short messages consecutively (prefers brevity)",
  "context": "Agent sent one long paragraph, user broke response into short chunks",
  "intensity": 3
}
```

---

## Signal Schema

All signals use the same JSON structure:

```json
{
  "ts": "ISO-8601 timestamp",
  "type": "preference|emotion|correction|approval|style",
  "summary": "One-sentence description of the signal",
  "context": "What triggered this signal (optional)",
  "intensity": 1-5
}
```

### Field Definitions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `ts` | string | ✅ | ISO-8601 timestamp (e.g., "2026-02-12T14:32:01") |
| `type` | enum | ✅ | One of: preference, emotion, correction, approval, style |
| `summary` | string | ✅ | One-sentence description (max 100 chars) |
| `context` | string | ❌ | Optional background/trigger (max 150 chars) |
| `intensity` | integer | ✅ | Scale 1-5 (1=weak, 5=strong) |

### Intensity Scale

| Value | Meaning | Example |
|-------|---------|---------|
| 1 | Barely noticeable | Single "ok", mild sentiment |
| 2 | Slight signal | "thanks", 👍 emoji |
| 3 | Moderate signal | "good", "I prefer X", mild frustration |
| 4 | Strong signal | "Perfect!", "Don't do that", clear emotion |
| 5 | Extremely strong | "I LOVE this!", "STOP", explicit correction |

**Guideline**: When in doubt, default to intensity 3. Over-weighting signals can cause erratic persona drift.

---

## Storage Format: JSONL

Signals are stored as **newline-delimited JSON** (JSONL)—one signal per line.

### File Organization
```
memory/growth/signals/
├── 2026-02-10.jsonl
├── 2026-02-11.jsonl
├── 2026-02-12.jsonl
└── ...
```

Each day's signals in a separate file for easy management.

### Example File (`2026-02-12.jsonl`)
```json
{"ts":"2026-02-12T10:15:00","type":"correction","summary":"User corrected: X is not Y","context":"Agent assumed X was a type of Y","intensity":4}
{"ts":"2026-02-12T14:32:01","type":"preference","summary":"User prefers direct links without explanation","context":"Provided link with context paragraph","intensity":4}
{"ts":"2026-02-12T16:45:22","type":"emotion","summary":"User frustrated (repeated misunderstanding)","context":"Agent misunderstood request twice","intensity":5}
{"ts":"2026-02-12T18:22:10","type":"style","summary":"User sent 4 short messages consecutively","context":"Agent sent one long paragraph","intensity":3}
{"ts":"2026-02-12T20:15:33","type":"approval","summary":"User praised quick summary format","context":"Bullet-point summary provided","intensity":4}
```

### Advantages of JSONL
- ✅ **Streamable**: Process line-by-line without loading entire file
- ✅ **Append-friendly**: Add new signals with simple file append (no parsing/re-writing)
- ✅ **Human-readable**: Easy to inspect and debug
- ✅ **Tooling**: Standard format with wide library support

---

## Implementation Guide

### Pseudocode: Signal Detection

```python
def detect_signals(user_message, agent_response, conversation_context):
    signals = []
    
    # 1. Preference detection
    if contains_preference_keywords(user_message):
        signal = {
            "ts": now_iso8601(),
            "type": "preference",
            "summary": extract_preference(user_message),
            "context": agent_response_summary(agent_response),
            "intensity": calculate_intensity(user_message)
        }
        signals.append(signal)
    
    # 2. Emotion detection
    sentiment = analyze_sentiment(user_message)
    if sentiment.intensity >= 3:
        signal = {
            "ts": now_iso8601(),
            "type": "emotion",
            "summary": f"User {sentiment.label} ({sentiment.trigger})",
            "context": conversation_context.last_topic,
            "intensity": sentiment.intensity
        }
        signals.append(signal)
    
    # 3. Correction detection
    if is_correction(user_message, conversation_context):
        signal = {
            "ts": now_iso8601(),
            "type": "correction",
            "summary": extract_correction(user_message),
            "context": agent_response_summary(agent_response),
            "intensity": 4  # corrections are always high priority
        }
        signals.append(signal)
    
    # 4. Approval detection
    if contains_approval(user_message):
        signal = {
            "ts": now_iso8601(),
            "type": "approval",
            "summary": extract_approval(user_message),
            "context": conversation_context.last_agent_action,
            "intensity": calculate_approval_intensity(user_message)
        }
        signals.append(signal)
    
    # 5. Style detection (requires conversation history)
    style_signals = analyze_style_patterns(
        user_message, 
        conversation_context.recent_messages
    )
    signals.extend(style_signals)
    
    # Filter: max 3 signals per exchange (avoid over-capturing)
    return signals[:3]
```

### Pseudocode: Writing Signals

```python
def write_signal(signal, date=today()):
    signal_file = f"memory/growth/signals/{date}.jsonl"
    
    # Validate schema
    assert signal["type"] in ["preference", "emotion", "correction", "approval", "style"]
    assert 1 <= signal["intensity"] <= 5
    assert len(signal["summary"]) <= 100
    
    # Append to JSONL file (thread-safe)
    with open(signal_file, 'a') as f:
        f.write(json.dumps(signal) + '\n')
```

### Integration Pattern

```python
# In your agent's main conversation loop
user_message = get_user_input()
agent_response = generate_response(user_message)

# Non-blocking signal capture
signals = detect_signals(user_message, agent_response, context)
for signal in signals:
    write_signal(signal)  # Async write, doesn't block conversation

send_to_user(agent_response)
```

---

## Detection Strategies

### Strategy 1: Rule-Based Detection
**Best for**: Preference, Correction, Approval

Use keyword dictionaries and pattern matching:

```python
PREFERENCE_KEYWORDS = [
    "please", "prefer", "like when", "don't like", 
    "better if", "instead of", "just give me"
]

CORRECTION_PHRASES = [
    "no,", "not", "actually,", "wrong", "incorrect",
    "I meant", "to clarify", "you misunderstood"
]

APPROVAL_KEYWORDS = [
    "perfect", "great", "good", "excellent", "nice",
    "exactly", "love it", "well done", "thanks", "thank you"
]
```

**Advantages**: Fast, deterministic, easy to debug  
**Disadvantages**: Brittle, misses nuanced signals

---

### Strategy 2: LLM-Based Detection
**Best for**: Emotion, Style, nuanced signals

Prompt an LLM to analyze the conversation:

```python
prompt = f"""
Analyze this conversation exchange and identify behavioral signals:

User: "{user_message}"
Agent: "{agent_response}"

Detect signals of type: preference, emotion, correction, approval, style.
For each signal found, output JSON:
{{"type": "...", "summary": "...", "intensity": 1-5}}

Only output clear signals (confidence > 70%). Output "none" if no signals.
"""

llm_output = llm.generate(prompt)
signals = parse_llm_signals(llm_output)
```

**Advantages**: Catches nuanced signals, understands context  
**Disadvantages**: Slower, non-deterministic, requires API calls

---

### Strategy 3: Hybrid Approach ✅ Recommended
Combine both methods:
1. **Fast pass**: Rule-based detection for obvious signals (preference, correction, approval)
2. **Deep pass**: LLM-based detection for emotion and style (only if rule-based found nothing)

```python
signals = rule_based_detect(user_message, agent_response)

if len(signals) == 0 and should_use_llm(context):
    signals = llm_based_detect(user_message, agent_response, context)

return signals
```

---

## Best Practices

### ✅ Do:
- Capture signals immediately (don't batch)
- Validate schema before writing
- Use moderate intensity as default (3)
- Write clear, concise summaries
- Include context when available
- Limit to 3-5 signals per conversation to avoid noise

### ❌ Don't:
- Log full message content (privacy violation)
- Capture ambiguous signals (false positives are worse than false negatives)
- Over-weight intensity (avoid drift instability)
- Capture more than 10 signals per day per user (over-capturing)
- Store sensitive information (passwords, personal details)

---

## Privacy & Security

### Data Minimization
Signals should contain **only behavioral metadata**, never:
- Full message transcripts
- Personal identifiable information (PII)
- Passwords, API keys, secrets
- Location data
- Third-party names (unless public figures)

**Example of good signal**:
```json
{"type":"preference","summary":"User prefers bullet points","intensity":4}
```

**Example of bad signal** ❌:
```json
{"type":"preference","summary":"User John Smith from 123 Main St said he prefers bullet points when discussing his medical history","intensity":4}
```

### Retention Policy
- **Signals**: Keep indefinitely (small, anonymous metadata)
- **Conversation logs**: Optional (separate from signals, with user consent)
- **Daily reflections**: Keep indefinitely (audit trail)

### Access Control
- Signal files should be write-only by agent process
- Read access for reflection automation only
- No external API exposure

---

## Testing Signal Capture

### Unit Tests

```python
def test_preference_detection():
    message = "Please just send me the link next time"
    signal = detect_signals(message, context)
    assert signal["type"] == "preference"
    assert "link" in signal["summary"].lower()
    assert signal["intensity"] >= 3

def test_emotion_detection():
    message = "This is so frustrating!!!"
    signal = detect_signals(message, context)
    assert signal["type"] == "emotion"
    assert signal["intensity"] >= 4

def test_no_false_positives():
    message = "ok"
    signals = detect_signals(message, context)
    assert len(signals) == 0  # too ambiguous
```

### Manual Review
Periodically audit signal files:
```bash
# Check today's signals
cat memory/growth/signals/$(date +%Y-%m-%d).jsonl | jq .

# Count signals by type
cat memory/growth/signals/*.jsonl | jq -r .type | sort | uniq -c

# Find high-intensity signals
cat memory/growth/signals/*.jsonl | jq 'select(.intensity >= 4)'
```

---

## Advanced: Custom Signal Types

Extend Kairos with domain-specific signals:

```python
# Add new signal type
SIGNAL_TYPES = [
    "preference", "emotion", "correction", "approval", "style",
    "technical_depth",  # custom: user wants more/less technical detail
    "formality"         # custom: user adjusts formality level
]

# Detection logic
if user_says("can you explain that more simply"):
    signal = {
        "type": "technical_depth",
        "summary": "User requests simpler explanation",
        "intensity": 4
    }
```

Update reflection logic to handle new signal types.

---

## Troubleshooting

### Too Few Signals Captured
- Lower intensity threshold (capture intensity ≥ 2 instead of ≥ 3)
- Add more keywords to detection dictionaries
- Use LLM-based detection for nuanced signals

### Too Many Signals (Noise)
- Raise intensity threshold (only capture ≥ 4)
- Limit to 1-2 signals per conversation turn
- Increase specificity of detection rules

### False Positives
- Add negative keywords (e.g., "not really" negates approval)
- Require multiple confirming cues (keyword + sentiment + emoji)
- Manual review and filter adjustment

### Performance Impact
- Use async/background writing for signals
- Batch LLM calls if using LLM detection
- Consider sampling (only analyze 1 in N messages for style signals)

---

## Summary

| Signal Type | Trigger | Detection Method | Priority |
|-------------|---------|------------------|----------|
| Preference | Explicit statement | Rule-based (keywords) | High |
| Emotion | Sentiment expression | LLM or sentiment analysis | Medium |
| Correction | Negation/clarification | Rule-based + context | High |
| Approval | Praise/thanks | Rule-based (keywords + emoji) | Medium |
| Style | Implicit patterns | Pattern analysis | Low |

**Key Insight**: Signal capture is about **listening**, not **surveillance**. Capture only what's clearly expressed, respect privacy, and let the Growth Layer do the heavy lifting of interpretation.

---

[← Architecture](architecture.md) | [README](../README.md) | [Persona Drift →](persona-drift.md)
