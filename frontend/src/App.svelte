<script>
  import { gameState, selectedUnit, showNarration, isLoading } from './lib/stores/game.js';
  import { newGame, advanceDay, makeChoice } from './lib/api.js';
  import GameCanvas from './components/scene/GameCanvas.svelte';
  import ScenarioCard from './components/game/ScenarioCard.svelte';
  import NarrationOverlay from './components/game/NarrationOverlay.svelte';
  import TenantDetail from './components/game/TenantDetail.svelte';
  import EndScreen from './components/game/EndScreen.svelte';
  import MenuScreen from './components/game/MenuScreen.svelte';

  async function handleNewGame() {
    $isLoading = true;
    try {
      const state = await newGame();
      $gameState = { ...state, phase: state.phase || 'playing' };
    } catch (e) {
      console.error('Failed to start game:', e);
    }
    $isLoading = false;
  }

  async function handleAdvanceDay() {
    if ($gameState.active_scenario || $gameState.phase !== 'playing') return;
    $isLoading = true;
    try {
      const state = await advanceDay();
      $gameState = state;
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
  <MenuScreen onstart={handleNewGame} />
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

  {#if $gameState.phase === 'won' || $gameState.phase === 'lost'}
    <EndScreen phase={$gameState.phase} onrestart={handleNewGame} />
  {/if}
{/if}
