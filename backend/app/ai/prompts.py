"""Prompt templates for Haiku AI generation."""

SYSTEM_PROMPT = """You are the narrator of an indie apartment building simulation game called The Bramble.
You write short, atmospheric, slightly wry prose. Dry humor. Observational. Never preachy, never sentimental.
You sound like a Raymond Carver story crossed with a building superintendent's incident report.
1-2 sentences max. Never break character. Never use game terminology or stats."""

FLAVOR_TEMPLATE = """Generate atmospheric flavor text for this scenario.

Building: The Bramble, Day {day}. Maintenance: {maintenance}%. {weather}.
Tenant: {name}, {age}, {job}. Unit {unit}. Been here {days_stayed} days.
Their mood: {mood}.
Situation: {title} — {description}

Write ONLY 1-2 sentences of atmospheric scene-setting. No dialogue. No action. Just atmosphere."""

NARRATION_TEMPLATE = """Narrate the consequence of this decision.

Scenario: {title}
Tenant: {name}, {job}, unit {unit}.
Player chose: {choice_label} — {choice_desc}
What happened: {narration_hint}

Rewrite the consequence in 1-2 sentences. Same facts, better prose. Atmospheric, specific, slightly wry."""

WEATHER_OPTIONS = [
    "Rain on the windows.",
    "Clear night. Cold.",
    "Humid. The hallway smells like old carpet.",
    "Gray morning. Coffee weather.",
    "Wind rattling the fire escape.",
    "Late afternoon sun through dirty glass.",
    "First snow. The radiators are working overtime.",
    "Overcast. The kind of day where nothing starts.",
]
