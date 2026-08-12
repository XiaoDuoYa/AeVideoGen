(() => {
  const FPS = 30;
  const DURATION = 30;
  const capture = new URLSearchParams(location.search).has("capture");
  if (capture) document.body.classList.add("capture");

  const $ = (selector) => document.querySelector(selector);
  const clamp = (value, min = 0, max = 1) => Math.min(max, Math.max(min, value));
  const progress = (time, start, end) => clamp((time - start) / (end - start));
  const ease = (value) => 1 - Math.pow(1 - clamp(value), 3);
  const lerp = (from, to, amount) => from + (to - from) * amount;
  const set = (element, values) => Object.assign(element.style, values);

  const titleScene = $("#titleScene");
  const heroTitle = $("#heroTitle");
  const productScene = $("#productScene");
  const productShell = $("#productShell");
  const demoButton = $("#demoButton");
  const pointer = $("#pointer");
  const valueScene = $("#valueScene");
  const valueTitle = $("#valueTitle");
  const score = $("#score");

  function render(time) {
    const t = clamp(Number(time) || 0, 0, DURATION);
    const introIn = ease(progress(t, 0, 1.2));
    const introOut = ease(progress(t, 5.8, 7.2));
    set(titleScene, {
      opacity: String(introIn * (1 - introOut)),
      transform: `translate3d(${lerp(42, -30, introOut)}px, ${lerp(18, -18, introOut)}px, 0) scale(${lerp(.96, 1.025, introIn)})`,
      filter: `blur(${lerp(10, 0, introIn) + lerp(0, 8, introOut)}px)`,
    });
    set(heroTitle, { letterSpacing: `${lerp(-.025, -.055, introIn)}em` });

    const productIn = ease(progress(t, 6.2, 8.0));
    const productOut = ease(progress(t, 20.8, 22.4));
    const focus = ease(progress(t, 11.5, 14.0)) * (1 - ease(progress(t, 17.8, 20.2)));
    set(productScene, {
      opacity: String(productIn * (1 - productOut)),
      transform: `translate3d(0, ${lerp(28, -14, productIn)}px, 0)`,
      filter: `blur(${lerp(8, 0, productIn) + lerp(0, 10, productOut)}px)`,
    });
    set(productShell, {
      transform: `translate3d(${lerp(0, -96, focus)}px, ${lerp(0, 104, focus)}px, 0) scale(${lerp(.88, 1.82, focus)})`,
    });

    const buttonRect = demoButton.getBoundingClientRect();
    const stageRect = $("#stage").getBoundingClientRect();
    const clickX = buttonRect.left - stageRect.left + buttonRect.width / 2;
    const clickY = buttonRect.top - stageRect.top + buttonRect.height / 2;
    const pointerIn = ease(progress(t, 10.0, 11.4));
    const clickPulse = Math.sin(progress(t, 13.6, 14.2) * Math.PI);
    set(pointer, {
      opacity: String(productIn * (1 - productOut) * pointerIn),
      left: `${lerp(stageRect.width * .78, clickX, pointerIn)}px`,
      top: `${lerp(stageRect.height * .2, clickY, pointerIn)}px`,
      transform: `translate(-50%, -50%) scale(${1 - clickPulse * .22})`,
      boxShadow: `0 0 0 ${lerp(8, 22, clickPulse)}px rgba(112,228,173,${lerp(.12, 0, clickPulse)})`,
    });

    const valueIn = ease(progress(t, 21.4, 23.4));
    const valueOut = ease(progress(t, 28.4, 30));
    const breathing = Math.sin(t * 1.15) * .008;
    set(valueScene, {
      opacity: String(valueIn * (1 - valueOut)),
      transform: `translate3d(0, ${lerp(34, -8, valueIn)}px, 0) scale(${1 + breathing})`,
      filter: `blur(${lerp(12, 0, valueIn) + lerp(0, 8, valueOut)}px)`,
    });
    set(valueTitle, { transform: `scale(${lerp(.92, 1, valueIn)})` });

    updateControls(t);
    return t;
  }

  let currentTime = 0;
  let playing = false;
  let lastNow = 0;
  let raf = 0;
  const scrubber = $("#scrubber");
  const timeInput = $("#timeInput");
  const frameInput = $("#frameInput");
  const readout = $("#readout");
  const playPause = $("#playPause");

  function formatTime(time) {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    const millis = Math.floor((time % 1) * 1000);
    return `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}.${String(millis).padStart(3, "0")}`;
  }

  function updateControls(time) {
    currentTime = clamp(time, 0, DURATION);
    if (!capture) {
      const frame = Math.round(currentTime * FPS);
      scrubber.value = String(currentTime);
      timeInput.value = currentTime.toFixed(3);
      frameInput.value = String(frame);
      readout.value = `${formatTime(currentTime)} · ${String(frame).padStart(4, "0")} / ${String(Math.round(DURATION * FPS)).padStart(4, "0")}`;
      playPause.textContent = playing ? "❚❚" : "▶";
    }
  }

  function seek(time) {
    currentTime = clamp(Number(time) || 0, 0, DURATION);
    if (score.src) score.currentTime = currentTime;
    render(currentTime);
  }

  function pause() {
    playing = false;
    cancelAnimationFrame(raf);
    if (score.src) score.pause();
    updateControls(currentTime);
  }

  function tick(now) {
    if (!playing) return;
    const delta = (now - lastNow) / 1000;
    lastNow = now;
    currentTime = Math.min(DURATION, currentTime + delta);
    render(currentTime);
    if (score.src && Math.abs(score.currentTime - currentTime) > .08) score.currentTime = currentTime;
    if (currentTime >= DURATION) pause();
    else raf = requestAnimationFrame(tick);
  }

  function play() {
    if (currentTime >= DURATION) seek(0);
    playing = true;
    lastNow = performance.now();
    if (score.src) {
      score.currentTime = currentTime;
      score.play().catch(() => {});
    }
    raf = requestAnimationFrame(tick);
    updateControls(currentTime);
  }

  function toggle() { playing ? pause() : play(); }
  function step(frames) { pause(); seek(currentTime + frames / FPS); }

  if (!capture) {
    scrubber.max = String(DURATION);
    timeInput.max = String(DURATION);
    frameInput.max = String(Math.round(DURATION * FPS));
    playPause.addEventListener("click", toggle);
    $("#stepBack").addEventListener("click", () => step(-1));
    $("#stepForward").addEventListener("click", () => step(1));
    scrubber.addEventListener("input", () => { pause(); seek(scrubber.value); });
    timeInput.addEventListener("change", () => { pause(); seek(timeInput.value); });
    frameInput.addEventListener("change", () => { pause(); seek(Number(frameInput.value) / FPS); });
    window.addEventListener("keydown", (event) => {
      if (event.target.matches("input")) return;
      if (event.code === "Space") { event.preventDefault(); toggle(); }
      if (event.code === "ArrowLeft") step(event.shiftKey ? -FPS : -1);
      if (event.code === "ArrowRight") step(event.shiftKey ? FPS : 1);
    });
    const markerRail = $("#markerRail");
    [0, 6.2, 11.5, 14.0, 19.5, 21.4, 28.4].forEach((time) => {
      const marker = document.createElement("i");
      marker.className = "marker";
      marker.style.left = `${(time / DURATION) * 100}%`;
      marker.title = `${time.toFixed(2)}s / ${Math.round(time * FPS)}f`;
      markerRail.append(marker);
    });
  }

  window.__AE_VIDEO__ = { FPS, DURATION, render, seek, play, pause, step };
  render(0);
})();

