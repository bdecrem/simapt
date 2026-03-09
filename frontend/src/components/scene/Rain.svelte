<script>
  import { onMount } from 'svelte';

  let canvas;

  onMount(() => {
    const ctx = canvas.getContext('2d');
    canvas.width = 1080;
    canvas.height = 700;

    const drops = Array.from({ length: 120 }, () => ({
      x: Math.random() * 1080,
      y: Math.random() * 700,
      len: Math.random() * 14 + 6,
      speed: Math.random() * 8 + 6,
      opacity: Math.random() * 0.4 + 0.1,
    }));

    let animId;
    function animate() {
      ctx.clearRect(0, 0, 1080, 700);
      ctx.strokeStyle = 'rgba(180, 200, 230, 1)';
      for (const d of drops) {
        ctx.globalAlpha = d.opacity;
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.moveTo(d.x, d.y);
        ctx.lineTo(d.x - d.len * 0.2, d.y + d.len);
        ctx.stroke();
        d.y += d.speed;
        d.x -= d.speed * 0.2;
        if (d.y > 720) {
          d.y = -20;
          d.x = Math.random() * 1080;
        }
      }
      ctx.globalAlpha = 1;
      animId = requestAnimationFrame(animate);
    }
    animate();

    return () => cancelAnimationFrame(animId);
  });
</script>

<canvas bind:this={canvas} class="rain"></canvas>

<style>
  .rain {
    position: absolute;
    inset: 0;
    pointer-events: none;
    z-index: 20;
    opacity: 0.35;
  }
</style>
