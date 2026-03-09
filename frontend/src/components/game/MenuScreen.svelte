<script>
  import { onMount } from 'svelte';
  import { hasGame, clearGame } from '../../lib/api.js';

  let { onstart, oncontinue } = $props();
  let savedGame = $state(hasGame());
  let stars = $state([]);

  onMount(() => {
    stars = Array.from({ length: 60 }, () => ({
      size: Math.random() * 1.5 + 0.5,
      top: Math.random() * 100,
      left: Math.random() * 100,
      dim: Math.random() * 0.3 + 0.1,
      bright: Math.random() * 0.5 + 0.4,
      duration: Math.random() * 4 + 2,
      delay: -Math.random() * 5,
    }));
  });
</script>

<div class="menu">
  <div class="sky">
    {#each stars as star}
      <div
        class="star"
        style="
          width: {star.size}px; height: {star.size}px;
          top: {star.top}%; left: {star.left}%;
          --dim: {star.dim}; --bright: {star.bright};
          --d: {star.duration}s; --delay: {star.delay}s;
        "
      ></div>
    {/each}
  </div>

  <div class="menu-content">
    <h1 class="title">THE<br>BRAMBLE</h1>
    <p class="subtitle">A BUILDING SIM</p>
    <p class="tagline">Eight units. Eight lives. Zero easy answers.</p>
    {#if savedGame}
      <button class="start-btn" onclick={oncontinue}>CONTINUE</button>
      <button class="start-btn secondary" onclick={() => { clearGame(); savedGame = false; }}>NEW GAME</button>
    {:else}
      <button class="start-btn" onclick={onstart}>START GAME</button>
    {/if}
  </div>

  <div class="scanlines"></div>
</div>

<style>
  .menu {
    position: fixed;
    inset: 0;
    background: #060708;
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 300;
  }

  .sky {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% 30%, #1a2240 0%, #0d0f1a 60%);
  }

  .star {
    position: absolute;
    background: #fff;
    border-radius: 50%;
    animation: twinkle var(--d, 3s) ease-in-out infinite var(--delay, 0s);
  }

  .menu-content {
    position: relative;
    z-index: 10;
    text-align: center;
    animation: fade-in 1s ease-out;
  }

  .title {
    font-family: 'Press Start 2P', monospace;
    font-size: 48px;
    color: var(--cream);
    text-shadow: 4px 4px 0 #5a3a10, 8px 8px 0 rgba(0,0,0,0.5);
    letter-spacing: 4px;
    line-height: 1.3;
    margin-bottom: 16px;
  }

  .subtitle {
    font-family: 'VT323', monospace;
    font-size: 24px;
    color: var(--amber);
    letter-spacing: 6px;
    text-transform: uppercase;
    margin-bottom: 32px;
  }

  .tagline {
    font-family: 'VT323', monospace;
    font-size: 20px;
    color: var(--muted);
    margin-bottom: 48px;
    line-height: 1.6;
  }

  .start-btn {
    font-family: 'Press Start 2P', monospace;
    font-size: 12px;
    color: var(--cream);
    background: rgba(42, 32, 16, 0.6);
    border: 2px solid var(--amber);
    padding: 14px 40px;
    cursor: pointer;
    letter-spacing: 3px;
    transition: all 0.3s;
  }
  .start-btn:hover {
    background: rgba(212, 136, 42, 0.25);
    box-shadow: 0 0 30px rgba(212, 136, 42, 0.3);
    transform: scale(1.05);
  }
  .start-btn.secondary {
    margin-top: 12px;
    font-size: 9px;
    border-color: var(--muted);
    opacity: 0.6;
  }
  .start-btn.secondary:hover {
    opacity: 1;
  }

  .scanlines {
    position: absolute;
    inset: 0;
    z-index: 20;
    background: repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,0,0,0.05) 2px, rgba(0,0,0,0.05) 4px);
    pointer-events: none;
  }
</style>
