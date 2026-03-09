"""Database layer — stores game state as JSON in a single table."""

from datetime import datetime, timezone
from sqlalchemy import create_engine, Column, String, DateTime, Text
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import DATABASE_URL
from .models.game import GameState

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()


class GameRow(Base):
    __tablename__ = "games"

    token = Column(String(24), primary_key=True)
    state = Column(Text, nullable=False)  # JSON string (works with both Postgres and SQLite)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc),
                        onupdate=lambda: datetime.now(timezone.utc))


def create_tables():
    Base.metadata.create_all(bind=engine)


def save_game(token: str, state: GameState) -> None:
    session = SessionLocal()
    try:
        row = session.get(GameRow, token)
        json_str = state.model_dump_json()
        if row:
            row.state = json_str
            row.updated_at = datetime.now(timezone.utc)
        else:
            row = GameRow(token=token, state=json_str)
            session.add(row)
        session.commit()
    finally:
        session.close()


def load_game(token: str) -> GameState | None:
    session = SessionLocal()
    try:
        row = session.get(GameRow, token)
        if not row:
            return None
        return GameState.model_validate_json(row.state)
    finally:
        session.close()
