"""FastAPI application for The Bramble."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import game, scenarios

app = FastAPI(title="The Bramble", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(game.router, prefix="/game", tags=["game"])
app.include_router(scenarios.router, prefix="/scenario", tags=["scenarios"])


@app.get("/")
def root():
    return {"name": "The Bramble", "version": "0.1.0"}
