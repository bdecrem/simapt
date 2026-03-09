<script>
  import { onMount } from 'svelte';

  let stars = $state([]);

  onMount(() => {
    stars = Array.from({ length: 80 }, () => ({
      size: Math.random() * 1.5 + 0.5,
      top: Math.random() * 55,
      left: Math.random() * 100,
      dim: Math.random() * 0.3 + 0.1,
      bright: Math.random() * 0.5 + 0.4,
      duration: Math.random() * 4 + 2,
      delay: -Math.random() * 5,
    }));
  });
</script>

<div class="sky">
  {#each stars as star}
    <div
      class="star"
      style="
        width: {star.size}px; height: {star.size}px;
        top: {star.top}%; left: {star.left}%;
        --dim: {star.dim}; --bright: {star.bright};
        --d: {star.duration}s; --delay: {star.delay}s;
      "
    ></div>
  {/each}
</div>

<style>
  .sky {
    position: absolute;
    inset: 0;
    background: radial-gradient(ellipse 80% 60% at 50% -10%, #1a2240 0%, #0d0f1a 60%);
  }

  .star {
    position: absolute;
    background: #fff;
    border-radius: 50%;
    animation: twinkle var(--d, 3s) ease-in-out infinite var(--delay, 0s);
  }
</style>
