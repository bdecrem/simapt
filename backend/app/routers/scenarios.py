"""Scenario routes: make a choice."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..routers.game import get_game
from ..engine.scenarios import apply_choice
from ..ai.generate import generate_narration

router = APIRouter()


class ChoiceRequest(BaseModel):
    choice_id: str


@router.post("/choose")
async def choose(req: ChoiceRequest):
    """Apply a scenario choice and get AI narration."""
    state = get_game()

    if not state.active_scenario:
        raise HTTPException(status_code=400, detail="No active scenario")

    # Generate AI narration before applying (need scenario context)
    scenario = state.active_scenario
    ai_narration = await generate_narration(state, scenario, req.choice_id)

    # Apply the choice effects
    result = apply_choice(state, req.choice_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    return {
        **state.model_dump(),
        "narration": ai_narration,
        "choice_result": result,
    }
