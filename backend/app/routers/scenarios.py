"""Scenario routes: make a choice."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from ..dependencies import get_game_from_token
from ..engine.scenarios import apply_choice
from ..ai.generate import generate_narration
from ..database import save_game

router = APIRouter()


class ChoiceRequest(BaseModel):
    choice_id: str


@router.post("/choose")
async def choose(req: ChoiceRequest, game: tuple = Depends(get_game_from_token)):
    """Apply a scenario choice and get AI narration."""
    token, state = game

    if not state.active_scenario:
        raise HTTPException(status_code=400, detail="No active scenario")

    # Generate AI narration before applying (need scenario context)
    scenario = state.active_scenario
    ai_narration = await generate_narration(state, scenario, req.choice_id)

    # Apply the choice effects
    result = apply_choice(state, req.choice_id)

    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    save_game(token, state)

    return {
        **state.model_dump(),
        "narration": ai_narration,
        "choice_result": result,
    }
