# THE BRAMBLE — Project Plan

## Project Summary
A single-file HTML/JavaScript landlord simulation game where you manage an apartment building with 8 units and tenant archetypes. Players respond to scenario cards (tenant situations) with choices that affect tenant stats (happiness, finances, health, social, stability, suspicion), your reputation, and building progression. Win by reaching 1000 rep; lose by running out of money or losing all tenants.

---

## Phase 1: Core Structure & Game State
**Goal:** Establish the HTML skeleton, CSS styling, game state object, tenant system, and basic rendering pipeline.

### Tasks
1. **HTML Skeleton** - Basic structure with containers for building view, sidebar, scenario card, and log
2. **CSS Styling** - Retro CRT aesthetic with brick textures, animated windows showing tenant status
3. **Game State Object (G)** - Initialize: money ($5000), rep (0), units array (8 empty slots), day counter
4. **Tenant System** - Create tenant data structure with stats (happiness, finances, health, social, stability, suspicion), quirks, hidden traits, memory log
5. **Archetypes** - Define 12 tenant archetypes with stat profiles and personality traits
6. **Render Pipeline** - Implement `renderBuilding()`, `renderSidebar()`, `renderLog()` functions
7. **Tick System** - Create `tickTenants()` for daily stat decay calculations

### Success Criteria (Phase 1 Complete)
- [ ] HTML file loads without errors
- [ ] CSS renders the building with visible windows showing tenant status
- [ ] Game state initializes correctly ($5000 money, 8 empty units, rep=0)
- [ ] Tenant archetypes defined and accessible
- [ ] `tickTenants()` runs every day and decays stats
- [ ] Scenario card displays after a few days (auto-triggered)

### Dependencies for Phase 2
- Game state object fully implemented with all required properties
- Rendering pipeline working (building view, sidebar, log)
- Tenant system functional with stat decay
- Basic scenario trigger mechanism in place

---

## Phase 2: Scenario System & Interaction
**Goal:** Build the core gameplay loop - scenario cards appear, player makes choices, consequences unfold.

### Tasks
1. **Scenario Array (SCENARIOS)** - Structure with id, tier, title, weight, condition logic, description template, choices array
2. **Condition Logic** - Implement `checkCond()` for various conditions (stat thresholds, rep thresholds, unit empty, days stayed)
3. **Scenario Trigger** - Auto-fire scenario after 3-4 clicks or set interval
4. **Choice System** - Display 2-3 choices with consequences attached
5. **Consequence Engine** - Apply stat changes, rep changes, unlock new units when thresholds met
6. **Tenant Arrival** - Spawn new tenants when units unlocked (rep-based)
7. **Harder Scenarios** - Increase difficulty as rep increases

### Success Criteria (Phase 2 Complete)
- [ ] Scenario cards appear automatically after a few days
- [ ] Player can make choices from scenario card
- [ ] Choices affect tenant stats and reputation
- [ ] Consequences trigger stat changes and rep adjustments
- [ ] New tenants spawn when rep thresholds unlocked
- [ ] Scenario variety increases with higher rep

### Dependencies for Phase 3
- Rendering pipeline working (scenario card display)
- Consequence engine functional (stat/rep changes)
- Tenant arrival system operational
- Condition logic implemented

---

## Phase 3: AI Content Generation & Polish
**Goal:** Wire up Qwen model for scenario generation, add flavor text, balance mechanics.

### Tasks
1. **callModel() Integration** - Connect to Qwen API for content generation
2. **Scenario Templates** - Create prompt templates for tenant situations
3. **Flavor Text** - Add descriptive sentences and narrative elements
4. **Balance Tuning** - Adjust decay rates, starting money, unlock thresholds
5. **Bug Fixes** - Fix scenario condition logic, stat balance issues

### Success Criteria (Phase 3 Complete)
- [ ] `callModel()` successfully generates scenarios
- [ ] Flavor text adds immersion and variety
- [ ] Decay rates feel balanced (tenants don't leave too fast)
- [ ] Starting money allows reasonable gameplay ($5000, rent every 30 days)
- [ ] Scenario conditions trigger reliably

### Dependencies for Phase 4
- AI content generation working
- Balance tuning complete
- Bug fixes resolved

---

## Phase 4: Win/Loss States & Polish
**Goal:** Implement victory/defeat conditions and final polish.

### Tasks
1. **Win Condition** - Reach 1000 rep to win game
2. **Loss Conditions** - Run out of money or lose all tenants
3. **End Game Screen** - Display victory/defeat message with stats summary
4. **Final Polish** - Add any remaining visual/audio polish

### Success Criteria (Phase 4 Complete)
- [ ] Win screen displays at 1000 rep
- [ ] Loss conditions trigger correctly
- [ ] End game shows final stats and summary
- [ ] Game is fully playable end-to-end

---

## Technical Notes

### File Structure
- Single file: `bramble.html` (all HTML, CSS, JS in one file)
- No external dependencies except Google Fonts

### Key Data Structures
```javascript
// Game state
G = {
  money: 5000,
  rep: 0,
  day: 1,
  units: [], // 8 slots, each with tenant or empty
  usedScenarios: [] // track for variety
}

// Tenant object
{
  id: 'unique_id',
  name: 'Tenant Name',
  happiness: 50,
  finances: 50,
  health: 50,
  social: 50,
  stability: 50,
  suspicion: 50,
  rent: 100,
  quirks: [],
  hidden: {},
  memory: [], // event log
  daysStayed: 0,
  leaving: false,
  leaveDay: null
}

// Scenario object
{
  id: 'unique_id',
  tier: 1,
  title: 'Display Title',
  weight: 5, // frequency
  cond: { always: true }, // or statBelow, statAbove, etc.
  desc: t => `Description involving ${t.name}`,
  choices: [
    { text: 'Choice A', effect: { happiness: -10, rep: 5 } },
    { text: 'Choice B', effect: { happiness: 10, rep: -5 } }
  ]
}
```

### Key Functions to Implement
- `tickTenants()` - daily stat decay
- `checkCond()` - scenario condition evaluation
- `renderBuilding()` - display building with windows
- `renderSidebar()` - show stats and controls
- `renderLog()` - event history
- `callModel()` - AI content generation
- `triggerScenario()` - fire next scenario

### Common Debugging Points
- Scenario conditions not firing → check `checkCond()` logic
- Tenants leaving too fast → reduce decay rates in `tickTenants()`
- Going broke too quickly → increase starting money or reduce costs
- Same scenarios repeating → verify `G.usedScenarios` tracking works

---

## Next Steps After Phase 1
Once Phase 1 is complete, we'll:
1. Verify the game state initializes correctly
2. Test the rendering pipeline (building view, windows showing tenant status)
3. Implement auto-triggered scenario cards after a few days
4. Add choice system and consequence application

**Ready to start Phase 1?** I'll begin by creating the HTML skeleton, CSS styling, and core game state structure.
