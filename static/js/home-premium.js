/* ============================================================
   XL Academy — Home Premium interactions
   Vanilla JS: scroll reveal, parallax, sticky progress,
   navbar state, mobile menu, counters, smooth scroll.
   No external dependencies (jQuery/axios are loaded only
   for the existing contact form logic in the template).
   ============================================================ */
(function () {
  "use strict";

  const root = document.querySelector("body.xl");
  if (!root) return;

  const prefersReduced = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  /* ---------- navbar scroll state + back-to-top ---------- */
  const nav = document.getElementById("xl-nav");
  const toTop = document.getElementById("xl-totop");

  function onScroll() {
    const y = window.scrollY || window.pageYOffset;
    if (nav) nav.classList.toggle("scrolled", y > 24);
    if (toTop) toTop.classList.toggle("show", y > 600);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- mobile menu ---------- */
  const burger = document.getElementById("xl-burger");
  if (burger && nav) {
    burger.addEventListener("click", function () {
      nav.classList.toggle("open");
    });
    nav.querySelectorAll(".mobile-panel a").forEach(function (a) {
      a.addEventListener("click", function () {
        nav.classList.remove("open");
      });
    });
  }

  /* ---------- smooth scroll for in-page anchors ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      const id = link.getAttribute("href");
      if (id === "#" || id.length < 2) return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const top = target.getBoundingClientRect().top + window.scrollY - 90;
      window.scrollTo({ top: top, behavior: prefersReduced ? "auto" : "smooth" });
    });
  });

  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: prefersReduced ? "auto" : "smooth" });
    });
  }

  /* ---------- scroll reveal ---------- */
  // On the homepage, animations replay every time they scroll into view.
  const replayReveal = window.location.pathname === "/";
  const revealEls = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && !prefersReduced) {
    const io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("in");
            if (!replayReveal) io.unobserve(entry.target);
          } else if (replayReveal) {
            entry.target.classList.remove("in");
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -60px 0px" }
    );
    revealEls.forEach(function (el) {
      io.observe(el);
    });
  } else {
    revealEls.forEach(function (el) {
      el.classList.add("in");
    });
  }

  /* ---------- hero parallax (orbs + content) ---------- */
  const hero = document.querySelector(".hero");
  const heroInner = document.querySelector(".hero-inner");
  const orbs = document.querySelectorAll(".hero .orb");
  let ticking = false;

  function parallax() {
    const y = window.scrollY || window.pageYOffset;
    if (!hero) return;
    const h = hero.offsetHeight || 1;
    const p = Math.min(y / h, 1);
    orbs.forEach(function (orb, i) {
      const depth = 60 + i * 40;
      orb.style.transform = "translateY(" + p * depth + "px)";
    });
    if (heroInner) {
      heroInner.style.transform = "translateY(" + p * 60 + "px)";
      heroInner.style.opacity = String(1 - p * 0.9);
    }
    ticking = false;
  }
  if (!prefersReduced && hero) {
    window.addEventListener(
      "scroll",
      function () {
        if (!ticking) {
          window.requestAnimationFrame(parallax);
          ticking = true;
        }
      },
      { passive: true }
    );
    parallax();
  }

  /* ---------- workflow sticky progress bar ---------- */
  const flow = document.getElementById("xl-flow");
  const flowBar = document.getElementById("xl-flow-bar");
  if (flow && flowBar) {
    function flowProgress() {
      const rect = flow.getBoundingClientRect();
      const vh = window.innerHeight;
      const total = rect.height - vh * 0.5;
      const scrolled = Math.min(Math.max(vh * 0.5 - rect.top, 0), total);
      const ratio = total > 0 ? scrolled / total : 0;
      flowBar.style.transform = "scaleX(" + Math.min(Math.max(ratio, 0), 1) + ")";
    }
    window.addEventListener("scroll", flowProgress, { passive: true });
    flowProgress();
  }

  /* ---------- animated counters ---------- */
  function animateCounter(el) {
    const target = parseFloat(el.getAttribute("data-count")) || 0;
    const duration = 2200;
    let start = null;
    function step(ts) {
      if (!start) start = ts;
      const progress = Math.min((ts - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(eased * target).toLocaleString();
      if (progress < 1) {
        window.requestAnimationFrame(step);
      } else {
        el.textContent = target.toLocaleString();
      }
    }
    window.requestAnimationFrame(step);
  }

  /* ---------- generic category filter (school list) ---------- */
  document.querySelectorAll(".filter-bar").forEach(function (bar) {
    const items = document.querySelectorAll(".card-grid .grid-item");
    bar.querySelectorAll("[data-filter]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        bar
          .querySelectorAll("[data-filter]")
          .forEach(function (b) {
            b.classList.remove("current_menu_item", "active");
          });
        btn.classList.add("active");
        const f = (btn.getAttribute("data-filter") || "*").replace(/^\./, "");
        items.forEach(function (it) {
          const show = f === "*" || it.classList.contains(f);
          it.classList.toggle("is-hidden", !show);
        });
      });
    });
  });

  const counters = document.querySelectorAll("[data-count]");
  if ("IntersectionObserver" in window) {
    const co = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting && !entry.target.dataset.counted) {
            entry.target.dataset.counted = "1";
            if (prefersReduced) {
              entry.target.textContent = (
                parseFloat(entry.target.getAttribute("data-count")) || 0
              ).toLocaleString();
            } else {
              animateCounter(entry.target);
            }
            if (!replayReveal) co.unobserve(entry.target);
          } else if (!entry.isIntersecting && replayReveal) {
            // reset so it re-counts next time it scrolls into view
            entry.target.dataset.counted = "";
            entry.target.textContent = "0";
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach(function (el) {
      co.observe(el);
    });
  } else {
    counters.forEach(function (el) {
      el.textContent = (
        parseFloat(el.getAttribute("data-count")) || 0
      ).toLocaleString();
    });
  }
})();
