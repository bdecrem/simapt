<script>
  import { gameState } from '../../lib/stores/game.js';

  let { phase, onrestart } = $props();

  let title = $derived(phase === 'won' ? 'LEGENDARY' : 'GAME OVER');
  let subtitle = $derived(phase === 'won'
    ? 'The Bramble has become the building everyone talks about.'
    : $gameState.money < 0
      ? 'The bank called. The building is theirs now.'
      : 'The last tenant left. The building stands empty.'
  );
</script>

<div class="overlay">
  <div class="end-card">
    <h1 class="end-title" class:won={phase === 'won'}>{title}</h1>
    <p class="end-subtitle">{subtitle}</p>

    <div class="final-stats">
      <div class="final-stat">
        <span class="label">Days</span>
        <span class="value">{$gameState.day}</span>
      </div>
      <div class="final-stat">
        <span class="label">Rep</span>
        <span class="value">{$gameState.rep}</span>
      </div>
      <div class="final-stat">
        <span class="label">Money</span>
        <span class="value">${$gameState.money}</span>
      </div>
      <div class="final-stat">
        <span class="label">Tenants</span>
        <span class="value">{$gameState.tenants.length}</span>
      </div>
    </div>

    <button class="restart-btn" onclick={onrestart}>PLAY AGAIN</button>
  </div>
</div>

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 200;
    background: rgba(0, 0, 0, 0.85);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fade-in 0.5s ease-out;
  }

  .end-card {
    text-align: center;
    animation: slide-up 0.6s ease-out;
  }

  .end-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 32px;
    color: var(--red-dim);
    letter-spacing: 4px;
    margin-bottom: 16px;
  }
  .end-title.won {
    color: var(--amber);
    text-shadow: 0 0 30px rgba(212, 136, 42, 0.5);
  }

  .end-subtitle {
    font-family: 'VT323', monospace;
    font-size: 22px;
    color: var(--cream);
    margin-bottom: 40px;
    max-width: 400px;
    line-height: 1.5;
  }

  .final-stats {
    display: flex;
    gap: 32px;
    justify-content: center;
    margin-bottom: 40px;
  }
  .final-stat {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  .label {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: var(--muted);
    letter-spacing: 1px;
    margin-bottom: 4px;
  }
  .value {
    font-family: 'VT323', monospace;
    font-size: 28px;
    color: var(--cream);
  }

  .restart-btn {
    font-family: 'Press Start 2P', monospace;
    font-size: 10px;
    color: var(--cream);
    background: rgba(42, 32, 16, 0.6);
    border: 2px solid var(--amber);
    padding: 12px 32px;
    cursor: pointer;
    letter-spacing: 2px;
  }
  .restart-btn:hover {
    background: rgba(212, 136, 42, 0.2);
  }
</style>
