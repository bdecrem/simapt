<script>
  import { gameState } from '../../lib/stores/game.js';

  let tickerItems = $derived(buildTicker($gameState));

  function buildTicker(state) {
    const items = [];

    // Recent log entries
    for (const entry of state.log.slice(-5)) {
      items.push(entry);
    }

    // Tenant color
    for (const t of state.tenants.slice(0, 3)) {
      if (t.stats.happiness < 30) {
        items.push(`[Unit ${t.unit + 1}] ${t.name} hasn't been themselves lately.`);
      } else if (t.stats.suspicion > 40) {
        items.push(`[Unit ${t.unit + 1}] Something going on behind that door.`);
      }
    }

    if (items.length === 0) {
      items.push("The building breathes. In and out. Day after day.");
      items.push("A quiet night at The Bramble. Those don't last.");
    }

    return items;
  }
</script>

<div class="ticker">
  <div class="ticker-inner">
    {#each tickerItems as item, i}
      <span>{item}</span>
      {#if i < tickerItems.length - 1}
        <span class="tick-sep">&#9670;</span>
      {/if}
    {/each}
  </div>
</div>

<style>
  .ticker {
    position: absolute;
    bottom: 0; left: 0; right: 0;
    z-index: 40;
    background: rgba(8,9,16,0.92);
    border-top: 2px solid #2a2010;
    padding: 8px 0;
    overflow: hidden;
  }
  .ticker-inner {
    display: inline-block;
    white-space: nowrap;
    animation: ticker-scroll 40s linear infinite;
    font-family: 'VT323', monospace;
    font-size: 18px;
    color: var(--amber);
    padding-left: 100%;
  }
  .tick-sep {
    color: var(--muted);
    margin: 0 24px;
  }
</style>
