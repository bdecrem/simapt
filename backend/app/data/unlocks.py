"""Rep threshold unlock table."""

UNLOCKS = [
    {"rep": 0, "units": 3, "tier": 1, "label": "Starting Out"},
    {"rep": 100, "units": 4, "tier": 2, "label": "Getting Noticed"},
    {"rep": 200, "units": 5, "tier": 2, "label": "Established"},
    {"rep": 350, "units": 6, "tier": 3, "label": "Respected"},
    {"rep": 500, "units": 7, "tier": 3, "label": "Renowned"},
    {"rep": 700, "units": 8, "tier": 4, "label": "Legendary"},
    {"rep": 1000, "units": 8, "tier": 4, "label": "The Bramble"},
]


def get_unlock_level(rep: int) -> dict:
    """Return the unlock info for a given rep value."""
    result = UNLOCKS[0]
    for u in UNLOCKS:
        if rep >= u["rep"]:
            result = u
    return result
