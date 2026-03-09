<script>
  let { onclick, disabled = false } = $props();
</script>

<button class="next-day" onclick={onclick} {disabled}>
  {disabled ? '...' : 'NEXT DAY ▸'}
</button>

<style>
  .next-day {
    position: absolute;
    bottom: 50px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 38;
    font-family: 'Press Start 2P', monospace;
    font-size: 10px;
    color: var(--cream);
    background: rgba(58, 34, 24, 0.9);
    border: 2px solid var(--amber);
    padding: 10px 24px;
    letter-spacing: 2px;
    cursor: pointer;
    transition: all 0.2s;
  }
  .next-day:hover:not(:disabled) {
    background: rgba(212, 136, 42, 0.3);
    box-shadow: 0 0 15px rgba(212, 136, 42, 0.3);
  }
  .next-day:disabled {
    opacity: 0.4;
    cursor: default;
  }
</style>
