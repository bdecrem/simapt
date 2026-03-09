<script>
  import { gameState } from '../../lib/stores/game.js';

  let month = $derived(Math.ceil($gameState.day / 30));
  let dayOfMonth = $derived((($gameState.day - 1) % 30) + 1);
</script>

<div class="day-counter">
  <div class="day-label">MONTH</div>
  <div class="day-num">{month}</div>
  <div class="month-label">DAY {dayOfMonth}</div>
</div>

<style>
  .day-counter {
    position: absolute;
    top: 50%; left: 50%;
    transform: translate(-50%, -200%);
    z-index: 35;
    text-align: center;
    pointer-events: none;
  }
  .day-label {
    font-family: 'Press Start 2P', monospace;
    font-size: 8px;
    color: var(--muted);
    letter-spacing: 2px;
    margin-bottom: 2px;
  }
  .day-num {
    font-family: 'VT323', monospace;
    font-size: 48px;
    color: var(--cream);
    text-shadow: 0 0 20px rgba(240,228,192,0.2);
    line-height: 1;
  }
  .month-label {
    font-family: 'VT323', monospace;
    font-size: 18px;
    color: var(--muted);
    letter-spacing: 3px;
  }
</style>
