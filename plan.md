# THE BRAMBLE — Implementation Plan

## Architecture Overview

```
simapt/
├── frontend/                    # Svelte + Vite
│   ├── src/
│   │   ├── App.svelte
│   │   ├── main.js
│   │   ├── lib/
│   │   │   ├── stores/          # Svelte stores for state
│   │   │   │   ├── game.js      # Core game state (money, rep, day, tenants, building)
│   │   │   │   ├── scenario.js  # Active scenario, queue, used list
│   │   │   │   └── ui.js        # Selected unit, overlays, panels
│   │   │   ├── engine/          # Game logic (pure functions, no UI)
│   │   │   │   ├── tick.js      # advanceDay, tickTenants, tickBuilding
│   │   │   │   ├── scenarios.js # tryQueueScenario, checkCond, makeChoice
│   │   │   │   ├── tenants.js   # makeTenant, collectRent, tenant departure
│   │   │   │   ├── economy.js   # Money calculations, rent, costs
│   │   │   │   └── progression.js # Rep thresholds, unlocks, win/lose checks
│   │   │   ├── data/            # Static game data
│   │   │   │   ├── archetypes.js  # 12 tenant archetypes
│   │   │   │   ├── scenarios.js   # 25 scenario definitions (4 tiers)
│   │   │   │   └── unlocks.js     # Rep threshold unlock table
│   │   │   └── api.js           # HTTP client for backend calls
│   │   ├── components/
│   │   │   ├── scene/           # The building visual
│   │   │   │   ├── Scene.svelte       # Sky, rain, stars, street — the full scene
│   │   │   │   ├── Building.svelte    # Building body with floors
│   │   │   │   ├── Window.svelte      # Individual window (lit state, silhouettes)
│   │   │   │   ├── Rooftop.svelte     # Water tower, antenna, HVAC
│   │   │   │   ├── Street.svelte      # Street, lamps, puddles
│   │   │   │   └── Rain.svelte        # Canvas rain animation
│   │   │   ├── ui/              # Game interface panels
│   │   │   │   ├── Header.svelte      # Game title, building name
│   │   │   │   ├── StatusPanel.svelte # Left sidebar: occupancy, vibe, rent
│   │   │   │   ├── NoticePanel.svelte # Right sidebar: pending matters
│   │   │   │   ├── Ticker.svelte      # Bottom news ticker
│   │   │   │   ├── DayCounter.svelte  # Day/month display
│   │   │   │   └── Sidebar.svelte     # Tenant detail panel (stats, traits, memory)
│   │   │   ├── game/            # Gameplay overlays
│   │   │   │   ├── ScenarioCard.svelte  # Scenario popup with choices
│   │   │   │   ├── ChoiceButton.svelte  # Individual choice in scenario
│   │   │   │   ├── ConsequenceOverlay.svelte # AI-narrated consequence
│   │   │   │   ├── ApplicantCard.svelte # New tenant application
│   │   │   │   └── EndScreen.svelte     # Win/lose screen
│   │   │   └── shared/
│   │   │       ├── StatBar.svelte     # Reusable stat bar (green/amber/red)
│   │   │       └── Overlay.svelte     # Modal overlay wrapper
│   │   └── styles/
│   │       ├── global.css       # CSS variables, fonts, reset
│   │       ├── crt.css          # Scanlines, vignette, glow effects
│   │       └── building.css     # Building-specific styles
│   ├── index.html
│   ├── vite.config.js
│   └── package.json
│
├── backend/                     # Python FastAPI
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app, CORS, lifespan
│   │   ├── config.py            # Settings (API keys, model config)
│   │   ├── routers/
│   │   │   ├── game.py          # POST /game/new, GET /game/{id}, POST /game/{id}/advance
│   │   │   ├── scenarios.py     # POST /game/{id}/choice — apply choice, get AI narration
│   │   │   └── ai.py            # POST /ai/flavor, POST /ai/narrate — direct AI endpoints
│   │   ├── models/
│   │   │   ├── game_state.py    # Pydantic models: GameState, Tenant, Building, Scenario
│   │   │   └── requests.py      # Request/response schemas
│   │   ├── services/
│   │   │   ├── ai_service.py    # Anthropic Haiku client — flavor text & narration
│   │   │   ├── game_service.py  # Game logic orchestration
│   │   │   └── prompt_templates.py # Prompt engineering for Haiku calls
│   │   └── storage/
│   │       └── memory.py        # In-memory game state store (swap for DB later)
│   ├── requirements.txt
│   └── pyproject.toml
│
├── design.html                  # Original aesthetic reference (keep for reference)
├── intro.txt                    # Original design notes
├── project-overview.md          # Original Opus briefing doc
├── project-plan.md              # Original project plan
└── plan.md                      # THIS FILE
```

---

## Tech Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Frontend | Svelte + Vite | Reactive, lightweight, great for game UIs with lots of state transitions |
| Backend | Python + FastAPI | Clean async API, easy Anthropic SDK integration, good for future DB |
| AI | Claude Haiku (anthropic) | Real-time flavor text and consequence narration — core feature |
| State mgmt | Svelte stores | Game state in writable stores, synced to backend on key actions |
| Persistence | In-memory (backend) + localStorage (frontend fallback) | Swap for SQLite/Postgres later |
| Art style | Indie retro, warm — refine design.html | Keep the vibe, brighten it up, less grimdark |

---

## AI Integration Design

Haiku is called in two moments per scenario:

1. **Flavor text** — When a scenario card appears, Haiku generates 1-2 atmospheric sentences setting the scene
2. **Consequence narration** — After the player makes a choice, Haiku narrates what happens next

### Prompt Strategy
```
System: You are the narrator of a landlord simulation game called The Bramble.
You write short, atmospheric, slightly wry prose. 1-2 sentences max.
Never break character. Never use game terminology.

User: [Context about tenant, their stats, the scenario, the building state]
Generate flavor text for this scenario: {scenario.title}
Tenant: {tenant.name}, {tenant.job}, happiness {tenant.stats.happiness}/100
```

### Fallback
If Haiku is unavailable (no API key, rate limit, error), fall back to pre-written flavor text from `data/scenarios.js`. The game must always be playable without AI.

---

## State Management

```javascript
// stores/game.js
export const gameState = writable({
  id: null,           // game session ID from backend
  day: 1,
  money: 5000,
  rep: 0,
  tenants: [],        // array of tenant objects
  building: {         // building stats
    maintenance: 70,
    safety: 80,
    noise: 30,
    appeal: 50,
    happiness: 60
  },
  units: Array(8).fill(null),  // unit index → tenant id or null
  log: []             // event log entries
});

export const scenarioState = writable({
  queue: [],
  active: null,       // currently displayed scenario
  usedIds: [],        // prevent repeats
  consequence: null   // AI-generated consequence text
});
```

Game state lives in Svelte stores on the frontend. On key actions (advance day, make choice), the frontend sends the action to the backend, which:
1. Computes the new state
2. Calls Haiku if needed
3. Returns the updated state + AI text

---

## Build Order (Implementation Steps)

### Step 1: Project Scaffolding
- Initialize Svelte + Vite project in `frontend/`
- Initialize FastAPI project in `backend/`
- Set up dev scripts (concurrent frontend + backend)
- Port CSS variables and fonts from design.html

### Step 2: Static Scene (Visual Foundation)
- Port the building visual from design.html into Svelte components
- Scene.svelte, Building.svelte, Window.svelte, Rooftop.svelte, Street.svelte
- Rain canvas animation in Rain.svelte
- Stars, scanlines, vignette
- Refine the aesthetic: warmer, more indie, less grimdark
- **Goal: the building renders and looks alive**

### Step 3: Game State & Data Layer
- Define all data types: archetypes, scenarios, unlocks
- Implement Svelte stores for game state
- Build the 12 tenant archetypes in `data/archetypes.js`
- Build the 25 scenarios across 4 tiers in `data/scenarios.js`
- Define unlock thresholds in `data/unlocks.js`

### Step 4: Core Game Engine (Frontend)
- `engine/tenants.js` — makeTenant(), tenant stat decay, departure logic
- `engine/tick.js` — advanceDay(), tickTenants(), tickBuilding()
- `engine/scenarios.js` — tryQueueScenario(), checkCond(), makeChoice()
- `engine/economy.js` — collectRent(), cost calculations
- `engine/progression.js` — rep unlocks, win/lose checks
- Wire engine to stores: clicking "Next Day" advances the game

### Step 5: UI Panels
- StatusPanel (occupancy, vibe, money, rep)
- NoticePanel (pending matters derived from game state)
- DayCounter
- Ticker (dynamically generated from tenant states)
- Sidebar (tenant detail when window clicked)
- **Goal: game state is visible and updating**

### Step 6: Scenario System (Frontend)
- ScenarioCard overlay with choices
- ChoiceButton with effect preview
- ConsequenceOverlay for narration
- Wire scenario flow: trigger → display → choose → consequence → close
- **Goal: full gameplay loop works with static text**

### Step 7: Backend API
- FastAPI app with CORS for local dev
- Game routes: new game, advance day, make choice
- Pydantic models mirroring frontend state
- In-memory game store
- **Goal: frontend talks to backend for state management**

### Step 8: AI Integration
- Anthropic SDK setup in `services/ai_service.py`
- Prompt templates for flavor text and consequence narration
- Wire into scenario flow: card shows AI flavor, choice shows AI narration
- Fallback to static text when AI unavailable
- **Goal: Haiku breathes life into every scenario**

### Step 9: Progression & Endgame
- Rep-based unit unlocks (100 → unit 4, 250 → unit 5, 500 → weird tier, 1000 → win)
- Tenant arrival system (applicant cards when units unlock)
- Win screen at 1000 rep
- Lose conditions: $0 money or 0 tenants
- EndScreen component
- **Goal: game is completable**

### Step 10: Balance & Polish
- Tune stat decay rates
- Tune money economy (rent vs costs)
- Tune scenario conditions and weights
- Add more scenario variety if needed
- Window states reflect tenant mood dynamically
- Ticker text generated from current game state
- Final visual polish

---

## Key Architecture Principles

1. **Engine is pure logic** — `lib/engine/` has zero UI imports. It takes state in, returns state out. This makes it testable and portable.

2. **Data is separate from logic** — `lib/data/` contains all archetypes, scenarios, and unlocks as plain objects. Easy to add content without touching code.

3. **AI is an enhancement, not a dependency** — Every AI call has a static fallback. The game is fully playable offline.

4. **Backend is optional for now** — The frontend engine can run standalone with localStorage. Backend adds persistence and AI proxying.

5. **Components mirror the visual hierarchy** — Scene contains Building contains Windows. UI panels are siblings. Overlays float above everything.
