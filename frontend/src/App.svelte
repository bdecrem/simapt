<script>
  import { gameState, selectedUnit, showNarration, isLoading } from './lib/stores/game.js';
  import { newGame, advanceDay, makeChoice, getState, clearGame } from './lib/api.js';
  import GameCanvas from './components/scene/GameCanvas.svelte';
  import ScenarioCard from './components/game/ScenarioCard.svelte';
  import NarrationOverlay from './components/game/NarrationOverlay.svelte';
  import TenantDetail from './components/game/TenantDetail.svelte';
  import EndScreen from './components/game/EndScreen.svelte';
  import MenuScreen from './components/game/MenuScreen.svelte';

  async function handleNewGame() {
    clearGame();
    $isLoading = true;
    try {
      const state = await newGame();
      $gameState = { ...state, phase: state.phase || 'playing' };
    } catch (e) {
      console.error('Failed to start game:', e);
    }
    $isLoading = false;
  }

  async function handleContinue() {
    $isLoading = true;
    try {
      const state = await getState();
      $gameState = { ...state, phase: state.phase || 'playing' };
    } catch (e) {
      console.error('Failed to load game:', e);
      clearGame();
    }
    $isLoading = false;
  }

  let dayFlash = $state(false);

  async function handleAdvanceDay() {
    if ($gameState.active_scenario || $gameState.phase !== 'playing') return;
    $isLoading = true;
    try {
      const state = await advanceDay();
      $gameState = state;
      // Brief flash to show day advanced
      dayFlash = true;
      setTimeout(() => dayFlash = false, 400);
    } catch (e) {
      console.error('Failed to advance day:', e);
    }
    $isLoading = false;
  }

  async function handleChoice(choiceId) {
    $isLoading = true;
    try {
      const result = await makeChoice(choiceId);
      $showNarration = {
        text: result.narration,
        choiceResult: result.choice_result,
      };
      $gameState = result;
    } catch (e) {
      console.error('Failed to make choice:', e);
    }
    $isLoading = false;
  }

  function handleDismissNarration() {
    $showNarration = null;
  }

  function handleSelectUnit(unitIndex) {
    $selectedUnit = $selectedUnit === unitIndex ? null : unitIndex;
  }
</script>

{#if $gameState.phase === 'menu'}
  <MenuScreen onstart={handleNewGame} oncontinue={handleContinue} />
{:else}
  <GameCanvas
    onadvanceday={handleAdvanceDay}
    onselectunit={handleSelectUnit}
  />

  {#if $gameState.active_scenario && !$showNarration}
    <ScenarioCard
      scenario={$gameState.active_scenario}
      onchoose={handleChoice}
    />
  {/if}

  {#if $showNarration}
    <NarrationOverlay
      narration={$showNarration}
      ondismiss={handleDismissNarration}
    />
  {/if}

  {#if $selectedUnit !== null}
    <TenantDetail
      unitIndex={$selectedUnit}
      onclose={() => $selectedUnit = null}
    />
  {/if}

  {#if dayFlash}
    <div class="day-flash"></div>
  {/if}

  {#if $gameState.phase === 'won' || $gameState.phase === 'lost'}
    <EndScreen phase={$gameState.phase} onrestart={handleNewGame} />
  {/if}
{/if}

<style>
  .day-flash {
    position: fixed;
    inset: 0;
    z-index: 200;
    background: rgba(212, 136, 42, 0.08);
    pointer-events: none;
    animation: flash-fade 0.4s ease-out forwards;
  }
  @keyframes flash-fade {
    0% { opacity: 1; }
    100% { opacity: 0; }
  }
</style>
