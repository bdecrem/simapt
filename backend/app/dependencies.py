"""FastAPI dependencies for game state access."""

from fastapi import Header, HTTPException
from .database import load_game, save_game
from .models.game import GameState


async def get_game_from_token(
    x_game_token: str = Header(..., description="Game session token"),
) -> tuple[str, GameState]:
    """Load game state from the database using the token header."""
    state = load_game(x_game_token)
    if state is None:
        raise HTTPException(status_code=404, detail="Game not found. Start a new one.")
    return (x_game_token, state)
