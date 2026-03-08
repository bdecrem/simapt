"""Tenant creation, stat decay, and departure logic."""

import random
from ..models.game import Tenant, TenantStats
from ..data.archetypes import ARCHETYPES


def make_tenant(unit: int, archetype_key: str | None = None) -> Tenant:
    """Create a new tenant from a random or specified archetype."""
    if archetype_key:
        arch = next(a for a in ARCHETYPES if a["key"] == archetype_key)
    else:
        arch = random.choice(ARCHETYPES)

    name = random.choice(arch["names"])
    age = random.randint(*arch["age_range"])
    job = random.choice(arch["jobs"])
    rent = random.randint(*arch["rent_range"])
    base = arch["base_stats"]

    # Add some variance to base stats
    stats = TenantStats(
        happiness=_vary(base["happiness"]),
        finances=_vary(base["finances"]),
        social=_vary(base["social"]),
        health=_vary(base["health"]),
        stability=_vary(base["stability"]),
        suspicion=_vary(base["suspicion"]),
    )

    return Tenant(
        unit=unit,
        name=name,
        age=age,
        job=job,
        emoji=arch["emoji"],
        desc=f"{name}, {age}, {job}",
        archetype=arch["key"],
        stats=stats,
        rent=rent,
        quirks=list(arch["quirks"]),
        hidden=arch["hidden"],
        hidden_text=arch["hidden_text"],
    )


def _vary(val: int, amount: int = 10) -> int:
    """Add random variance to a stat value, clamped 0-100."""
    return max(0, min(100, val + random.randint(-amount, amount)))


def tick_tenants(tenants: list[Tenant], day: int) -> list[str]:
    """Decay/grow tenant stats each day. Returns log entries."""
    log = []
    for t in tenants:
        if t is None:
            continue
        t.days_stayed += 1
        s = t.stats

        # Daily decay
        s.happiness = _clamp(s.happiness - random.randint(1, 3))
        s.finances = _clamp(s.finances - random.randint(0, 2))
        s.health = _clamp(s.health - random.randint(0, 1))
        s.stability = _clamp(s.stability + (1 if s.happiness > 50 else -2))

        # Social decay if isolated
        if s.social > 30:
            s.social = _clamp(s.social - 1)

        # Suspicion decays slowly toward 20
        if s.suspicion > 20:
            s.suspicion = _clamp(s.suspicion - 1)

        # Hidden trait reveal check
        if not t.revealed and t.days_stayed > 20 and random.random() < 0.05:
            t.revealed = True
            log.append(f"Day {day}: You discovered something about {t.name}...")

        # Leaving logic
        if not t.leaving and s.happiness < 15 and s.stability < 20:
            t.leaving = True
            t.leave_day = day + 7
            log.append(f"Day {day}: {t.name} is thinking about leaving...")

        if t.leaving and t.leave_day and day >= t.leave_day:
            log.append(f"Day {day}: {t.name} has moved out of unit {t.unit + 1}.")

    return log


def _clamp(val: int, lo: int = 0, hi: int = 100) -> int:
    return max(lo, min(hi, val))
