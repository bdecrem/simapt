import { writable, derived } from 'svelte/store';

export const gameState = writable({
  id: null,
  day: 0,
  money: 5000,
  rep: 0,
  tenants: [],
  building: { maintenance: 70, safety: 80, noise: 20, appeal: 60, happiness: 50 },
  units: [null, null, null, null, null, null, null, null],
  unlocked_units: 3,
  scenario_queue: [],
  active_scenario: null,
  used_scenarios: [],
  log: [],
  phase: 'menu', // 'menu' | 'playing' | 'won' | 'lost'
  next_scenario_day: 3,
});

export const occupancy = derived(gameState, $g =>
  $g.tenants.filter(t => t !== null).length
);

export const occupancyMax = derived(gameState, $g => $g.unlocked_units);

export const buildingVibe = derived(gameState, $g => $g.building.happiness);

export const overdueTenants = derived(gameState, $g =>
  $g.tenants.filter(t => t && t.stats.finances < 20)
);

export const recentLog = derived(gameState, $g =>
  $g.log.slice(-20).reverse()
);

// UI state
export const selectedUnit = writable(null);
export const showLog = writable(false);
export const showNarration = writable(null); // { text, choiceResult }
export const isLoading = writable(false);
