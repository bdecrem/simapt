<script>
  import { onMount } from 'svelte';
  import { gameState, isLoading } from '../../lib/stores/game.js';
  import Sky from './Sky.svelte';
  import Rain from './Rain.svelte';
  import Building from './Building.svelte';
  import Header from '../ui/Header.svelte';
  import StatusPanel from '../ui/StatusPanel.svelte';
  import NoticePanel from '../ui/NoticePanel.svelte';
  import DayCounter from '../ui/DayCounter.svelte';
  import Ticker from '../ui/Ticker.svelte';
  import NextDayButton from '../ui/NextDayButton.svelte';

  let { onadvanceday, onselectunit } = $props();

  let canvas;
  let scale = $state(1);

  function scaleCanvas() {
    const scaleX = window.innerWidth / 1080;
    const scaleY = window.innerHeight / 700;
    scale = Math.min(scaleX, scaleY);
  }

  onMount(() => {
    scaleCanvas();
    window.addEventListener('resize', scaleCanvas);
    return () => window.removeEventListener('resize', scaleCanvas);
  });
</script>

<div
  class="game-canvas"
  bind:this={canvas}
  style="transform: scale({scale})"
>
  <div class="scene">
    <Sky />
    <Rain />

    <!-- Neighbor buildings -->
    <div class="neighbor left">
      {#each [['warm',''], ['','dim'], ['warm','warm'], ['','']] as [a, b]}
        <div class="nb-floor">
          <div class="nb-window {a}"></div>
          <div class="nb-window {b}"></div>
        </div>
      {/each}
    </div>
    <div class="neighbor right">
      {#each [['warm',''], ['','warm'], ['dim',''], ['','dim']] as [a, b]}
        <div class="nb-floor">
          <div class="nb-window {a}"></div>
          <div class="nb-window {b}"></div>
        </div>
      {/each}
    </div>

    <Building onselectunit={onselectunit} />
  </div>

  <Header />
  <DayCounter />
  <StatusPanel />
  <NoticePanel />
  <NextDayButton onclick={onadvanceday} disabled={$isLoading || !!$gameState.active_scenario} />
  <Ticker />

  <div class="scanlines"></div>
  <div class="vignette"></div>
</div>

<style>
  .game-canvas {
    position: relative;
    width: 1080px;
    height: 700px;
    transform-origin: center center;
    flex-shrink: 0;
  }

  .scene {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: flex-end;
    justify-content: center;
  }

  .neighbor {
    position: absolute;
    bottom: 80px;
    z-index: 5;
    background: #1a110a;
    display: flex;
    flex-direction: column;
  }
  .neighbor.left { left: 0; width: 110px; height: 200px; }
  .neighbor.right { right: 0; width: 90px; height: 160px; }
  .nb-floor {
    display: flex;
    justify-content: center;
    gap: 8px;
    padding: 8px 10px;
    border-bottom: 1px solid rgba(0,0,0,0.4);
  }
  .nb-window {
    width: 24px;
    height: 28px;
    background: #0e1018;
    border: 2px solid #100c08;
  }
  .nb-window.warm { background: rgba(232,168,50,0.6); }
  .nb-window.dim { background: rgba(50,60,100,0.4); }

  .scanlines {
    position: absolute;
    inset: 0;
    z-index: 50;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 4px);
    pointer-events: none;
  }

  .vignette {
    position: absolute;
    inset: 0;
    z-index: 45;
    background: radial-gradient(ellipse 80% 80% at 50% 50%, transparent 50%, rgba(0,0,0,0.5) 100%);
    pointer-events: none;
  }
</style>
