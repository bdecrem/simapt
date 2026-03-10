"""Game routes: new game, get state, advance day."""

import random
import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from ..models.game import GameState
from ..engine.tenants import make_tenant
from ..engine.tick import advance_day
from ..engine.scenarios import try_queue_scenario
from ..ai.generate import generate_flavor_text
from ..config import STARTING_MONEY, STARTING_REP, STARTING_UNITS
from ..data.archetypes import ARCHETYPES
from ..database import save_game
from ..dependencies import get_game_from_token

router = APIRouter()


@router.post("/new")
async def new_game():
    """Create a new game with starting tenants."""
    token = uuid.uuid4().hex[:24]
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
    save_game(token, state)
    return {"token": token, **state.model_dump()}


@router.get("/state")
async def get_state(game: tuple = Depends(get_game_from_token)):
    """Get current game state."""
    token, state = game
    return state.model_dump()


@router.post("/advance")
async def advance(game: tuple = Depends(get_game_from_token)):
    """Advance the game by one day."""
    token, state = game

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

    save_game(token, state)

    return {
        **state.model_dump(),
        "day_log": day_log,
        "flavor_text": flavor_text,
    }


class FixTaskRequest(BaseModel):
    task_id: str


@router.post("/fix-task")
async def fix_task(req: FixTaskRequest, game: tuple = Depends(get_game_from_token)):
    """Fix a maintenance task for rep and maintenance boost."""
    token, state = game

    task = next((t for t in state.maintenance_tasks if t.id == req.task_id), None)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Apply effects
    state.money -= task.money_cost
    state.rep += task.rep_reward
    state.building.maintenance = min(100, state.building.maintenance + task.maint_reward)

    # Remove the task
    state.maintenance_tasks = [t for t in state.maintenance_tasks if t.id != req.task_id]

    cost_str = f" (-${task.money_cost})" if task.money_cost > 0 else ""
    state.log.append(f"Day {state.day}: Fixed {task.label.lower()}.{cost_str} +{task.rep_reward} rep.")

    save_game(token, state)
    return state.model_dump()
