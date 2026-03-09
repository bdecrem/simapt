<script>
  import { onMount } from 'svelte';

  let { unitIndex, tenant, unlocked, onclick } = $props();

  let windowState = $state('dark');
  let flickerInterval;

  // Determine window visual state from tenant
  $effect(() => {
    if (!unlocked) {
      windowState = 'boarded';
    } else if (!tenant) {
      windowState = 'dark';
    } else if (tenant.stats.suspicion > 50) {
      windowState = 'red';
    } else if (tenant.stats.happiness > 60) {
      windowState = 'warm';
    } else if (tenant.stats.happiness > 30) {
      windowState = 'cool';
    } else {
      windowState = 'dark';
    }
  });

  // Random flicker for occupied windows
  onMount(() => {
    flickerInterval = setInterval(() => {
      if (!tenant || !unlocked) return;
      if (windowState === 'red') return; // suspicious units stay red
      if (Math.random() < 0.15) {
        const states = ['warm', 'cool', 'tv', 'dark'];
        windowState = states[Math.floor(Math.random() * states.length)];
      }
    }, 5000 + Math.random() * 5000);

    return () => clearInterval(flickerInterval);
  });

  function getTitle() {
    if (!unlocked) return `Unit ${unitIndex + 1} — Locked`;
    if (!tenant) return `Unit ${unitIndex + 1} — Vacant`;
    return `Unit ${unitIndex + 1} — ${tenant.name}\nRent: $${tenant.rent}/mo`;
  }
</script>

<button
  class="window {windowState}"
  title={getTitle()}
  onclick={onclick}
  disabled={!unlocked}
>
  {#if tenant && windowState !== 'dark'}
    {#if Math.random() > 0.5}
      <div class="sil sil-person"></div>
    {/if}
  {/if}
  {#if windowState === 'tv' || windowState === 'red'}
    <div class="blinds"></div>
  {/if}
  <span class="unit-label">{unitIndex + 1}</span>
</button>

<style>
  .window {
    width: 80px;
    height: 80px;
    background: var(--window-off);
    border: 3px solid #1a140c;
    position: relative;
    overflow: hidden;
    image-rendering: pixelated;
    cursor: pointer;
    transition: filter 0.3s;
    padding: 0;
  }
  .window:hover:not(:disabled) { filter: brightness(1.2); }
  .window:disabled { cursor: default; opacity: 0.5; }

  .window::before {
    content: '';
    position: absolute;
    top: 0; bottom: 0; left: 50%;
    width: 2px;
    background: rgba(0,0,0,0.4);
    z-index: 3;
  }
  .window::after {
    content: '';
    position: absolute;
    left: 0; right: 0; top: 50%;
    height: 2px;
    background: rgba(0,0,0,0.4);
    z-index: 3;
  }

  .window.warm {
    background: var(--window-warm);
    box-shadow: 0 0 12px 3px rgba(232, 168, 50, 0.4), inset 0 0 20px rgba(255,200,80,0.3);
  }
  .window.cool {
    background: var(--window-cool);
    box-shadow: 0 0 10px 2px rgba(122,179,212,0.3), inset 0 0 16px rgba(150,200,240,0.2);
  }
  .window.tv {
    background: var(--window-tv);
    animation: tv-flicker 0.12s steps(1) infinite;
  }
  .window.red {
    background: #6b1515;
    box-shadow: 0 0 8px 2px rgba(150,30,30,0.3);
  }
  .window.dark { background: #0e1018; }
  .window.boarded {
    background: #0a0c14;
    border-color: #0e0a06;
  }

  .sil {
    position: absolute;
    z-index: 4;
    bottom: 8px;
  }
  .sil-person {
    left: 12px;
    width: 12px;
    height: 32px;
    background: rgba(0,0,0,0.5);
    clip-path: polygon(20% 0%, 80% 0%, 100% 40%, 70% 40%, 70% 100%, 30% 100%, 30% 40%, 0% 40%);
  }

  .blinds {
    position: absolute;
    inset: 0;
    z-index: 5;
    background: repeating-linear-gradient(180deg, rgba(0,0,0,0.35) 0px, rgba(0,0,0,0.35) 4px, transparent 4px, transparent 8px);
  }

  .unit-label {
    position: absolute;
    bottom: 3px;
    right: 5px;
    font-family: 'Press Start 2P', monospace;
    font-size: 6px;
    color: rgba(0,0,0,0.4);
    z-index: 10;
  }
</style>
