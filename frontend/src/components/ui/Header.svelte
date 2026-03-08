<script>
</script>

<div class="title-ui">
  <div class="game-title">THE<br>BRAMBLE</div>
  <div class="game-subtitle">a building sim</div>
  <div class="game-tagline">Eight units.<br>Eight lives.<br>Zero easy answers.</div>
</div>

<div class="nameplate">
  <div class="building-name">Waverly Arms</div>
  <div class="address">412 Dunmore St.</div>
</div>

<style>
  .title-ui {
    position: absolute;
    top: 0; left: 0; right: 0;
    z-index: 30;
    padding: 28px 40px 0;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    pointer-events: none;
  }
  .game-title {
    font-family: 'Press Start 2P', monospace;
    font-size: 28px;
    color: var(--cream);
    text-shadow: 3px 3px 0 #5a3a10, 6px 6px 0 rgba(0,0,0,0.5);
    letter-spacing: 2px;
    line-height: 1.4;
    margin-bottom: 6px;
  }
  .game-subtitle {
    font-family: 'VT323', monospace;
    font-size: 20px;
    color: var(--amber);
    letter-spacing: 3px;
    margin-bottom: 18px;
    text-transform: uppercase;
  }
  .game-tagline {
    font-family: 'VT323', monospace;
    font-size: 16px;
    color: var(--muted);
    max-width: 360px;
    line-height: 1.6;
  }

  .nameplate {
    position: absolute;
    top: 28px; right: 40px;
    z-index: 30;
    text-align: right;
    pointer-events: none;
  }
  .building-name {
    font-family: 'Press Start 2P', monospace;
    font-size: 9px;
    color: var(--muted);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 6px;
  }
  .address {
    font-family: 'VT323', monospace;
    font-size: 20px;
    color: rgba(120,110,90,0.7);
  }
</style>
