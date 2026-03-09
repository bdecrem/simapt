<script>
  import { gameState } from '../../lib/stores/game.js';
  import Window from './Window.svelte';

  let { onselectunit } = $props();

  // 8 units arranged as 3 floors of building + entrance
  // Floor 3 (top): units 6, 7
  // Floor 2: units 4, 5
  // Floor 1: units 2, 3
  // Ground: units 0, 1
  const floors = [
    [6, 7],
    [4, 5],
    [2, 3],
    [0, 1],
  ];

  function getTenantForUnit(unitIndex) {
    return $gameState.tenants.find(t => t.unit === unitIndex) || null;
  }

  function isUnlocked(unitIndex) {
    return unitIndex < $gameState.unlocked_units;
  }
</script>

<div class="building-wrap">
  <!-- Rooftop -->
  <div class="rooftop">
    <div class="water-tower">
      <div class="wt-top"></div>
      <div class="wt-body"></div>
      <div class="wt-legs">
        <div class="wt-leg"></div>
        <div class="wt-leg"></div>
        <div class="wt-leg"></div>
      </div>
    </div>
    <div class="hvac"></div>
    <div class="antenna"></div>
  </div>

  <!-- Building body -->
  <div class="building">
    {#each floors as floor}
      <div class="floor">
        {#each floor as unitIndex}
          <Window
            {unitIndex}
            tenant={getTenantForUnit(unitIndex)}
            unlocked={isUnlocked(unitIndex)}
            onclick={() => onselectunit?.(unitIndex)}
          />
        {/each}
      </div>
    {/each}
  </div>

  <!-- Entrance -->
  <div class="entrance">
    <div class="door-container">
      <div class="door-arch">
        <div class="door-light"></div>
      </div>
      <div class="door-steps"></div>
    </div>
  </div>

  <!-- Street -->
  <div class="street">
    <div class="lamp-post" style="left:60px;">
      <div class="lamp-head"></div>
      <div class="lamp-pole"></div>
      <div class="lamp-glow"></div>
    </div>
    <div class="lamp-post" style="right:60px;">
      <div class="lamp-head"></div>
      <div class="lamp-pole"></div>
      <div class="lamp-glow"></div>
    </div>
    <div class="puddle" style="left:100px;"></div>
    <div class="puddle" style="left:300px; animation-delay:1.2s;"></div>
    <div class="puddle" style="right:120px; animation-delay:0.6s;"></div>
  </div>
</div>

<style>
  .building-wrap {
    position: relative;
    z-index: 10;
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-bottom: 0;
  }

  .rooftop {
    width: 420px;
    height: 28px;
    background: var(--brick-dark);
    position: relative;
    border-top: 3px solid #2a1f14;
    display: flex;
    align-items: flex-start;
    justify-content: center;
  }
  .rooftop::before {
    content: '';
    position: absolute;
    top: -14px;
    left: 40px;
    right: 40px;
    height: 14px;
    background: var(--brick-dark);
    border-top: 3px solid #2a1f14;
  }

  .water-tower {
    position: absolute;
    right: 60px;
    top: -68px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .wt-top { width: 36px; height: 12px; background: #1e1510; clip-path: polygon(0% 100%, 50% 0%, 100% 100%); }
  .wt-body { width: 40px; height: 36px; background: #241a10; border-left: 2px solid #1a1008; border-right: 2px solid #1a1008; }
  .wt-legs { width: 44px; height: 20px; display: flex; justify-content: space-between; padding: 0 2px; }
  .wt-leg { width: 3px; height: 100%; background: #1a1008; }

  .hvac { position: absolute; left: 50px; top: -20px; width: 28px; height: 16px; background: #1c1812; border: 2px solid #141210; }
  .antenna { position: absolute; left: 110px; top: -30px; width: 2px; height: 30px; background: #1a1810; }
  .antenna::after { content: ''; position: absolute; top: 0; left: -6px; width: 14px; height: 2px; background: #1a1810; }

  .building {
    width: 420px;
    background: var(--brick);
    position: relative;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    border-left: 4px solid var(--brick-dark);
    border-right: 4px solid var(--brick-dark);
  }
  .building::before {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
      repeating-linear-gradient(0deg, transparent, transparent 11px, rgba(0,0,0,0.25) 11px, rgba(0,0,0,0.25) 13px),
      repeating-linear-gradient(90deg, transparent, transparent 28px, rgba(0,0,0,0.15) 28px, rgba(0,0,0,0.15) 30px);
    pointer-events: none;
    z-index: 1;
  }

  .floor {
    display: flex;
    justify-content: center;
    gap: 18px;
    padding: 14px 24px;
    position: relative;
    z-index: 2;
  }
  .floor:not(:last-child) {
    border-bottom: 2px solid rgba(0,0,0,0.3);
  }

  .entrance {
    width: 420px;
    height: 48px;
    background: var(--brick-dark);
    display: flex;
    align-items: flex-end;
    justify-content: center;
    position: relative;
    border-left: 4px solid #1a0f08;
    border-right: 4px solid #1a0f08;
    z-index: 10;
  }
  .door-container { position: relative; }
  .door-arch {
    width: 56px;
    height: 46px;
    background: #080a12;
    border-radius: 28px 28px 0 0;
    border: 3px solid #100c08;
    border-bottom: none;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
  }
  .door-light {
    position: absolute;
    top: -8px;
    width: 20px;
    height: 20px;
    background: radial-gradient(circle, rgba(255,180,60,0.8) 0%, transparent 70%);
    animation: lamp-pulse 4s ease-in-out infinite;
  }
  .door-steps {
    width: 80px;
    height: 10px;
    background: #1a1710;
    border-top: 2px solid #2a2218;
    position: absolute;
    bottom: -10px;
    left: -12px;
  }

  .street {
    width: 100%;
    height: 80px;
    background: var(--street);
    position: relative;
    border-top: 3px solid #0e1018;
  }
  .street::after {
    content: '';
    position: absolute;
    top: 30px;
    left: 0; right: 0;
    height: 2px;
    background: repeating-linear-gradient(90deg, transparent 0, transparent 30px, rgba(255,220,100,0.15) 30px, rgba(255,220,100,0.15) 60px);
  }

  .lamp-post { position: absolute; bottom: 0; }
  .lamp-pole { width: 3px; height: 60px; background: #1a1810; }
  .lamp-head {
    width: 20px; height: 8px; background: #1e1c14;
    border-radius: 3px 3px 0 0; margin-left: -9px;
  }
  .lamp-head::after {
    content: '';
    position: absolute; bottom: 56px; left: 50%; transform: translateX(-50%);
    width: 10px; height: 10px;
    background: radial-gradient(circle, rgba(255,200,80,0.9) 0%, transparent 70%);
    border-radius: 50%;
  }
  .lamp-glow {
    position: absolute; bottom: 0; left: 50%; transform: translateX(-50%);
    width: 120px; height: 80px;
    background: radial-gradient(ellipse 50% 40% at 50% 0%, rgba(255,180,50,0.06) 0%, transparent 100%);
    pointer-events: none;
  }

  .puddle {
    position: absolute; bottom: 20px;
    width: 60px; height: 10px;
    background: radial-gradient(ellipse, rgba(100,130,200,0.15) 0%, transparent 70%);
    border-radius: 50%;
    animation: puddle-shimmer 3s ease-in-out infinite;
  }
</style>
