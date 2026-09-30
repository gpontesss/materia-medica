# CLAUDE.md — Materia Medica Website

This file defines how the `site/` generator works and how the generated pages must look and behave. Read this before touching anything under `site/` — templates, CSS, JS, or the build script.

## What this is, and the one rule that governs everything else

`site/` is a **generator**, not a website. It compiles `materia-medica/*.typ` to HTML with Typst's own HTML backend and wraps the result in a page template. **The generated HTML is never hand-written and never committed.** `out/site/` is gitignored and rebuilt from the Typst sources every time — locally via `make site`, and in CI via `.github/workflows/pages.yml` on every push that touches `materia-medica/**`, `fonts/**`, or `site/**`.

Consequence: to change anything about how an entry looks or behaves on the web — layout, typography, search, navigation — edit `site/build.py` and/or `site/assets/*`, then rebuild. Never patch `out/site/*.html` directly; it will be silently discarded on the next build.

## Files

```
site/
  build.py            # the generator: Typst → HTML → templated pages + search/nav indexes
  CLAUDE.md            # this file
  assets/
    style.css         # all page styling
    search.js         # full-text search widget (header, every page)
    nav.js            # A-Z entry switcher + per-entry section drawer (every page)
```

Build output (`out/site/`, gitignored): one `<slug>.html` per `materia-medica/*.typ` file, `index.html`, `search-index.json`, `nav-index.json`, copies of the three asset files, and `fonts/*.ttf`.

## Build pipeline (`site/build.py`)

For each `materia-medica/*.typ` file, in order:

1. `typst compile --features html --format html --font-path ./fonts <file> <tmp>.html` — Typst's HTML backend is experimental but produces clean semantic HTML (`<h2>`/`<h3>`/`<h4>` for `=`/`==`/`===`, `<em>`/`<strong>`, footnotes as `<a role="doc-noteref">` + an endnotes `<section>`). Entry files compile standalone — no cross-file `#include`/`#ref`/image dependencies — so this never needs to go through the PDF's `materia-medica.typ` root document.
2. Extract the `<body>…</body>` fragment (`BODY_RE`).
3. **Demote every heading by one level** (`demote_headings`): Typst's top-level `=` heading compiles to `<h2>`, because the HTML backend's own document title/heading conventions assume it isn't the page's only heading. Since each entry page *is* single-subject, shifting `h2→h1, h3→h2, h4→h3` makes the entry title the page's one true `<h1>`. The corpus never uses more than `===` (three levels), so this never needs to go past `h3`.
4. **Inject heading `id`s and build a table of contents** (`add_heading_ids_and_toc`): every heading gets a slugified, de-duplicated `id` (for deep links); the TOC is built from the **top two heading levels actually present** in that entry (usually h1+h2), not a fixed level — so a short reference entry's TOC doesn't over-nest.
5. Title = the text of the first heading (plain-text, tags stripped), category = `category_for(slug)`: `zz-glossary` → `"glossary"`, `{climates, tibb-al-arabi}` → `"reference"`, everything else → `"entry"`. This mirrors `materia-medica/CLAUDE.md`'s own distinction between substance entries and foundational-reference entries — if a new foundational-reference entry is added there, add its slug to `REFERENCE_SLUGS` here too.
6. Excerpt = first `<p>` text, truncated (used only in the index cards' hover text is gone now — currently used in search-result snippets when the query matches the title rather than the body).

Then `build()` writes: one page per entry (`render_entry_page`), `index.html` (`render_index_page`), `search-index.json` (full plain text per entry — this is what powers full-text search), and `nav-index.json` (slug/title/category only, deliberately small so the A-Z switcher opens instantly without waiting on the full-text payload).

**A broken entry fails the whole build, loudly, by design.** If a `.typ` file has a Typst syntax error, `run_typst_html` raises and the build stops — this is the same failure that `make materia-medica` (the PDF) would hit, so it's never something to work around in the generator; fix the source `.typ` file.

## Typography

Deliberately **takes its family and relative proportions from the Typst PDF** (`materia-medica.typ`), but not its absolute sizes or page width:

- Font stack: `EB Garamond` (Google Fonts, loaded in `render_shell`) with `Noto Serif Devanagari` (self-hosted from `fonts/`, via `@font-face`) as fallback for Sanskrit, matching the PDF's `#set text(font: (...))`.
- Headings inside `.entry` are sized at Typst's own default ratios — `h1: 1.4em`, `h2: 1.2em`, `h3: 1.1em`, all bold — so they stay proportional if the base size ever changes.
- Base body size is **15pt**, chosen (not copied from the PDF's 11pt) to keep words-per-line comfortable at the responsive measure below — bump it if the measure changes significantly, since the two were tuned together. A proportionally-scaled 14pt kicks in under 30rem viewport width.
- Paragraphs are justified with `hyphens: auto`, matching the PDF's `#set par(justify: true)`.
- **Text measure is intentionally *not* the PDF's fixed 5in page width.** `--max-measure: min(38rem, 92vw)` — a comfortable, device-appropriate reading line length that adapts to viewport, capped so it never gets uncomfortably wide on large screens or overflows on small ones.
- Color: **plain black-on-white, no accent color anywhere** — including search-match highlighting, which is bold+underline rather than a colored `<mark>`. Dark mode is a true monochrome inversion (`prefers-color-scheme: dark` flips `--bg`/`--text`/`--border` etc.), not a separate palette.

## Layout

### Index page (`render_index_page`)
A plain, dense, multi-column list of entry titles grouped under three headers (Foundational references / Substance entries / Glossary, in that order, alphabetized within each) — modeled on the PDF's own two-column `#columns(2, outline(depth: 1))` front page, not a card grid. No excerpts here (excerpts exist only in `search-index.json`, for search-result snippets).

### Entry page (`render_entry_page`)
The article (`.entry`) is the **only** thing that determines text width: `max-width: var(--max-measure); margin: 0 auto;`, unconditionally, regardless of viewport or whether a TOC is present. This is deliberate — an earlier version shared a CSS grid track between the TOC and the article, which visibly squeezed/deformed the article at medium viewport widths. Do not reintroduce a layout where the TOC and the article compete for the same track.

The sidebar TOC (`#entry-toc`, ≥60rem viewport) is a **true floating side nav**, not a layout participant:
```css
.entry-toc { display: none; }
@media (min-width: 60rem) {
  .entry-toc {
    display: block;
    position: fixed;
    left: calc(50% - (var(--max-measure) / 2) - 15rem);
    width: 13rem;
    ...
  }
}
```
`left` is computed from the viewport center and `--max-measure`, not from the sidebar/article's shared container — this works because both `.entry` (centered via `margin:auto` in `.site-main`, itself centered via `margin:auto` in `body`) and the `position:fixed` TOC resolve to the same true viewport center, so the TOC hugs the article's left edge with a constant 2rem gap at *any* viewport width ≥60rem, without ever touching the article's own box model. If you change `--max-measure`, this still holds — don't hardcode a measure value into the TOC's `left` calc separately from `--max-measure` itself.

Below 60rem, the sidebar disappears and the TOC becomes a drawer opened by its own floating button (`#toc-fab`) — see **Floating navigation** below.

**Anchor targets must clear the sticky header.** `.site-header` is `position: sticky; top: 0` and up to ~108px tall (it wraps to two rows below ~35rem-ish viewports, when the search box no longer fits beside the site title). Without help, jumping to any in-page anchor — a TOC link, a footnote ref/backlink, a heading's own id — lands the target right underneath it, which looks exactly like navigation silently failed. Fixed globally: `[id] { scroll-margin-top: 7.5rem; }` (in `style.css`, right after `.site-header`) — applies to every anchor target (headings *and* footnote list items), not just a hand-picked selector list, so a new kind of anchorable content doesn't quietly reintroduce the bug. If the header's max height ever grows (more header content, larger fonts), bump 7.5rem to match.

## Floating navigation (`nav.js` + the FAB stack)

Up to three circular floating buttons, bottom-right, in `.fab-stack` — a `flex-direction: column-reverse` container so they always stack cleanly with a consistent gap regardless of which ones exist on a given page/viewport, with **no per-button `bottom: calc()` math to keep in sync**. DOM order (first = bottom of stack, nearest the screen corner): `#nav-fab`, then `{toc_fab_html}` (only present on entry pages with a multi-item TOC), then `#top-fab`. `column-reverse` puts the first child at the bottom and stacks later children upward, so visually: **A–Z at the very corner, section TOC above it (when present), back-to-top at the top.** All three share the `.fab-circle` base class for their visual treatment (border, circle, hover-invert) — a button-specific class (`.nav-fab`, `.toc-fab`, `.top-fab`) only adds what's different about it.

- **`#nav-fab`** ("A–Z" text) — on **every** page, always visible. Opens `#nav-overlay`: a modal (bottom sheet under 40rem, centered dialog above it) listing every entry grouped by first letter, with an A-Z jump strip on the panel's edge (click, or drag/scrub via pointer events) and the current page marked `→ **Title**`. Content is fetched lazily from `nav-index.json` on first open only (`built` flag prevents re-fetching).
- **`#toc-fab`** (list-icon SVG, no text) — only on entry pages with more than one TOC item, and only **below 60rem** (exactly where the sidebar TOC is hidden — the two are mutually exclusive by design, never both visible). Toggles the *same* `#entry-toc` element into an `.open` bottom-drawer via a class, rather than duplicating the TOC markup. Rendered by `render_entry_page` but passed into `render_shell`'s `toc_fab_html` parameter, so it lives in the same `.fab-stack` as the other two rather than being positioned separately.
- **`#top-fab`** (up-arrow SVG, no text) — on **every** page, always visible, always the topmost button in the stack. `window.scrollTo(0, 0)` — instant, not smooth (see gotcha 2).

### Hard-won gotchas — read before touching this code

These were real, reproduced bugs, not theoretical:

1. **`[hidden]` vs. a class rule that sets `display`.** The browser's built-in `[hidden] { display: none }` rule and an author rule like `.nav-overlay { display: flex; ... }` have *equal* CSS specificity (one attribute selector, one class selector), so the later-loaded author stylesheet wins by source order and the element shows despite `hidden`. Always guard: `.nav-overlay:not([hidden]) { display: flex; }`. The same trap applies to `.entry-toc.open` (see gotcha 4).
2. **`scrollIntoView`/`Element.scrollTo` with `behavior: "smooth"` can silently no-op.** Reproduced repeatedly in this codebase's testing (Chrome). Don't rely on smooth scrolling for anything that must actually happen — every programmatic scroll in `nav.js` (A-Z jump, back-to-top) uses instant scrolling only. (This also happens to match how a real iOS/Android A-Z contacts index behaves — an instant jump, not an animated one.)
3. **`position: sticky` elements' `getBoundingClientRect()` *and* `offsetTop` are not stable measurement targets.** Both reflect wherever the sticky element is *currently, visually* pinned or pushed to — which depends on scroll position — not a fixed layout position. Measuring a sticky element's position live, after the user has already scrolled, gives you a value that depends on the very thing you're trying to compute, and jumps to some letters silently landed on the wrong offset (or the same offset as a different letter) as a result. The fix: cache every letter's offset **once**, immediately after the list is built and while `scrollTop` is still 0 (`letterOffsets` in `nav.js`), and always look up the cache — never re-measure a sticky element's position after the initial build.
4. **Drawer/open-state CSS must stay nested inside the same width media query as its trigger button.** `.entry-toc.open` (two classes) has higher specificity than the wide-viewport sidebar rule `.entry-toc` (one class) from the section above. If `.entry-toc.open`'s drawer styles were ever written as a bare top-level rule, it could in principle beat the sidebar rule at a wide viewport should `.open` ever be true there. Keeping both the `.toc-fab` button *and* `.entry-toc.open` inside the same `@media (max-width: 59.99rem)` block makes that structurally impossible rather than relying on it just not happening to occur. The `.entry-toc.open` drawer's `bottom` offset must clear the *tallest possible* `.fab-stack` (all three buttons) — recompute it if a fourth FAB is ever added.

## Search (`search.js`)

Fetched lazily from `search-index.json` on first focus of `#search-input` (not on page load — the full-text payload is the largest asset on the site). Scoring is simple and deliberate, no library: exact title match > title starts-with > title contains > body-text contains. Results show a highlighted snippet — from the entry's excerpt if the match was in the title, otherwise from the surrounding body text. No color in the highlight (bold + underline), consistent with the rest of the site's black-and-white design.

## CI (`.github/workflows/pages.yml`)

Installs the **same Typst version used locally** (currently 0.14.2, via `typst-community/setup-typst`) — bump both together when upgrading Typst, since the HTML backend is explicitly marked experimental and its output shape could change between versions. Runs `site/build.py`, deploys via `actions/upload-pages-artifact` + `actions/deploy-pages`. GitHub Pages must have its source set to "GitHub Actions" in the repo's Settings → Pages — a one-time manual step, not something the workflow can do for itself.
