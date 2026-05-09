def comparison_prompt(summary):  
    """Generate structured comparison prompt for LLM."""
    return f"""
Battery degradation comparison:

{summary}

CRITICAL:
- Max 180–220 words
- Must include BOTH numbers and engineering reasoning
- Explain trends using known battery physics (even if slightly general)
- Link physical explanation to observed data

OUTPUT FORMAT:

Fastest group:
<group name + value>

Comparison:
<2–3 sentences with numeric comparison>

Physical reason:
<2–3 sentences combining data + known physics>

Reliability:
<1–2 sentences (std, sample size)>

Engineering action:
<2–3 practical insights>
"""


def single_battery_prompt(selected, initial, final, fade, cycles, temp, load_type, load_level):
    """Generate single battery analysis prompt."""
    return f"""
Battery Analysis Report

Battery ID: {selected}

Measured Data:
- Total cycles: {cycles}
- Initial capacity: {initial:.3f}
- Final capacity: {final:.3f}
- Capacity fade: {fade:.3f}

Conditions:
- Temperature: {temp}
- Load type: {load_type}
- Load level: {load_level}

CRITICAL:
- Max 180–220 words
- Include some general battery knowledge if helpful
- BUT always connect to measured values
- If capacity increases → treat as anomaly
- If anomaly exists, explain possible causes clearly

OUTPUT FORMAT:

Degradation summary:
<2–3 sentences>

Physical explanation:
<2–3 sentences (data + physics)>

Classification:
<slow / moderate / fast / anomaly>

Reliability:
<1–2 sentences>

Engineering insight:
<2–3 practical recommendations>
"""