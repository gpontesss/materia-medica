(function () {
  "use strict";

  var script = document.currentScript;
  var base = (script && script.dataset.base) || "";
  var activeSlug = (script && script.dataset.active) || "";

  var topFab = document.getElementById("top-fab");
  if (topFab) {
    topFab.addEventListener("click", function () {
      // No smooth behavior: see the scrollIntoView/scrollTo gotcha in
      // site/CLAUDE.md -- smooth scrolling proved unreliable here.
      window.scrollTo(0, 0);
    });
  }

  var fab = document.getElementById("nav-fab");
  var overlay = document.getElementById("nav-overlay");
  var panel = document.getElementById("nav-panel");
  var closeBtn = document.getElementById("nav-close");
  var listEl = document.getElementById("nav-list");
  var azEl = document.getElementById("nav-az");
  if (!fab || !overlay || !panel || !listEl || !azEl) return;

  var ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
  var built = false;
  var lastScrubLetter = null;
  var letterOffsets = {};

  function firstLetter(title) {
    var stripped = title
      .normalize("NFD")
      .replace(/[̀-ͯ]/g, "")
      .trim();
    var ch = (stripped.charAt(0) || "?").toUpperCase();
    return /[A-Z]/.test(ch) ? ch : "#";
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function build(entries) {
    var groups = {};
    entries.forEach(function (e) {
      var letter = firstLetter(e.title);
      (groups[letter] = groups[letter] || []).push(e);
    });

    var listHtml = [];
    var azHtml = [];
    ALPHABET.forEach(function (letter) {
      var group = groups[letter];
      if (!group || group.length === 0) {
        azHtml.push('<button type="button" class="nav-az-letter" disabled>' + letter + "</button>");
        return;
      }
      azHtml.push(
        '<button type="button" class="nav-az-letter" data-target="nav-letter-' + letter + '">' + letter + "</button>"
      );
      listHtml.push('<li class="nav-letter-group" id="nav-letter-' + letter + '">' + letter + "</li>");
      group.forEach(function (e) {
        var current = e.slug === activeSlug;
        listHtml.push(
          '<li><a href="' + base + e.slug + '.html"' +
            (current ? ' class="current" aria-current="page"' : "") +
            ">" + escapeHtml(e.title) +
            (e.category !== "entry" ? '<span class="nav-item-category">' + escapeHtml(e.category) + "</span>" : "") +
            "</a></li>"
        );
      });
    });

    listEl.innerHTML = listHtml.join("");
    azEl.innerHTML = azHtml.join("");
    built = true;

    // Cache each letter's offset now, while the list is freshly built and
    // unscrolled -- see the comment in jumpTo() for why these can't be
    // measured live later.
    letterOffsets = {};
    ALPHABET.forEach(function (letter) {
      var el = document.getElementById("nav-letter-" + letter);
      if (el) letterOffsets[letter] = el.offsetTop - listEl.offsetTop;
    });

    if (activeSlug) {
      var currentEl = listEl.querySelector("a.current");
      if (currentEl) {
        window.requestAnimationFrame(function () {
          currentEl.scrollIntoView({ block: "center" });
        });
      }
    }
  }

  function loadEntries() {
    return fetch(base + "nav-index.json")
      .then(function (r) { return r.json(); })
      .catch(function () { return []; });
  }

  function jumpTo(letter) {
    // Uses the offsets cached in build(), not live geometry: the letter
    // headers are position:sticky, and in Chrome both getBoundingClientRect
    // *and* offsetTop for a sticky element reflect wherever it's currently
    // pinned/pushed to on screen, not a stable layout position -- so
    // measuring "live" gives a value that depends on the scroll position at
    // the moment of measuring, which is exactly what we're trying to
    // compute and made jumps upward (and jumps after any prior jump) land
    // on the wrong offset or not move at all.
    // Instant, not smooth: smooth scrolling (both target.scrollIntoView and
    // listEl.scrollTo with behavior:"smooth") proved unreliable -- it can
    // silently no-op. An instant jump also matches how the iOS/Android
    // contacts-style A-Z index this is modeled on actually behaves.
    if (letter in letterOffsets) listEl.scrollTop = letterOffsets[letter];
  }

  function openPanel() {
    overlay.hidden = false;
    document.body.classList.add("nav-open");
    fab.setAttribute("aria-expanded", "true");
    if (!built) {
      loadEntries().then(build);
    }
    window.requestAnimationFrame(function () {
      closeBtn.focus();
    });
  }

  function closePanel() {
    overlay.hidden = true;
    document.body.classList.remove("nav-open");
    fab.setAttribute("aria-expanded", "false");
    fab.focus();
  }

  fab.addEventListener("click", openPanel);
  closeBtn.addEventListener("click", closePanel);

  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) closePanel();
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && !overlay.hidden) closePanel();
  });

  azEl.addEventListener("click", function (e) {
    var btn = e.target.closest(".nav-az-letter");
    if (!btn || btn.disabled) return;
    jumpTo(btn.dataset.target.replace("nav-letter-", ""));
  });

  function scrubAt(x, y) {
    var el = document.elementFromPoint(x, y);
    var btn = el && el.closest(".nav-az-letter");
    if (!btn || btn.disabled) return;
    var letter = btn.dataset.target.replace("nav-letter-", "");
    if (letter !== lastScrubLetter) {
      lastScrubLetter = letter;
      jumpTo(letter);
    }
  }

  azEl.addEventListener("pointerdown", function (e) {
    lastScrubLetter = null;
    scrubAt(e.clientX, e.clientY);
    azEl.setPointerCapture(e.pointerId);
  });

  azEl.addEventListener("pointermove", function (e) {
    if (e.buttons !== 1 && e.pointerType !== "touch") return;
    scrubAt(e.clientX, e.clientY);
  });

  azEl.addEventListener("pointerup", function () {
    lastScrubLetter = null;
  });

  // Mobile-only section nav: below the width where the sidebar TOC has room
  // (see the max-width:59.99rem block in style.css), its own floating
  // button opens the same #entry-toc markup as a drawer instead.
  var tocFab = document.getElementById("toc-fab");
  var entryToc = document.getElementById("entry-toc");
  if (tocFab && entryToc) {
    var closeToc = function () {
      entryToc.classList.remove("open");
      tocFab.setAttribute("aria-expanded", "false");
    };
    tocFab.addEventListener("click", function () {
      var willOpen = !entryToc.classList.contains("open");
      entryToc.classList.toggle("open", willOpen);
      tocFab.setAttribute("aria-expanded", String(willOpen));
    });
    entryToc.addEventListener("click", function (e) {
      if (e.target.tagName === "A") closeToc();
    });
    document.addEventListener("click", function (e) {
      if (
        entryToc.classList.contains("open") &&
        !entryToc.contains(e.target) &&
        e.target !== tocFab
      ) {
        closeToc();
      }
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && entryToc.classList.contains("open")) closeToc();
    });
  }
})();
