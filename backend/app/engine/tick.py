"""Main game loop tick — advance day, tick building, collect rent."""

import random
import math
from ..models.game import GameState, MaintenanceTask
from .tenants import tick_tenants, make_tenant
from ..data.unlocks import get_unlock_level
from ..data.archetypes import ARCHETYPES
from ..config import RENT_CYCLE_DAYS

TASK_TYPES = [
    {"kind": "dripping_pipe",    "label": "Dripping Pipe",    "icon": "🔧", "cost_range": (10, 25)},
    {"kind": "flickering_light", "label": "Flickering Light", "icon": "💡", "cost_range": (0, 15)},
    {"kind": "cracked_step",     "label": "Cracked Step",     "icon": "🪜", "cost_range": (10, 20)},
    {"kind": "loose_railing",    "label": "Loose Railing",    "icon": "🔩", "cost_range": (0, 15)},
    {"kind": "squeaky_door",     "label": "Squeaky Door",     "icon": "🚪", "cost_range": (0, 10)},
    {"kind": "broken_mailbox",   "label": "Broken Mailbox",   "icon": "📬", "cost_range": (0, 15)},
    {"kind": "peeling_paint",    "label": "Peeling Paint",    "icon": "🖌️", "cost_range": (0, 10)},
    {"kind": "clogged_drain",    "label": "Clogged Drain",    "icon": "🪠", "cost_range": (5, 20)},
]
MAX_TASKS = 6


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

    # Spawn maintenance tasks
    spawn_maintenance_tasks(state)

    # Collect rent
    if state.day % RENT_CYCLE_DAYS == 0:
        rent_logs = collect_rent(state)
        log.extend(rent_logs)

    # Check unlocks
    unlock = get_unlock_level(state.rep)
    if unlock["units"] > state.unlocked_units:
        state.unlocked_units = unlock["units"]
        log.append(f"Day {state.day}: A new unit has opened up! You now have {state.unlocked_units} units available.")

    # Fill vacant unlocked units with new tenants (one per day, with a delay)
    move_in_logs = try_move_in(state)
    log.extend(move_in_logs)

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


def try_move_in(state: GameState) -> list[str]:
    """Try to move a new tenant into a vacant unlocked unit. One per day max."""
    log = []
    # Find vacant unlocked units
    vacant = []
    for i in range(state.unlocked_units):
        if state.units[i] is None:
            vacant.append(i)

    if not vacant:
        return log

    # 50% chance each day a new tenant shows up (feels organic, not instant)
    if random.random() > 0.5:
        return log

    unit = vacant[0]

    # Pick an archetype not already in the building
    current_archetypes = {t.archetype for t in state.tenants}
    available = [a["key"] for a in ARCHETYPES if a["key"] not in current_archetypes]
    if not available:
        available = [a["key"] for a in ARCHETYPES]

    tenant = make_tenant(unit=unit, archetype_key=random.choice(available))
    state.tenants.append(tenant)
    state.units[unit] = tenant.id
    log.append(f"Day {state.day}: {tenant.name} moved into unit {unit + 1}.")

    return log


def spawn_maintenance_tasks(state: GameState) -> None:
    """Spawn 1-3 new maintenance tasks if below the cap."""
    if len(state.maintenance_tasks) >= MAX_TASKS:
        return

    count = random.randint(1, 3)
    count = min(count, MAX_TASKS - len(state.maintenance_tasks))

    for _ in range(count):
        t = random.choice(TASK_TYPES)

        # Find a position that doesn't overlap existing tasks
        for _ in range(10):
            x = random.uniform(0.08, 0.92)
            y = random.uniform(0.08, 0.92)
            too_close = any(
                math.hypot(x - et.x, y - et.y) < 0.15
                for et in state.maintenance_tasks
            )
            if not too_close:
                break

        task = MaintenanceTask(
            kind=t["kind"],
            label=t["label"],
            icon=t["icon"],
            x=x,
            y=y,
            rep_reward=random.randint(1, 3),
            maint_reward=random.randint(2, 5),
            money_cost=random.randint(*t["cost_range"]),
            spawned_day=state.day,
        )
        state.maintenance_tasks.append(task)


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
