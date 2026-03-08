"""Scenario selection, condition checking, and choice application."""

import random
from ..models.game import (
    GameState, ActiveScenario, ScenarioDefinition, ScenarioCondition,
    ScenarioChoice, ChoiceEffect, Tenant
)
from ..data.scenarios import SCENARIOS
from ..data.unlocks import get_unlock_level
from ..config import SCENARIO_INTERVAL_MIN, SCENARIO_INTERVAL_MAX


def try_queue_scenario(state: GameState) -> ActiveScenario | None:
    """Try to select and activate a scenario for the current game state."""
    if state.active_scenario is not None:
        return None
    if state.day < state.next_scenario_day:
        return None
    if not state.tenants:
        return None

    unlock = get_unlock_level(state.rep)
    max_tier = unlock["tier"]

    # Filter scenarios by tier and conditions
    candidates = []
    for s_data in SCENARIOS:
        if s_data["id"] in state.used_scenarios:
            continue
        if s_data["tier"] > max_tier:
            continue

        sd = _parse_scenario(s_data)

        # Check condition against each tenant
        for tenant in state.tenants:
            if check_condition(sd.cond, state, tenant):
                candidates.append((sd, tenant, s_data["weight"]))

    if not candidates:
        # Reset used scenarios if we've used 80%+
        tier_scenarios = [s for s in SCENARIOS if s["tier"] <= max_tier]
        if len(state.used_scenarios) >= len(tier_scenarios) * 0.8:
            state.used_scenarios = []
        return None

    # Weighted random selection
    total_weight = sum(c[2] for c in candidates)
    r = random.random() * total_weight
    cumulative = 0
    chosen_sd, chosen_tenant, _ = candidates[0]
    for sd, tenant, weight in candidates:
        cumulative += weight
        if r <= cumulative:
            chosen_sd = sd
            chosen_tenant = tenant
            break

    # Build description from template
    desc = chosen_sd.desc_template.format(
        name=chosen_tenant.name,
        unit=chosen_tenant.unit + 1,
        rent=chosen_tenant.rent,
        job=chosen_tenant.job,
        issue=random.choice(["faucet", "radiator", "window latch", "outlet", "ceiling fan"]),
    )

    active = ActiveScenario(
        definition=chosen_sd,
        tenant_id=chosen_tenant.id,
        tenant_name=chosen_tenant.name,
        description=desc,
    )

    state.active_scenario = active
    state.used_scenarios.append(chosen_sd.id)
    state.next_scenario_day = state.day + random.randint(SCENARIO_INTERVAL_MIN, SCENARIO_INTERVAL_MAX)

    return active


def check_condition(cond: ScenarioCondition, state: GameState, tenant: Tenant) -> bool:
    """Check if a scenario condition is met."""
    if cond.always:
        return True

    if cond.stat_below:
        for stat, threshold in cond.stat_below.items():
            val = getattr(tenant.stats, stat, None)
            if val is None or val >= threshold:
                return False

    if cond.stat_above:
        for stat, threshold in cond.stat_above.items():
            val = getattr(tenant.stats, stat, None)
            if val is None or val <= threshold:
                return False

    if cond.b_stat_below:
        for stat, threshold in cond.b_stat_below.items():
            val = getattr(state.building, stat, None)
            if val is None or val >= threshold:
                return False

    if cond.rep_above is not None and state.rep <= cond.rep_above:
        return False

    if cond.rep_below is not None and state.rep >= cond.rep_below:
        return False

    if cond.days_stayed_above is not None and tenant.days_stayed <= cond.days_stayed_above:
        return False

    return True


def apply_choice(state: GameState, choice_id: str) -> dict:
    """Apply a scenario choice's effects. Returns summary dict."""
    if not state.active_scenario:
        return {"error": "No active scenario"}

    scenario = state.active_scenario
    definition = scenario.definition

    # Find the choice
    choice = None
    for c in definition.choices:
        if c.id == choice_id:
            choice = c
            break

    if not choice:
        return {"error": f"Choice {choice_id} not found"}

    # Find the tenant
    tenant = None
    for t in state.tenants:
        if t.id == scenario.tenant_id:
            tenant = t
            break

    if not tenant:
        return {"error": "Tenant not found"}

    # Apply effects
    state.rep = max(0, state.rep + choice.rep)
    state.money += choice.money

    fx = choice.fx
    tenant.stats.happiness = _clamp(tenant.stats.happiness + fx.t_happiness)
    tenant.stats.finances = _clamp(tenant.stats.finances + fx.t_finances)
    tenant.stats.social = _clamp(tenant.stats.social + fx.t_social)
    tenant.stats.health = _clamp(tenant.stats.health + fx.t_health)
    tenant.stats.stability = _clamp(tenant.stats.stability + fx.t_stability)
    tenant.stats.suspicion = _clamp(tenant.stats.suspicion + fx.t_suspicion)

    state.building.maintenance = _clamp(state.building.maintenance + fx.b_maintenance)
    state.building.safety = _clamp(state.building.safety + fx.b_safety)
    state.building.noise = _clamp(state.building.noise + fx.b_noise)
    state.building.appeal = _clamp(state.building.appeal + fx.b_appeal)
    state.building.happiness = _clamp(state.building.happiness + fx.b_happiness)

    # Add to tenant memory
    tenant.memory.append(f"Day {state.day}: {definition.title} — {choice.label}")

    # Log
    narration = choice.narration.replace("{name}", tenant.name)
    state.log.append(f"Day {state.day}: [{definition.title}] {choice.label}")

    # Clear active scenario
    state.active_scenario = None

    return {
        "narration": narration,
        "rep_change": choice.rep,
        "money_change": choice.money,
        "tenant_name": tenant.name,
        "choice_label": choice.label,
    }


def _parse_scenario(data: dict) -> ScenarioDefinition:
    """Parse a raw scenario dict into a ScenarioDefinition."""
    cond = ScenarioCondition(**(data.get("cond", {"always": True})))
    choices = []
    for c in data.get("choices", []):
        fx = ChoiceEffect(**c.get("fx", {}))
        choices.append(ScenarioChoice(
            id=c["id"],
            label=c["label"],
            desc=c.get("desc", ""),
            rep=c.get("rep", 0),
            money=c.get("money", 0),
            fx=fx,
            narration=c.get("narration", ""),
        ))
    return ScenarioDefinition(
        id=data["id"],
        tier=data["tier"],
        title=data["title"],
        weight=data.get("weight", 5),
        cond=cond,
        desc_template=data.get("desc_template", ""),
        choices=choices,
    )


def _clamp(val: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, val))
