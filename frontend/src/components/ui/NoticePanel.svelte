<script>
  import { gameState } from '../../lib/stores/game.js';

  let notices = $derived(buildNotices($gameState));

  function buildNotices(state) {
    const items = [];

    // Overdue tenants
    for (const t of state.tenants) {
      if (t.stats.finances < 20) {
        items.push({ text: `Unit ${t.unit + 1} — rent overdue`, type: 'overdue' });
      }
    }

    // Unhappy tenants
    for (const t of state.tenants) {
      if (t.stats.happiness < 25 && !t.leaving) {
        items.push({ text: `Unit ${t.unit + 1} — unhappy`, type: 'event' });
      }
    }

    // Leaving tenants
    for (const t of state.tenants) {
      if (t.leaving) {
        items.push({ text: `Unit ${t.unit + 1} — moving out`, type: 'overdue' });
      }
    }

    // Building issues
    if (state.building.maintenance < 40) {
      items.push({ text: 'Maintenance critical', type: 'overdue' });
    }
    if (state.building.safety < 50) {
      items.push({ text: 'Safety concerns', type: 'event' });
    }

    // Active scenario
    if (state.active_scenario) {
      items.push({ text: state.active_scenario.definition.title, type: 'event' });
    }

    if (items.length === 0) {
      items.push({ text: 'All quiet.', type: 'neutral' });
    }

    return items.slice(0, 5);
  }
</script>

<div class="notice-panel">
  <div class="notice-header">▌PENDING MATTERS</div>
  {#each notices as notice}
    <div class="notice-item {notice.type}">{notice.text}</div>
  {/each}
</div>

<style>
  .notice-panel {
    position: absolute;
    right: 40px; bottom: 100px;
    z-index: 35;
    width: 200px;
    background: var(--panel-bg);
    border: 1px solid var(--panel-border);
    padding: 14px;
    pointer-events: none;
  }
  .notice-header {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: var(--amber);
    letter-spacing: 1px;
    margin-bottom: 10px;
    border-bottom: 1px solid rgba(210,136,42,0.3);
    padding-bottom: 6px;
  }
  .notice-item {
    font-family: 'VT323', monospace;
    font-size: 16px;
    color: var(--cream);
    opacity: 0.75;
    margin-bottom: 8px;
    line-height: 1.3;
    padding-left: 8px;
    border-left: 2px solid;
  }
  .notice-item.overdue { border-color: var(--red-dim); }
  .notice-item.event { border-color: var(--amber); }
  .notice-item.neutral { border-color: var(--muted); }
</style>
