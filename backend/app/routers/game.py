"""Game routes: new game, get state, advance day."""

import random
from fastapi import APIRouter, HTTPException
from ..models.game import GameState
from ..engine.tenants import make_tenant
from ..engine.tick import advance_day
from ..engine.scenarios import try_queue_scenario
from ..ai.generate import generate_flavor_text
from ..config import STARTING_MONEY, STARTING_REP, STARTING_UNITS
from ..data.archetypes import ARCHETYPES

router = APIRouter()

# In-memory game store (single game for MVP)
_game: GameState | None = None


def get_game() -> GameState:
    global _game
    if _game is None:
        raise HTTPException(status_code=404, detail="No active game. Start a new one.")
    return _game


@router.post("/new")
async def new_game():
    """Create a new game with starting tenants."""
    global _game
    state = GameState(
        money=STARTING_MONEY,
        rep=STARTING_REP,
        unlocked_units=STARTING_UNITS,
    )

    # Pick 3 distinct archetypes for starting tenants
    starting_archetypes = random.sample(
        [a["key"] for a in ARCHETYPES],
        k=STARTING_UNITS,
    )

    for i, arch_key in enumerate(starting_archetypes):
        tenant = make_tenant(unit=i, archetype_key=arch_key)
        state.tenants.append(tenant)
        state.units[i] = tenant.id

    state.log.append(f"Day 1: Welcome to The Bramble. {len(state.tenants)} tenants. ${state.money} in the bank.")
    _game = state
    return state.model_dump()


@router.get("/state")
async def get_state():
    """Get current game state."""
    state = get_game()
    return state.model_dump()


@router.post("/advance")
async def advance():
    """Advance the game by one day."""
    state = get_game()

    if state.phase != "playing":
        return state.model_dump()

    # Advance day (tick tenants, building, rent, etc.)
    day_log = advance_day(state)

    # Try to trigger a scenario
    scenario = try_queue_scenario(state)
    flavor_text = ""
    if scenario:
        flavor_text = await generate_flavor_text(state, scenario)
        scenario.flavor_text = flavor_text

    return {
        **state.model_dump(),
        "day_log": day_log,
        "flavor_text": flavor_text,
    }
