<script>
  let { scenario, onchoose } = $props();

  function handleChoice(choiceId) {
    onchoose?.(choiceId);
  }
</script>

<div class="overlay">
  <div class="card">
    <div class="card-header">
      <span class="card-tier">TIER {scenario.definition.tier}</span>
      <h2 class="card-title">{scenario.definition.title}</h2>
    </div>

    {#if scenario.flavor_text}
      <p class="flavor">{scenario.flavor_text}</p>
    {/if}

    <p class="description">{scenario.description}</p>

    <div class="tenant-tag">
      RE: {scenario.tenant_name}
    </div>

    <div class="choices">
      {#each scenario.definition.choices as choice}
        <button class="choice-btn" onclick={() => handleChoice(choice.id)}>
          <span class="choice-label">{choice.label}</span>
          <span class="choice-desc">{choice.desc}</span>
          <span class="choice-effects">
            {#if choice.rep > 0}
              <span class="effect positive">+{choice.rep} rep</span>
            {/if}
            {#if choice.rep < 0}
              <span class="effect negative">{choice.rep} rep</span>
            {/if}
            {#if choice.money > 0}
              <span class="effect positive">+${choice.money}</span>
            {/if}
            {#if choice.money < 0}
              <span class="effect negative">-${Math.abs(choice.money)}</span>
            {/if}
          </span>
        </button>
      {/each}
    </div>
  </div>
</div>

<style>
  .overlay {
    position: fixed;
    inset: 0;
    z-index: 100;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    align-items: center;
    justify-content: center;
    animation: fade-in 0.3s ease-out;
  }

  .card {
    background: rgba(13, 15, 26, 0.97);
    border: 2px solid var(--amber);
    padding: 32px;
    max-width: 480px;
    width: 90%;
    animation: slide-up 0.4s ease-out;
  }

  .card-header {
    margin-bottom: 16px;
  }
  .card-tier {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: var(--muted);
    letter-spacing: 2px;
  }
  .card-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 14px;
    color: var(--cream);
    margin-top: 8px;
    letter-spacing: 1px;
    line-height: 1.6;
  }

  .flavor {
    font-family: 'VT323', monospace;
    font-size: 18px;
    color: var(--amber);
    line-height: 1.5;
    margin-bottom: 16px;
    font-style: italic;
    opacity: 0.8;
  }

  .description {
    font-family: 'VT323', monospace;
    font-size: 20px;
    color: var(--cream);
    line-height: 1.5;
    margin-bottom: 16px;
  }

  .tenant-tag {
    font-family: 'Press Start 2P', monospace;
    font-size: 7px;
    color: var(--muted);
    letter-spacing: 1px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 1px solid rgba(210,136,42,0.2);
  }

  .choices {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }

  .choice-btn {
    background: rgba(42, 32, 16, 0.6);
    border: 1px solid rgba(210,136,42,0.3);
    padding: 14px 16px;
    text-align: left;
    cursor: pointer;
    transition: all 0.2s;
    display: flex;
    flex-direction: column;
    gap: 4px;
  }
  .choice-btn:hover {
    background: rgba(212, 136, 42, 0.15);
    border-color: var(--amber);
  }

  .choice-label {
    font-family: 'VT323', monospace;
    font-size: 22px;
    color: var(--cream);
  }
  .choice-desc {
    font-family: 'VT323', monospace;
    font-size: 16px;
    color: var(--muted);
  }
  .choice-effects {
    display: flex;
    gap: 12px;
    margin-top: 4px;
  }
  .effect {
    font-family: 'VT323', monospace;
    font-size: 14px;
  }
  .effect.positive { color: var(--green); }
  .effect.negative { color: var(--red-dim); }
</style>
