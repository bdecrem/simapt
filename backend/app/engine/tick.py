"""Main game loop tick — advance day, tick building, collect rent."""

import random
from ..models.game import GameState
from .tenants import tick_tenants
from ..data.unlocks import get_unlock_level
from ..config import RENT_CYCLE_DAYS


def advance_day(state: GameState) -> list[str]:
    """Advance the game by one day. Returns log entries."""
    state.day += 1
    log = []

    # Tick tenants
    tenant_logs = tick_tenants(state.tenants, state.day)
    log.extend(tenant_logs)

    # Remove departed tenants
    departed = [t for t in state.tenants if t.leaving and t.leave_day and state.day >= t.leave_day]
    for t in departed:
        state.units[t.unit] = None
    state.tenants = [t for t in state.tenants if not (t.leaving and t.leave_day and state.day >= t.leave_day)]

    # Tick building
    building_logs = tick_building(state)
    log.extend(building_logs)

    # Collect rent
    if state.day % RENT_CYCLE_DAYS == 0:
        rent_logs = collect_rent(state)
        log.extend(rent_logs)

    # Check unlocks
    unlock = get_unlock_level(state.rep)
    if unlock["units"] > state.unlocked_units:
        state.unlocked_units = unlock["units"]
        log.append(f"Day {state.day}: A new unit has opened up! You now have {state.unlocked_units} units available.")

    # Check win/lose
    if state.rep >= 1000:
        state.phase = "won"
        log.append(f"Day {state.day}: The Bramble has achieved legendary status!")
    elif state.money < 0:
        state.phase = "lost"
        log.append(f"Day {state.day}: You've gone bankrupt. The building is lost.")
    elif len(state.tenants) == 0 and state.day > 10:
        state.phase = "lost"
        log.append(f"Day {state.day}: The building is empty. No one wants to live here anymore.")

    state.log.extend(log)
    return log


def tick_building(state: GameState) -> list[str]:
    """Decay building stats each day."""
    log = []
    b = state.building

    # Maintenance decays
    b.maintenance = max(0, b.maintenance - random.randint(0, 1))

    # Safety degrades with low maintenance
    if b.maintenance < 30:
        b.safety = max(0, b.safety - 1)
        if random.random() < 0.1:
            log.append(f"Day {state.day}: A pipe burst on the third floor.")
            b.maintenance = max(0, b.maintenance - 10)
            state.money -= 100

    # Building happiness from tenant happiness
    if state.tenants:
        avg_happy = sum(t.stats.happiness for t in state.tenants) / len(state.tenants)
        b.happiness = int(avg_happy * 0.7 + b.happiness * 0.3)

    # Noise decays toward 20
    if b.noise > 20:
        b.noise = max(20, b.noise - 1)

    return log


def collect_rent(state: GameState) -> list[str]:
    """Collect rent from all tenants."""
    log = []
    total = 0
    for t in state.tenants:
        if t.stats.finances > 15:
            state.money += t.rent
            total += t.rent
        else:
            log.append(f"Day {state.day}: {t.name} couldn't pay rent this month.")
    if total > 0:
        log.append(f"Day {state.day}: Collected ${total} in rent.")
    return log
