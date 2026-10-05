/* Manga Lab — interacciones del tema. Sin dependencias. */
(function () {
  "use strict";
  var root = document.documentElement;
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function store(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }

  /* ── Tema día / noche ─────────────────────────────────── */
  document.querySelectorAll('[data-toggle="theme"]').forEach(function (b) {
    b.addEventListener("click", function () {
      var t = root.dataset.theme === "dark" ? "light" : "dark";
      root.dataset.theme = t;
      store("ml-theme", t);
    });
  });

  /* ── Pausar / reanudar animaciones (también SMIL) ─────── */
  function applyMotion() {
    var off = root.dataset.motion === "off" || reduce;
    document.querySelectorAll("svg.scene").forEach(function (s) {
      if (!s.pauseAnimations) return;
      off ? s.pauseAnimations() : s.unpauseAnimations();
    });
  }
  document.querySelectorAll('[data-toggle="motion"]').forEach(function (b) {
    b.addEventListener("click", function () {
      if (root.dataset.motion === "off") { delete root.dataset.motion; store("ml-motion", "on"); }
      else { root.dataset.motion = "off"; store("ml-motion", "off"); }
      applyMotion();
    });
  });
  applyMotion();

  /* ── Menú móvil ───────────────────────────────────────── */
  var burger = document.querySelector(".burger"), nav = document.getElementById("nav");
  if (burger && nav) burger.addEventListener("click", function () {
    var open = nav.classList.toggle("is-open");
    burger.setAttribute("aria-expanded", open ? "true" : "false");
  });

  /* ── Viñetas que aparecen al hacer scroll ─────────────── */
  var pops = document.querySelectorAll(".pop");
  if ("IntersectionObserver" in window && !reduce) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("is-in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.15, rootMargin: "0px 0px -40px 0px" });
    pops.forEach(function (p) { io.observe(p); });
  } else {
    pops.forEach(function (p) { p.classList.add("is-in"); });
  }

  /* ── El doctor recorre la línea temporal ──────────────── */
  var tl = document.querySelector("[data-timeline]");
  var walker = tl && tl.querySelector(".timeline__walker");
  /* ── Barra de lectura ─────────────────────────────────── */
  var bar = document.querySelector("[data-progress]");
  var ticking = false;
  function onScroll() {
    if (ticking) return; ticking = true;
    requestAnimationFrame(function () {
      ticking = false;
      if (walker) {
        var r = tl.getBoundingClientRect(), vh = window.innerHeight;
        var p = Math.min(1, Math.max(0, (vh * 0.55 - r.top) / r.height));
        walker.style.top = (p * (r.height - walker.offsetHeight)) + "px";
      }
      if (bar) {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? (window.scrollY / h) * 100 : 0) + "%";
      }
    });
  }
  if (walker || bar) { window.addEventListener("scroll", onScroll, { passive: true }); onScroll(); }

  /* ── Héroe: mundo por capas, personajes y bocadillos ─── */
  var stage = document.querySelector("[data-stage]");
  if (!stage) return;
  var world = stage.querySelector("[data-world]");
  var bubble = stage.querySelector("[data-bubble]");
  var bubbleText = stage.querySelector("[data-bubble-text]");
  var sfx = stage.querySelector("[data-sfx]");
  var burst = stage.querySelector("[data-burst]");
  var lang = (root.lang || "es").slice(0, 2);
  var quotes = {};
  try { quotes = JSON.parse(document.getElementById("quotes").textContent); } catch (e) {}
  var SFX = { doctor: "ドン!", partner: "ふふっ", kidA: "ワーイ!", kidB: "キャー!", dog: "ワン!" };
  var WHO = { dad: "doctor", mom: "partner", kidA: "kidA", kidB: "kidB", dog: "dog" };

  // Encuadre: el mundo (16:9) cubre el escenario; en pantallas estrechas se centra en la familia.
  function frame() {
    var W = stage.clientWidth, H = stage.clientHeight;
    var ww = Math.max(W, H * 16 / 9), wh = ww * 9 / 16;
    var narrow = W < 861;
    var fx = narrow ? 0.71 : (W / H > 1.9 ? 0.5 : 0.56);   // punto que queremos centrado
    var left = Math.min(0, Math.max(W - ww, W / 2 - fx * ww));
    var top = Math.min(0, Math.max(H - wh, (H - wh) * 0.9));
    world.classList.add("is-framed");
    world.style.width = ww + "px";
    world.style.left = left + "px";
    world.style.top = top + "px";
    place(current, bubbleText.textContent);
  }

  // Parallax con el puntero y con el scroll
  var mx = 0, my = 0, tx = 0, ty = 0, raf = 0;
  function loop() {
    raf = 0;
    mx += (tx - mx) * 0.08; my += (ty - my) * 0.08;
    var r = stage.getBoundingClientRect();
    var sy = Math.max(0, Math.min(1, -r.top / r.height));
    world.style.setProperty("--mx", mx.toFixed(3));
    world.style.setProperty("--my", my.toFixed(3));
    world.style.setProperty("--sy", sy.toFixed(3));
    if (Math.abs(tx - mx) > 0.002 || Math.abs(ty - my) > 0.002) raf = requestAnimationFrame(loop);
  }
  function kick() { if (!raf) raf = requestAnimationFrame(loop); }
  if (!reduce) {
    stage.addEventListener("pointermove", function (e) {
      if (root.dataset.motion === "off") return;
      var r = stage.getBoundingClientRect();
      tx = ((e.clientX - r.left) / r.width) * 2 - 1;
      ty = ((e.clientY - r.top) / r.height) * 2 - 1;
      kick();
    });
    stage.addEventListener("pointerleave", function () { tx = ty = 0; kick(); });
    window.addEventListener("scroll", kick, { passive: true });
  }

  // Bocadillo
  var current = "dad", typing;
  function say(text) {
    clearInterval(typing);
    if (reduce || root.dataset.motion === "off") { bubbleText.textContent = text; return; }
    var i = 0; bubbleText.textContent = "";
    typing = setInterval(function () {
      bubbleText.textContent = text.slice(0, ++i);
      if (i >= text.length) clearInterval(typing);
    }, 26);
  }
  function charEl(who) { return world.querySelector('.char[data-who="' + who + '"]'); }
  function place(who, text) {
    var c = charEl(who); if (!c) return;
    if (text != null) bubbleText.textContent = text;          // medimos con el texto completo
    bubble.style.marginLeft = "0px"; bubble.style.marginTop = "0px";
    bubble.style.setProperty("--tail", "0px");
    bubble.style.left = parseFloat(c.dataset.hx) + "%";
    bubble.style.top = (parseFloat(c.dataset.hy) - 1.5) + "%";
    var s = stage.getBoundingClientRect(), b = bubble.getBoundingClientRect();
    var dx = 0, dy = 0;
    if (b.left < s.left + 8) dx = s.left + 8 - b.left;
    if (b.right > s.right - 8) dx = s.right - 8 - b.right;
    if (b.top < s.top + 6) dy = s.top + 6 - b.top;
    bubble.style.marginLeft = dx + "px";
    bubble.style.marginTop = dy + "px";
    bubble.style.setProperty("--tail", (-dx) + "px");
    bubble.classList.toggle("is-low", dy > b.height * 0.5);
  }
  var last = {};
  function speak(who) {
    var key = WHO[who] || who;
    var list = (quotes[key] && (quotes[key][lang] || quotes[key].es)) || [];
    if (!list.length) return;
    var i; do { i = Math.floor(Math.random() * list.length); } while (list.length > 1 && i === last[key]);
    last[key] = i; current = who;
    place(who, list[i]);
    bubble.classList.remove("is-pop"); void bubble.offsetWidth; bubble.classList.add("is-pop");
    say(list[i]);
    var c = charEl(who);
    var cx = parseFloat(c.style.left) + parseFloat(c.style.width) / 2;
    var cy = parseFloat(c.style.top) + parseFloat(c.style.height) * 0.4;
    if (sfx) {
      sfx.textContent = SFX[key] || "!";
      sfx.style.left = (parseFloat(c.dataset.hx) + 6) + "%"; sfx.style.top = (parseFloat(c.dataset.hy) + 10) + "%";
      sfx.classList.remove("is-on"); void sfx.offsetWidth; sfx.classList.add("is-on");
    }
    if (burst && !reduce) {
      burst.style.left = cx + "%"; burst.style.top = cy + "%";
      burst.classList.remove("is-on"); void burst.offsetWidth; burst.classList.add("is-on");
    }
  }
  world.querySelectorAll(".char").forEach(function (c) {
    var hit = c.querySelector(".char__hit");
    hit.addEventListener("click", function () {
      c.classList.remove("is-jump"); void c.offsetWidth; c.classList.add("is-jump");
      speak(c.dataset.who);
    });
    c.addEventListener("animationend", function (e) { if (e.animationName === "jump") c.classList.remove("is-jump"); });
  });

  frame();
  window.addEventListener("resize", frame);
  var first = bubbleText.textContent;
  setTimeout(function () { place("dad", first); say(first); }, reduce ? 0 : 1100);
})();
