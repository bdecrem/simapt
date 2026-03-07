# THE BRAMBLE — Qwen Briefing
# Paste this entire file at the start of your session.

## What you are doing
You are helping finish and extend a single-file HTML/JS landlord simulation game called The Bramble.
The game file is bramble.html. Everything — HTML, CSS, game engine, content — is in that one file.
Your job is to make targeted edits. Do not rewrite the whole file. Find the relevant section and change only what needs changing.

---

## The game in one paragraph
You are a landlord managing a small apartment building. Tenants have stats (happiness, finances, health, etc.) that decay and interact. Every few days a scenario card appears — a situation involving a tenant. You pick from 2-3 choices. Consequences unfold, stats change, rep goes up or down. Rep unlocks new units, new tenants arrive, harder scenarios trigger. Reach 1000 rep to win. Run out of money or lose all tenants to lose.

---

## File structure (so you can find things fast)

```
<style>          — all CSS, ~200 lines
<body>           — HTML layout: header, building grid, sidebar, log, overlays
<script>
  ARCHETYPES     — array of 12 tenant objects (name, stats, hidden trait, rent, quirks)
  SCENARIOS      — array of 25 scenario objects (title, tier, condition, choices with effects)
  PROMPTS        — prompt templates for flavor text generation
  FLAVOR         — fallback flavor sentences (used when model is offline)
  G              — game state object (day, money, rep, tenants, building stats, etc.)
  init()         — starts the game, creates first 3 tenants
  advanceDay()   — main game loop tick
  tickTenants()  — decays/grows tenant stats each day
  tickBuilding() — decays building stats each day
  collectRent()  — runs every 30 days
  tryQueueScenario() — picks and queues a scenario based on conditions
  fireNextScenario() — displays scenario card overlay
  makeChoice()   — applies effects of player's decision
  render()       — redraws everything
  callModel()    — AI bridge function (THIS IS YOUR FIRST TASK)
```

---

## TASK 1 — Wire the AI (do this first, 20 minutes)

Find `callModel()` in the script. It currently returns a random fallback string.
Replace the body with a real Qwen call.

### If using Ollama:
```javascript
async function callModel(prompt) {
  const res = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'qwen2.5:8b',
      prompt: prompt,
      stream: false,
      options: { temperature: 0.8, num_predict: 80 }
    })
  });
  const d = await res.json();
  return d.response.trim();
}
```

### If using LM Studio:
```javascript
async function callModel(prompt) {
  const res = await fetch('http://localhost:1234/v1/completions', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'qwen2.5-8b',
      prompt: prompt,
      max_tokens: 80,
      temperature: 0.8
    })
  });
  const d = await res.json();
  return d.choices[0].text.trim();
}
```

The model is called twice per scenario: once for atmospheric flavor text, once for consequence narration.
The prompts are in the PROMPTS object. They are already well-engineered — don't change them unless the output is bad.

---

## TASK 2 — Play and fix (2 hours)

Open bramble.html in a browser. Click Next Day repeatedly until a scenario fires (usually within 3 clicks).
Common things to fix:
- Scenario condition logic: if scenarios never fire, check `checkCond()` — conditions may be too strict
- Stat balance: if tenants leave too fast, reduce the decay rates in `tickTenants()`
- Money balance: starting money is $5,000. Rent collects every 30 days. If player goes broke too fast, increase starting money or reduce costs
- Scenario variety: if you see the same scenario twice, `G.usedScenarios` tracks this — it clears after 80% coverage

To add a new scenario, add an object to the SCENARIOS array following this exact shape:
```javascript
{ id:'unique_id', tier:1, title:'Display Title', w:5,  // w = weight (higher = more frequent)
  cond:{ always:true },  // or statBelow, statAbove, bStatBelow, repAbove, repBelow, unitEmpty, daysStayed
  desc: t => `Description involving ${t.name}. Can reference t.job, t.rent, etc.`,
  choices:[
    { id:'choice_id', label:'Button label', desc:'Sub-description.',
      rep:+10, money:-500,
      fx:{ tHappiness:+20, tStability:+15, bMaintenance:+5 },  // see FX KEYS below
      nar:`Consequence narrative. Use {name} for tenant name.` }
  ]
}
```

FX keys (all optional):
- tHappiness, tFinances, tSocial, tHealth, tStability, tSuspicion — tenant stat changes
- bHappiness, bMaintenance, bSafety, bNoise, bAppeal — building stat changes

---

## TASK 3 (bonus) — Tenant relationship web in sidebar

When a tenant is selected, the sidebar currently shows their stats, hidden trait (if revealed), quirks, and memory.
Add a relationship section that shows their relationship score with every other current tenant (-100 to +100).

To implement:
1. Add a `relationships: {}` object to each tenant in `makeTenant()` — keyed by tenant id, defaulting to 0
2. Seed starting relationships randomly: artist and parent slightly positive, loner neutral-negative with everyone
3. Update relationships when scenarios involve multiple tenants (breakup scenario should tank both relationships)
4. Render in sidebar as colored bars: green = positive, red = negative
5. Use relationship scores to modify scenario conditions or choice availability over time

---

## Key variables to know

```javascript
G.day          // current day number
G.money        // current cash balance
G.rep          // current reputation (0-1000)
G.tenants      // array of tenant objects
G.bld          // building stats object: { maintenance, safety, noise, appeal, happiness }
G.selected     // unit index of selected unit (or null)
G.scenarioQ    // queue of pending scenarios
G.activeScenario // currently displayed scenario (null if none)
```

Tenant object shape:
```javascript
{
  id, unit, name, age, job, emoji, desc,
  stats: { happiness, finances, social, health, stability, suspicion },
  rent, quirks, hidden, hiddenText, revealed,
  memory,        // array of strings: "Day 12: Grace period given"
  daysStayed,    // days in building
  leaving,       // boolean
  leaveDay       // day they'll leave if nothing changes
}
```

---

## What NOT to change
- The CSS (it's done, it looks good)
- The ARCHETYPES array (all 12 are fully written and balanced)
- The UNLOCK thresholds in the UNLOCKS array
- The render() pipeline (renderHeader, renderBuilding, renderSidebar, renderLog)

## What you CAN freely change
- callModel() — wire it to Qwen
- SCENARIOS — add, edit, rebalance
- tickTenants() decay rates — tune for feel
- G.money starting value — tune for difficulty
- FLAVOR fallback sentences — add more
- Any bug you find
