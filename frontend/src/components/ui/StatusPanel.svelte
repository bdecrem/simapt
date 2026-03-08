<script>
  import { gameState, occupancy, occupancyMax, buildingVibe, overdueTenants } from '../../lib/stores/game.js';

  let occPercent = $derived($occupancyMax > 0 ? ($occupancy / $occupancyMax) * 100 : 0);
  let vibeColor = $derived($buildingVibe > 60 ? 'green' : $buildingVibe > 30 ? 'amber' : 'red');
  let overdueCount = $derived($overdueTenants.length);
</script>

<div class="status-panel">
  <div class="stat-row">
    <span class="stat-label">OCCUPANCY</span>
    <div class="stat-bar">
      <div class="stat-fill green" style="width:{occPercent}%"></div>
    </div>
    <span class="stat-val">{$occupancy}/{$occupancyMax}</span>
  </div>
  <div class="stat-row">
    <span class="stat-label">VIBE</span>
    <div class="stat-bar">
      <div class="stat-fill {vibeColor}" style="width:{$buildingVibe}%"></div>
    </div>
    <span class="stat-val">{$buildingVibe}</span>
  </div>
  <div class="stat-row">
    <span class="stat-label">MONEY</span>
    <div class="stat-bar">
      <div class="stat-fill amber" style="width:{Math.min(100, ($gameState.money / 5000) * 100)}%"></div>
    </div>
    <span class="stat-val">${$gameState.money}</span>
  </div>
  <div class="stat-row">
    <span class="stat-label">REP</span>
    <div class="stat-bar">
      <div class="stat-fill green" style="width:{($gameState.rep / 1000) * 100}%"></div>
    </div>
    <span class="stat-val">{$gameState.rep}/1000</span>
  </div>
</div>

<style>
  .status-panel {
    position: absolute;
    left: 40px; bottom: 100px;
    z-index: 35;
    pointer-events: none;
  }
  .stat-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 8px;
    font-family: 'VT323', monospace;
    font-size: 18px;
  }
  .stat-label { color: var(--muted); width: 90px; }
  .stat-bar {
    width: 100px; height: 8px;
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.1);
    position: relative;
    overflow: hidden;
  }
  .stat-fill { height: 100%; transition: width 1s; }
  .stat-fill.green { background: var(--green); }
  .stat-fill.amber { background: var(--amber); }
  .stat-fill.red { background: var(--red-dim); }
  .stat-val { color: var(--cream); font-size: 16px; opacity: 0.7; }
</style>
