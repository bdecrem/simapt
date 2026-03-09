<script>
  let { narration, ondismiss } = $props();
</script>

<div class="overlay">
  <div class="narration-card">
    <p class="narration-text">{narration.text}</p>

    {#if narration.choiceResult}
      <div class="effects">
        {#if narration.choiceResult.rep_change !== 0}
          <span class="effect" class:positive={narration.choiceResult.rep_change > 0} class:negative={narration.choiceResult.rep_change < 0}>
            {narration.choiceResult.rep_change > 0 ? '+' : ''}{narration.choiceResult.rep_change} rep
          </span>
        {/if}
        {#if narration.choiceResult.money_change !== 0}
          <span class="effect" class:positive={narration.choiceResult.money_change > 0} class:negative={narration.choiceResult.money_change < 0}>
            {narration.choiceResult.money_change > 0 ? '+' : ''}${narration.choiceResult.money_change}
          </span>
        {/if}
      </div>
    {/if}

    <button class="continue-btn" onclick={ondismiss}>Continue</button>
  </div>
</div>

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 100;
    background: rgba(0, 0, 0, 0.75);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fade-in 0.3s ease-out;
  }

  .narration-card {
    background: rgba(13, 15, 26, 0.97);
    border: 2px solid var(--muted);
    padding: 40px;
    max-width: 460px;
    width: 90%;
    text-align: center;
    animation: slide-up 0.4s ease-out;
  }

  .narration-text {
    font-family: 'VT323', monospace;
    font-size: 22px;
    color: var(--cream);
    line-height: 1.6;
    margin-bottom: 24px;
  }

  .effects {
    display: flex;
    gap: 16px;
    justify-content: center;
    margin-bottom: 24px;
  }
  .effect {
    font-family: 'VT323', monospace;
    font-size: 18px;
  }
  .effect.positive { color: var(--green); }
  .effect.negative { color: var(--red-dim); }

  .continue-btn {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: var(--cream);
    background: rgba(42, 32, 16, 0.6);
    border: 1px solid var(--amber);
    padding: 10px 28px;
    cursor: pointer;
    letter-spacing: 2px;
  }
  .continue-btn:hover {
    background: rgba(212, 136, 42, 0.2);
  }
</style>
