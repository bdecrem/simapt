"""AI generation functions for flavor text and narration."""

import random
from .client import call_haiku
from .prompts import SYSTEM_PROMPT, FLAVOR_TEMPLATE, NARRATION_TEMPLATE, WEATHER_OPTIONS
from ..models.game import GameState, ActiveScenario


FALLBACK_FLAVOR = [
    "The hallway light flickers. It always does around this time.",
    "Someone left a coffee cup on the stairs. Third one this week.",
    "The building settles. Old bones, old sounds.",
    "A door closes somewhere above. Then silence.",
    "The radiator clicks twice. A pipe answers from the wall.",
    "Footsteps in the stairwell. They stop at the second floor.",
    "The lobby smells like someone's dinner. Something with garlic.",
    "A car idles outside. Its headlights reach the third floor windows.",
]


async def generate_flavor_text(state: GameState, scenario: ActiveScenario) -> str:
    """Generate atmospheric flavor text for a scenario card."""
    tenant = next((t for t in state.tenants if t.id == scenario.tenant_id), None)
    if not tenant:
        return random.choice(FALLBACK_FLAVOR)

    h = tenant.stats.happiness
    mood = "good" if h > 60 else "rough" if h < 30 else "neutral"

    prompt = FLAVOR_TEMPLATE.format(
        day=state.day,
        maintenance=state.building.maintenance,
        weather=random.choice(WEATHER_OPTIONS),
        name=tenant.name,
        age=tenant.age,
        job=tenant.job,
        unit=tenant.unit + 1,
        days_stayed=tenant.days_stayed,
        mood=mood,
        title=scenario.definition.title,
        description=scenario.description,
    )

    result = await call_haiku(SYSTEM_PROMPT, prompt)
    return result or random.choice(FALLBACK_FLAVOR)


async def generate_narration(state: GameState, scenario: ActiveScenario, choice_id: str) -> str:
    """Generate consequence narration after a player's choice."""
    definition = scenario.definition
    choice = next((c for c in definition.choices if c.id == choice_id), None)
    if not choice:
        return "Something changed. You're not sure what."

    tenant = next((t for t in state.tenants if t.id == scenario.tenant_id), None)
    if not tenant:
        return choice.narration

    prompt = NARRATION_TEMPLATE.format(
        title=definition.title,
        name=tenant.name,
        job=tenant.job,
        unit=tenant.unit + 1,
        choice_label=choice.label,
        choice_desc=choice.desc,
        narration_hint=choice.narration.replace("{name}", tenant.name),
    )

    result = await call_haiku(SYSTEM_PROMPT, prompt)
    return result or choice.narration.replace("{name}", tenant.name)
