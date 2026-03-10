<script>
  import { gameState } from '../../lib/stores/game.js';
  import { fixTask } from '../../lib/api.js';

  let fixing = $state(null);
  let fixed = $state(null); // for pop animation

  async function handleFix(task) {
    if (fixing) return;
    fixing = task.id;
    try {
      const state = await fixTask(task.id);
      fixed = { id: task.id, x: task.x, y: task.y, rep: task.rep_reward };
      $gameState = state;
      setTimeout(() => { fixed = null; }, 800);
    } catch (e) {
      console.error('Failed to fix task:', e);
    }
    fixing = null;
  }
</script>

<div class="task-overlay">
  {#each $gameState.maintenance_tasks || [] as task (task.id)}
    <button
      class="task-icon"
      class:fixing={fixing === task.id}
      style="left: {task.x * 100}%; top: {task.y * 100}%"
      title="{task.label}{task.money_cost > 0 ? ` (-$${task.money_cost})` : ' (free)'}"
      onclick={() => handleFix(task)}
      disabled={!!fixing}
    >
      <span class="icon-emoji">{task.icon}</span>
    </button>
  {/each}

  {#if fixed}
    <div
      class="fix-pop"
      style="left: {fixed.x * 100}%; top: {fixed.y * 100}%"
    >
      +{fixed.rep} rep
    </div>
  {/if}
</div>

<style>
  .task-overlay {
    position: absolute;
    inset: 0;
    z-index: 20;
    pointer-events: none;
  }

  .task-icon {
    position: absolute;
    transform: translate(-50%, -50%);
    width: 32px;
    height: 32px;
    border-radius: 50%;
    background: rgba(212, 136, 42, 0.85);
    border: 2px solid rgba(255, 200, 80, 0.6);
    cursor: pointer;
    pointer-events: all;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    animation: task-pulse 2s ease-in-out infinite;
    transition: transform 0.15s, background 0.15s;
    box-shadow: 0 0 8px rgba(212, 136, 42, 0.4);
  }

  .task-icon:hover {
    transform: translate(-50%, -50%) scale(1.25);
    background: rgba(255, 180, 50, 0.95);
    box-shadow: 0 0 16px rgba(255, 180, 50, 0.6);
  }

  .task-icon:active {
    transform: translate(-50%, -50%) scale(0.9);
  }

  .task-icon.fixing {
    opacity: 0.5;
    pointer-events: none;
  }

  .task-icon:disabled {
    cursor: default;
  }

  .icon-emoji {
    font-size: 16px;
    line-height: 1;
    filter: saturate(0.8);
  }

  .fix-pop {
    position: absolute;
    transform: translate(-50%, -50%);
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: var(--amber);
    text-shadow: 0 0 6px rgba(212, 136, 42, 0.8);
    pointer-events: none;
    animation: pop-up 0.8s ease-out forwards;
    white-space: nowrap;
  }

  @keyframes task-pulse {
    0%, 100% { box-shadow: 0 0 6px rgba(212, 136, 42, 0.3); }
    50% { box-shadow: 0 0 14px rgba(212, 136, 42, 0.6); }
  }

  @keyframes pop-up {
    0% { opacity: 1; transform: translate(-50%, -50%) translateY(0); }
    100% { opacity: 0; transform: translate(-50%, -50%) translateY(-30px); }
  }
</style>
