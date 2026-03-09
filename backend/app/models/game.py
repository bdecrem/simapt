from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal
import uuid


class TenantStats(BaseModel):
    happiness: int = 50
    finances: int = 50
    social: int = 50
    health: int = 50
    stability: int = 50
    suspicion: int = 20


class Tenant(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    unit: int
    name: str
    age: int
    job: str
    emoji: str
    desc: str
    archetype: str
    stats: TenantStats = Field(default_factory=TenantStats)
    rent: int = 800
    quirks: list[str] = Field(default_factory=list)
    hidden: str = ""
    hidden_text: str = ""
    revealed: bool = False
    memory: list[str] = Field(default_factory=list)
    days_stayed: int = 0
    leaving: bool = False
    leave_day: int | None = None


class BuildingStats(BaseModel):
    maintenance: int = 70
    safety: int = 80
    noise: int = 20
    appeal: int = 60
    happiness: int = 50


class ChoiceEffect(BaseModel):
    t_happiness: int = 0
    t_finances: int = 0
    t_social: int = 0
    t_health: int = 0
    t_stability: int = 0
    t_suspicion: int = 0
    b_maintenance: int = 0
    b_safety: int = 0
    b_noise: int = 0
    b_appeal: int = 0
    b_happiness: int = 0


class ScenarioChoice(BaseModel):
    id: str
    label: str
    desc: str
    rep: int = 0
    money: int = 0
    fx: ChoiceEffect = Field(default_factory=ChoiceEffect)
    narration: str = ""


class ScenarioCondition(BaseModel):
    always: bool = False
    stat_below: dict[str, int] | None = None
    stat_above: dict[str, int] | None = None
    b_stat_below: dict[str, int] | None = None
    rep_above: int | None = None
    rep_below: int | None = None
    days_stayed_above: int | None = None


class ScenarioDefinition(BaseModel):
    id: str
    tier: int
    title: str
    weight: int = 5
    cond: ScenarioCondition = Field(default_factory=ScenarioCondition)
    desc_template: str = ""
    choices: list[ScenarioChoice] = Field(default_factory=list)


class ActiveScenario(BaseModel):
    definition: ScenarioDefinition
    tenant_id: str
    tenant_name: str
    description: str = ""
    flavor_text: str = ""


class GameState(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    day: int = 1
    money: int = 5000
    rep: int = 0
    tenants: list[Tenant] = Field(default_factory=list)
    building: BuildingStats = Field(default_factory=BuildingStats)
    units: list[str | None] = Field(default_factory=lambda: [None] * 8)
    unlocked_units: int = 3
    scenario_queue: list[str] = Field(default_factory=list)
    active_scenario: ActiveScenario | None = None
    used_scenarios: list[str] = Field(default_factory=list)
    log: list[str] = Field(default_factory=list)
    phase: Literal["playing", "won", "lost"] = "playing"
    next_scenario_day: int = 3
