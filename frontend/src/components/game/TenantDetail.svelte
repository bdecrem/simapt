<script>
  import { gameState } from '../../lib/stores/game.js';

  let { unitIndex, onclose } = $props();

  let tenant = $derived($gameState.tenants.find(t => t.unit === unitIndex));
  let isUnlocked = $derived(unitIndex < $gameState.unlocked_units);

  const statLabels = {
    happiness: 'Happiness',
    finances: 'Finances',
    social: 'Social',
    health: 'Health',
    stability: 'Stability',
    suspicion: 'Suspicion',
  };

  function statColor(key, val) {
    if (key === 'suspicion') return val > 40 ? 'red' : val > 20 ? 'amber' : 'green';
    return val > 60 ? 'green' : val > 30 ? 'amber' : 'red';
  }
</script>

<div class="sidebar">
  <button class="close-btn" onclick={onclose}>✕</button>

  <h3 class="unit-title">Unit {unitIndex + 1}</h3>

  {#if !isUnlocked}
    <p class="empty">This unit is locked. Earn more reputation to unlock it.</p>
  {:else if !tenant}
    <p class="empty">Vacant. Waiting for the right tenant.</p>
  {:else}
    <div class="tenant-header">
      <span class="emoji">{tenant.emoji}</span>
      <div>
        <div class="tenant-name">{tenant.name}</div>
        <div class="tenant-job">{tenant.job}, age {tenant.age}</div>
      </div>
    </div>

    <div class="rent-info">
      Rent: ${tenant.rent}/mo · Here {tenant.days_stayed} days
      {#if tenant.leaving}
        <span class="leaving-tag">LEAVING</span>
      {/if}
    </div>

    <div class="stats">
      {#each Object.entries(tenant.stats) as [key, val]}
        <div class="stat-row">
          <span class="stat-label">{statLabels[key]}</span>
          <div class="stat-bar">
            <div class="stat-fill {statColor(key, val)}" style="width:{val}%"></div>
          </div>
          <span class="stat-val">{val}</span>
        </div>
      {/each}
    </div>

    {#if tenant.quirks.length > 0}
      <div class="section">
        <div class="section-header">QUIRKS</div>
        {#each tenant.quirks as quirk}
          <div class="quirk">{quirk}</div>
        {/each}
      </div>
    {/if}

    {#if tenant.revealed}
      <div class="section hidden-trait">
        <div class="section-header">DISCOVERED</div>
        <div class="hidden-text">{tenant.hidden_text}</div>
      </div>
    {/if}

    {#if tenant.memory.length > 0}
      <div class="section">
        <div class="section-header">MEMORY</div>
        {#each tenant.memory.slice(-5) as mem}
          <div class="memory-entry">{mem}</div>
        {/each}
      </div>
    {/if}
  {/if}
</div>

<style>
  .sidebar {
    position: fixed;
    top: 0; right: 0;
    width: 320px;
    height: 100vh;
    background: rgba(8, 9, 16, 0.97);
    border-left: 2px solid var(--panel-border);
    z-index: 90;
    padding: 24px;
    overflow-y: auto;
    animation: slide-in-right 0.3s ease-out;
  }

  @keyframes slide-in-right {
    from { transform: translateX(100%); }
    to { transform: translateX(0); }
  }

  .close-btn {
    position: absolute;
    top: 16px; right: 16px;
    background: none;
    border: none;
    color: var(--muted);
    font-size: 20px;
    cursor: pointer;
  }
  .close-btn:hover { color: var(--cream); }

  .unit-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 10px;
    color: var(--amber);
    letter-spacing: 2px;
    margin-bottom: 16px;
  }

  .empty {
    font-family: 'VT323', monospace;
    font-size: 18px;
    color: var(--muted);
    margin-top: 20px;
  }

  .tenant-header {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;
  }
  .emoji { font-size: 28px; }
  .tenant-name {
    font-family: 'VT323', monospace;
    font-size: 24px;
    color: var(--cream);
  }
  .tenant-job {
    font-family: 'VT323', monospace;
    font-size: 16px;
    color: var(--muted);
  }

  .rent-info {
    font-family: 'VT323', monospace;
    font-size: 16px;
    color: var(--muted);
    margin-bottom: 20px;
  }
  .leaving-tag {
    color: var(--red-dim);
    font-weight: bold;
    margin-left: 8px;
  }

  .stats { margin-bottom: 20px; }
  .stat-row {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    font-family: 'VT323', monospace;
    font-size: 16px;
  }
  .stat-label { color: var(--muted); width: 80px; }
  .stat-bar {
    flex: 1;
    height: 6px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
    overflow: hidden;
  }
  .stat-fill { height: 100%; transition: width 0.5s; }
  .stat-fill.green { background: var(--green); }
  .stat-fill.amber { background: var(--amber); }
  .stat-fill.red { background: var(--red-dim); }
  .stat-val { color: var(--cream); width: 24px; text-align: right; opacity: 0.7; }

  .section {
    margin-bottom: 16px;
  }
  .section-header {
    font-family: 'Press Start 2P', monospace;
    font-size: 6px;
    color: var(--amber);
    letter-spacing: 2px;
    margin-bottom: 8px;
    padding-bottom: 4px;
    border-bottom: 1px solid rgba(210,136,42,0.2);
  }
  .quirk, .memory-entry {
    font-family: 'VT323', monospace;
    font-size: 16px;
    color: var(--cream);
    opacity: 0.7;
    margin-bottom: 4px;
    padding-left: 8px;
    border-left: 2px solid var(--muted);
  }

  .hidden-trait {
    background: rgba(139, 42, 42, 0.1);
    padding: 8px;
    border: 1px solid rgba(139, 42, 42, 0.3);
  }
  .hidden-text {
    font-family: 'VT323', monospace;
    font-size: 16px;
    color: var(--cream);
    line-height: 1.5;
  }
</style>
