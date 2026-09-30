(function () {
  "use strict";

  var script = document.currentScript;
  var base = (script && script.dataset.base) || "";
  var input = document.getElementById("search-input");
  var resultsBox = document.getElementById("search-results");
  if (!input || !resultsBox) return;

  var index = null;
  var indexPromise = null;
  var activeIndex = -1;
  var currentItems = [];

  function loadIndex() {
    if (!indexPromise) {
      indexPromise = fetch(base + "search-index.json")
        .then(function (r) { return r.json(); })
        .then(function (data) { index = data; return data; })
        .catch(function () { index = []; return []; });
    }
    return indexPromise;
  }

  input.addEventListener("focus", loadIndex);

  function escapeHtml(s) {
    return s.replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function highlight(text, query) {
    if (!query) return escapeHtml(text);
    var idx = text.toLowerCase().indexOf(query.toLowerCase());
    if (idx === -1) return escapeHtml(text);
    return (
      escapeHtml(text.slice(0, idx)) +
      "<mark>" + escapeHtml(text.slice(idx, idx + query.length)) + "</mark>" +
      escapeHtml(text.slice(idx + query.length))
    );
  }

  function snippetAround(text, query, radius) {
    radius = radius || 80;
    var lower = text.toLowerCase();
    var idx = lower.indexOf(query.toLowerCase());
    if (idx === -1) return text.slice(0, radius * 2);
    var start = Math.max(0, idx - radius);
    var end = Math.min(text.length, idx + query.length + radius);
    var snippet = text.slice(start, end);
    if (start > 0) snippet = "…" + snippet;
    if (end < text.length) snippet = snippet + "…";
    return snippet;
  }

  function search(query) {
    var q = query.trim().toLowerCase();
    if (!q || !index) return [];
    var scored = [];
    for (var i = 0; i < index.length; i++) {
      var entry = index[i];
      var titleLower = entry.title.toLowerCase();
      var score = -1;
      if (titleLower === q) score = 100;
      else if (titleLower.indexOf(q) === 0) score = 80;
      else if (titleLower.indexOf(q) !== -1) score = 60;
      else if (entry.text.toLowerCase().indexOf(q) !== -1) score = 20;
      if (score > 0) scored.push({ entry: entry, score: score });
    }
    scored.sort(function (a, b) {
      return b.score - a.score || a.entry.title.localeCompare(b.entry.title);
    });
    return scored.slice(0, 20).map(function (s) { return s.entry; });
  }

  function render(items, query) {
    currentItems = items;
    activeIndex = -1;
    if (items.length === 0) {
      resultsBox.innerHTML = '<p class="search-empty">No matches.</p>';
      resultsBox.hidden = query.trim().length === 0;
      return;
    }
    resultsBox.innerHTML = items
      .map(function (entry) {
        var titleLower = entry.title.toLowerCase();
        var inTitle = titleLower.indexOf(query.toLowerCase()) !== -1;
        var snippetSource = inTitle ? entry.excerpt : snippetAround(entry.text, query);
        return (
          '<a href="' + base + entry.slug + '.html">' +
          '<span class="result-title">' + highlight(entry.title, inTitle ? query : "") + "</span>" +
          '<span class="result-category">' + escapeHtml(entry.category) + "</span>" +
          '<div class="result-snippet">' + highlight(snippetSource, query) + "</div>" +
          "</a>"
        );
      })
      .join("");
    resultsBox.hidden = false;
  }

  function updateActive() {
    var links = resultsBox.querySelectorAll("a");
    for (var i = 0; i < links.length; i++) {
      links[i].classList.toggle("active", i === activeIndex);
    }
    if (activeIndex >= 0 && links[activeIndex]) {
      links[activeIndex].scrollIntoView({ block: "nearest" });
    }
  }

  input.addEventListener("input", function () {
    var query = input.value;
    if (!query.trim()) {
      resultsBox.hidden = true;
      resultsBox.innerHTML = "";
      return;
    }
    loadIndex().then(function () { render(search(query), query); });
  });

  input.addEventListener("keydown", function (e) {
    if (resultsBox.hidden || currentItems.length === 0) return;
    if (e.key === "ArrowDown") {
      e.preventDefault();
      activeIndex = Math.min(activeIndex + 1, currentItems.length - 1);
      updateActive();
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      activeIndex = Math.max(activeIndex - 1, 0);
      updateActive();
    } else if (e.key === "Enter") {
      if (activeIndex >= 0 && currentItems[activeIndex]) {
        window.location.href = base + currentItems[activeIndex].slug + ".html";
      }
    } else if (e.key === "Escape") {
      resultsBox.hidden = true;
      input.blur();
    }
  });

  document.addEventListener("click", function (e) {
    if (!resultsBox.contains(e.target) && e.target !== input) {
      resultsBox.hidden = true;
    }
  });
})();
