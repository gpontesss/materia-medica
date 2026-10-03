# Project Log

A running record of decisions, rationale, and changes made to this repository.

*This repository was split out of a larger private `writings` repository on 2026-09-30 (see the last entry below); the entries before that were made while this content still lived there, carried over verbatim since they document this project's own history, not the old repo's.*

---

## 2026-05-28 — Sanskrit font for materia-medica

**Problem:** Materia-medica entries include Sanskrit terms in Devanagari script (e.g., `गोधूम`). EB Garamond does not cover the Devanagari block, so those characters rendered as tofu.

**Decision:** Use **Noto Serif Devanagari** (Regular + Bold) as a fallback font alongside EB Garamond.

**Reasoning:**
- It is the only major Devanagari font with an explicitly serif design, matching EB Garamond's classical humanist character.
- Full Unicode Devanagari coverage including Vedic extensions and all Sanskrit conjuncts.
- SIL Open Font License v1.1 — freely redistributable, so it can be committed to the repo.
- Alternatives considered: Shobhika (scholarly but less visually harmonious), Murty Sanskrit (restrictive license), Sanskrit 2003 (unmaintained), Siddhanta (NC license).

**Changes:**
- Added `fonts/NotoSerifDevanagari-Regular.ttf` and `fonts/NotoSerifDevanagari-Bold.ttf` (sourced from `notofonts/noto-fonts` on GitHub).
- Updated `materia-medica.typ`: `font: ("EB Garamond", "Noto Serif Devanagari")` — Typst falls back to the second font for any codepoints the first cannot render.
- Updated `Makefile`: added `FONT_PATH := ./fonts` variable and `--font-path $(FONT_PATH)` to all `typst compile` calls so the bundled fonts are found at build time.

---

## 2026-06-07 — Add barley and oats entries

Added two new materia medica entries: `materia-medica/barley.typ` and `materia-medica/oats.typ`. Both follow the standard template established by wheat/licorice-root/milk.

**Barley (yava / 大麥 / 麥芽 / _Hordeum vulgare_):** a fully classical entry — yava is one of the most prominent Caraka grains (Sūtrasthāna 27.13–17), and 麥芽 (malted barley) is a major Chinese drug. Built around the classical wheat ↔ barley opposition (godhūma's _guru-snigdha-madhura-vipāka_ vs. yava's _laghu-rūkṣa-kaṭu-vipāka_), Caraka's _saktu-vidhi_ as the worked example of saṃskāra-class viruddha, and the modern β-glucan / hordein-celiac story.

**Oats (_Avena sativa_):** explicitly marked _reasoned-only_ for Ayurveda (no classical entry — oats are not in the saṃhitās or nighaṇṭus, and the modern Hindi _jaī_ is not a classical Sanskrit term) and _minor-classical-with-modern-extension_ for Chinese medicine (Bencao Gangmu's 雀麥 likely refers to wild oat / _Bromus_; cultivated 燕麥 is essentially modern in Chinese cuisine — flagged as a non-trivial conflation). The Greco-Roman section uses Pliny's note that oats were the staple food of the Germans (_Nat. Hist._ 18.149), Johnson's "horse vs. men" dictionary entry, and the colloidal-oatmeal → FDA 21 CFR 347 skin-protectant monograph line for modern survivals.

Both apply the prabhāva rule strictly: barley gets "no distinct prabhāva assigned; medohara reading is interpretive"; oats get "no prabhāva can be assigned with classical authority" because oats are not a classical dravya. Both apply the viruddha source-tier tagging and a conditional-dosage line for the modern section.

Reaffirmed conventions during these entries (already in `materia-medica/CLAUDE.md`): the "Ayurvedic status: reasoned-only / classical" header flag at the top of non-canonical entries; preserving the wheat ↔ barley contrastive reading where it sharpens both entries; flagging the 雀麥 / 燕麥 / _Avena fatua_ / _Avena sativa_ identification problem explicitly rather than smoothing it.

---

## 2026-06-09 — Add "Climate, Constitution & Regional Diet" template section

Added a new permanent template section to `materia-medica/CLAUDE.md` (now item 5 in the standard entry order, between "Classical Formulas & Preparations" and "Modern Nutrition & Pharmacology"), and worked the first two instances of it into the new barley and oats entries.

**Why a new section.** The classical formulas section catalogues *what* preparations existed; it does not say *why* a given climate selected for a given preparation. The new section makes the climate ↔ constitution ↔ preparation triangle explicit, using the canonical classical framework: Caraka Sūtrasthāna 6 and Aṣṭāṅga Hṛdaya Sūtrasthāna 3 (_ṛtucaryā_, seasonal regimen) for the Ayurvedic side; _Su Wen_ chs. 2 (_si qi tiao shen da lun_) and 67–74 (_wu yun liu qi_, the doctrine of climatic-pathogenic correspondences and the 六淫 six external excesses 風寒暑濕燥火) for the 中醫 side.

**Structure.** Organize by climate zone, not by region — same climate type can span continents (warm-dry Mediterranean ↔ Levantine ↔ North African; cool-damp Atlantic ↔ Baltic ↔ Pacific Northwest); zoning by climate makes the constitutional logic transparent and avoids ethnographic clutter. For each zone: climate type → doṣa/六淫 reading → traditional preparation → *cares* (climate-appropriate vs. climate-mismatched preparations). Close with a "Modern transposition" paragraph naming the globalized-eating mismatch as _deśa-viruddha_ (place-incompatible food, Caraka Sū. 26) — and use _kāla-viruddha_ for the parallel seasonal-shift category where relevant (e.g. Russian oat-kvass as a *summer*, not winter, form).

**Concrete content highlights.** Barley reads the Tibetan tsampa + po cha + salt triad as a constitutionally complete plateau-Vāta correction (citing _rGyud bzhi_, with the standard verification flag for Tibetan source citations); reads the Scottish broth/bannock/beer/whisky pattern as cool-damp Vāta-Kapha correction with fermentation as a _saṃskāra_ inversion (cooling-laghu → warming-vīrya). Oats are framed throughout as an essentially single-climate grain (Pliny's German-staple note as climate observation, not just sneer), with the Scottish salt-not-sugar rule read as Kidney-yang support against external 寒, and the modern cold-overnight-oat preparation explicitly named as the textbook _deśa-viruddha_ for oats (warm-climate Pitta-pacifying preparation transposed back into the cool-damp climate of origin).

The new section heading and its "Modern transposition" subsection convention are now durable — should be applied to milk, wheat, licorice-root and all future entries as those are next revised.

---

## 2026-06-09 — Add `climates.typ` as foundational reference entry

Created `materia-medica/climates.typ` as a *foundational reference* entry — not a substance entry, but a free-standing treatment of the canonical climate frameworks and a world-climate-type taxonomy that the substance entries cite rather than restate.

**Why a separate foundational entry.** The Climate rule (added in the previous turn) required each substance entry to apply Caraka Sū. 6 + Aṣṭāṅga Hṛdaya Sū. 3, _Su Wen_ chs. 2/5/12/66–74, Hippocrates' _Airs, Waters, Places_, and Galen's _De temperamentis_ to the relevant climate zones. Re-deriving that framework in every entry would bloat each entry and risk drift between them. A single canonical reference solves both problems and gives the substance entries a stable target to cite.

**What's in it.**
- *Classical frameworks for climate.* Full treatment of Ayurvedic _ṛtucaryā_ (six ṛtus, _ādāna_/_visarga_ split, doṣa cycle of _sañcaya_/_prakopa_/_praśama_) and _deśa_ (jāṅgala/sādhāraṇa/ānūpa); Chinese 六淫 with organ correspondences, the 五方 table from _Su Wen_ ch. 5, and the regional-therapeutics doctrine of _Su Wen_ ch. 12; Greco-Roman humoral with the four-humor/four-quality/four-season table; a brief Tibetan Sowa Rigpa note positioning _rGyud bzhi_ as the canonical frame for high-altitude.
- *World climate type taxonomy.* Eleven types — hot-arid; Mediterranean; hot-humid tropical; subtropical-humid; cool-damp temperate (Atlantic/oceanic); continental seasonal-extreme; cold-dry continental (steppe); cold-dry high-altitude; cold-damp boreal/subarctic; polar/arctic; tropical highland — each with geographic range + Köppen anchor, dravyaguna reading, 中醫 reading, Greco-Roman reading, and exemplary diet. Each entry also flags the climates that fall outside the canonical reach of one or more of the classical systems (Greco-Roman has no clean tropical or high-altitude treatment; polar is outside all three).
- *Cross-system convergences and divergences.* Named explicitly: convergence on hot-dry → cooling-moistening and cold-damp → warming-drying; divergence on tropics, high altitude, polar, monsoon-Vāta, and the warming/cooling reading of wheat.
- *Use within the materia medica.* The instruction that substance entries cite and apply — never re-derive — the framework, with _deśa-viruddha_ and _kāla-viruddha_ (Caraka Sū. 26) as the standard cross-references for modern globalized eating and seasonal-shift cases.

**Cross-references updated.** `materia-medica/CLAUDE.md` now (a) flags `climates.typ` in the File-structure section as a foundational-reference entry distinct from substance entries; (b) names `climates.typ` in the Climate rule as the canonical source substance entries must cite and apply; (c) instructs that if a needed framework concept is missing from `climates.typ`, it should be *added there first* and only then cited from a substance entry. This keeps the climate framework converging on one canonical place over time rather than diverging across entries.

**Placement note.** Filename `climates.typ` puts it alphabetically between `barley.typ` and `licorice-root.typ` in the materia-medica PDF. If front-of-document placement is preferred (since it's a foundational reference), the Makefile's glob-based file ordering would need adjustment or the file would need to be renamed with a sort-prefix. Left as `climates.typ` for now — flagged here for a possible later revisit.

---

## 2026-09-30 — Materia medica website (GitHub Pages, auto-deployed, searchable)

**Problem:** The materia medica is only distributed as a PDF, which isn't searchable across entries and requires a full rebuild-and-redistribute cycle to share updates.

**Decision:** Generate a static, full-text-searchable website from the same Typst sources, and auto-deploy it to GitHub Pages on every push via a GitHub Actions workflow. The Typst `.typ` files remain the single source of truth; no HTML is ever hand-written or committed.

**Reasoning:**
- Typst 0.14.2 ships an (experimental, `--features html`) HTML backend that converts each entry directly to clean semantic HTML — headings, `<em>`/`<strong>`, lists, and `#footnote[...]` calls all come out as proper `<a role="doc-noteref">` / endnote markup — so there was no need to hand-roll a Typst-to-HTML converter or duplicate content.
- Each entry file (`materia-medica/*.typ`) already compiles standalone (no cross-file `#include`/`#ref`/image dependencies), so entries can be compiled to HTML one at a time without going through the PDF's `materia-medica.typ` root document.
- Keeping the generator (script + CSS/JS templates) in the repo but the *output* out of the repo (`out/site/`, gitignored) means the website can never drift from the Typst sources — there is nothing to keep in sync by hand.
- Search is implemented client-side (vanilla JS, no dependency) against a generated `search-index.json` (full plain-text per entry, ~2 MB uncompressed for 81 entries) rather than a hosted search service, since the corpus is small and this needs zero infrastructure beyond static hosting.

**Changes:**
- Added `site/build.py`: runs `typst compile --features html --format html` per entry, extracts the `<body>` fragment, demotes heading levels so the entry title becomes the page's `<h1>`, injects heading `id`s and a per-entry table of contents, and renders each entry plus an `index.html` (grouped into Foundational references / Substance entries / Glossary, alphabetized) through a shared page template. Also writes `search-index.json`.
- Added `site/assets/style.css` (serif reading layout, light/dark via `prefers-color-scheme`, self-hosted `@font-face` for the bundled Noto Serif Devanagari, EB Garamond via Google Fonts) and `site/assets/search.js` (fetches the search index, live-filters by title/full-text with highlighted snippets, keyboard navigation).
- Added `.github/workflows/pages.yml`: on push to `master` touching `materia-medica/**`, `fonts/**`, or `site/**` (or manual `workflow_dispatch`), installs Typst 0.14.2 via `typst-community/setup-typst`, runs `site/build.py`, and deploys the output via `actions/upload-pages-artifact` + `actions/deploy-pages`. GitHub Pages must be switched to "GitHub Actions" as its source in the repo's Settings → Pages — that's a one-time manual step, not something a workflow can do for itself.
- Added `make site` (build to `out/site/`) and `make serve-site` (build + serve locally on port 8000) to the Makefile; added `/out/` to `.gitignore` (previously only `*.pdf` inside it was ignored).
- Documented the new architecture in the root `CLAUDE.md` under a new "Materia Medica Website" section.

**Alternatives considered:** a hand-written Typst→HTML converter (rejected — Typst's own HTML backend already does this correctly and the entries use only markup it supports); a hosted search service like Algolia (rejected — needless infrastructure and an external account for ~2 MB of text); committing the generated `out/site/` or a `docs/` folder for Pages (rejected — the whole point was for HTML to never be a checked-in, hand-maintained artifact).

**Known follow-up:** `materia-medica/apple.typ` (an in-progress, uncommitted entry) currently has a Typst syntax error (unclosed emphasis/strong delimiters around line 11) that will fail both `make materia-medica` and `make site`/the Pages workflow once it's committed — needs fixing before it's added to the repo.

---

## 2026-09-30 — Materia medica website: layout/typography pass and floating navigation

Follow-up round on the site added the previous day: matched the reading experience to feedback from actually using it, and added a way to move between entries and around a long entry without scrolling back to the index.

**Typography and layout, reworked twice.** First pass tried to mirror the PDF closely (11pt body text, a page-width-derived ~3.9in measure, a warm off-white/maroon palette) — rejected as "not my style"; wanted plain black-and-white instead, with the PDF's *relative* proportions (font family, heading-size ratios, justified text) kept but its *absolute* page geometry dropped in favor of whatever measure suits a browser. Landed on: plain monochrome (true inversion in dark mode, no accent color anywhere, including search highlights — bold+underline instead of colored `<mark>`); `--max-measure: min(38rem, 92vw)` instead of the PDF's fixed page width; base font size bumped from an initial 11pt to 15pt once the wider, device-appropriate measure made 11pt read as too many words per line for comfortable reading (headings/UI text didn't need separate tuning since they're already `em`-relative to the body size).

**Table of contents became a real side nav, not a layout participant.** The first version put the per-entry TOC and the article in a shared CSS grid track, which visibly squeezed the article's text width at medium viewport widths. Fixed by making `.entry`'s width unconditional (`max-width: var(--max-measure); margin: 0 auto`, full stop, regardless of viewport or TOC presence) and making the TOC `position: fixed`, positioned from the *viewport center* (`calc(50% - measure/2 - 15rem)`) rather than from a shared container — the two never compete for space again. Below 60rem there's no room for a fixed sidebar, so it's hidden entirely rather than falling back to squeezing.

**New: a floating "A–Z" entry switcher, on every page.** A circular button (bottom-right) opens a modal/drawer listing all 81 entries grouped by first letter, with a tap-or-drag A-Z index strip (iOS/Android contacts-app pattern) and the current entry marked. Backed by a new, deliberately small `nav-index.json` (slug/title/category only) so it opens instantly without waiting on the ~2MB full-text search index.

**New: a floating section-nav button, mobile only.** Below 60rem, where the sidebar TOC is hidden, a second button (list icon, stacked directly above the A–Z button) opens the *same* `#entry-toc` markup as a bottom drawer via a toggled `.open` class, rather than duplicating the TOC content.

**Three real bugs found and fixed along the way, all now documented in the new `site/CLAUDE.md` as gotchas to not reintroduce:**
1. A class rule (`.nav-overlay { display: flex }`) had equal CSS specificity to the browser's built-in `[hidden] { display: none }` and won by source order, so the nav panel showed immediately on page load regardless of the `hidden` attribute. Fixed with `:not([hidden])`.
2. `scrollIntoView`/`scrollTo` with `behavior: "smooth"` silently failed to scroll at all in testing (Chrome) — switched every programmatic scroll in `nav.js` to instant.
3. The A-Z jump only worked in one direction and only for some letters at first: `position: sticky` letter headers report unreliable `getBoundingClientRect()`/`offsetTop` (both reflect wherever the header is *currently pinned/pushed to*, not a stable layout position), so measuring live after the user had already scrolled gave wrong deltas. Fixed by caching every letter's offset once, immediately when the list is built and still unscrolled, and looking up the cache thereafter instead of re-measuring.

**New file:** `site/CLAUDE.md` — compiles the build pipeline, typography/layout system, floating-navigation design, the three gotchas above, and the CI setup into one reference, so this doesn't all need re-deriving from the diff next time. Root `CLAUDE.md`'s "Materia Medica Website" section now just points to it, mirroring how it already points to `materia-medica/CLAUDE.md` for content matters.

---

## 2026-09-30 — Sticky header covering anchor targets; FAB stack refactor; back-to-top button

Immediate follow-up to the floating-navigation work above, from actually using it: clicking a TOC link, footnote reference, or the A-Z entry list would scroll the target right underneath the sticky header (`.site-header`, up to ~108px tall when the search box wraps below it), making it look like navigation had silently failed or landed on the wrong entry.

**Fix:** `[id] { scroll-margin-top: 7.5rem; }` in `style.css`, applied globally rather than to a hand-picked list of selectors — covers headings, footnote refs, and footnote backlinks alike (anything that's ever an anchor target), and won't need updating if a new kind of anchorable content is added later.

**While in there, also added the requested back-to-top button** (`#top-fab`, up-arrow icon) and used the opportunity to stop hardcoding each floating button's `bottom` offset by hand — three buttons' worth of `calc(1.25rem + 3.2rem + 0.75rem + ...)` was already getting hard to keep in sync (the entry-TOC drawer's own clearance had to match it too). Replaced with `.fab-stack`, a `flex-direction: column-reverse` container that stacks however many buttons exist (1–3, depending on page and viewport) with a consistent gap automatically. Stack order, corner to top: A–Z (`#nav-fab`, every page) → section TOC (`#toc-fab`, entry pages only, below 60rem only) → back-to-top (`#top-fab`, every page). Also factored the buttons' shared circular styling into `.fab-circle`, applied alongside each button's own class.

Both changes are documented in `site/CLAUDE.md` (a new scroll-margin-top rule under **Layout**, and an expanded **Floating navigation** section) so the reasoning doesn't need re-deriving from a future diff.

---

## 2026-09-30 — Split into its own repository

**Problem:** This content lived in a private personal `writings` repository (diary, letters, and other personal material) alongside the materia medica. GitHub Pages needs a public repository (or a paid plan, for private-repo Pages) — but making `writings` public was never an option, given what else it contains.

**Decision:** Split the materia medica — content, website generator, GitHub Pages workflow, and the `herb-entry` skill — into this standalone repository, which can be public.

**What moved (working tree only, not git history — see below):** `materia-medica.typ`, `materia-medica/` (all entries + its `CLAUDE.md`), `site/` (generator + its `CLAUDE.md`), `.github/workflows/pages.yml` (branch trigger updated from `master` to this repo's `main`), the bundled Noto Serif Devanagari font files, `lib/page.typ` (the one piece of `writings`' shared Typst library that `materia-medica.typ` actually depends on, for its page-footer numbering), and `.claude/skills/herb-entry/SKILL.md`. Root `CLAUDE.md`, `Makefile`, and `.gitignore` were rewritten from scratch for a standalone repo rather than copied verbatim, since the originals mixed in diary/poetry-specific commands and paths that don't apply here.

**Git history was not transplanted.** This repo starts its own history from this commit rather than replaying `writings`' commits (which would risk dragging along commit-message context from a repo that needs to stay private). The prior entries in this log were copied over as plain text instead, so the documented reasoning survives even though the commits themselves don't. `writings`' own `log.md` keeps its original entries too — nothing was deleted there, since they're an accurate record of decisions made in that repo at the time, even though the content they describe has since moved.

**Left behind in `writings`, deliberately:** `lib/page.typ` (still needed there — `diary.typ` uses it too, independent of materia medica) and `.claude/settings.local.json` (machine/session-local Claude Code permissions, not project content, and full of hardcoded paths into the old repo that wouldn't even be correct here).

---

## 2026-10-03 — Formula entries; substances/ and formulas/ split

**Problem:** The project had grown to 86 substance entries sitting flat in `materia-medica/` alongside the two foundational references and the glossary, and there was no place for a *different kind* of entry. Classical formulas had been accumulating as cross-references inside substance entries (四君子湯 in `fuling.typ` and `korean-ginseng.typ`, 桑菊飲 in `chrysanthemum.typ`, 葦莖湯 in `coix.typ`, and so on) with nowhere to be treated in their own right — and a formula is a genuinely different object from a substance: the interesting question is not "what is this drug across four traditions" but "why *these* drugs, in these proportions, for this pattern."

**Decision:** Introduce formula entries as a first-class entry kind, and split the entry files into `materia-medica/substances/` and `materia-medica/formulas/`.

**Structure.** `climates.typ`, `tibb-al-arabi.typ`, and `zz-glossary.typ` stay at the `materia-medica/` root — they are neither substances nor formulas, and leaving them there means the root holds exactly the non-entry material. The 86 substance files moved with `git mv` to preserve rename detection.

**The book now assembles four ordered groups rather than one flat glob.** The Makefile builds `MM_REFERENCE`, `MM_SUBSTANCES`, `MM_FORMULAS`, `MM_GLOSSARY` and passes each as its own `--input`; `materia-medica.typ` includes them in order and emits centered *Substance Entries* and *Formulas* divider pages between them (level-1 headings, so they also appear in the front outline as section markers). The previous single `files=` input is gone. An empty formulas glob is harmless — the group-include already skips empty strings.

**Site categories became folder-derived rather than slug-listed.** `category_for()` now takes the source `Path` and reads its parent folder (`formulas/` → `"formula"`, `substances/` → `"entry"`), with the glossary and the two references still special-cased by slug at the root. The practical gain: adding a substance or a formula needs no registration in `build.py` — only a genuinely new *kind* of entry does. `CATEGORY_ORDER` drives both the index grouping and its headings, so the new Formulas group appeared on the index without further changes.

**Slugs share one flat namespace, and that is now enforced rather than assumed.** The site emits `<slug>.html` with no folder in the output path, so a substance and a formula with the same filename would silently overwrite each other. `entry_sources()` raises a `BuildError` naming both paths instead.

**Cross-references were deliberately left as bare filenames.** Entries refer to each other in prose as `fuling.typ`, not `substances/fuling.typ`. Nothing in either build resolves these into links — they are human-readable pointers, filenames are unique project-wide, and rewriting ~90 files' worth of them would have been churn with no benefit. New entries may use the folder-qualified form where it aids clarity; the convention is documented in root `CLAUDE.md` so it does not get "fixed" later.

**New: `materia-medica/formulas/CLAUDE.md`** — the authoritative formula-entry spec, mirroring how `materia-medica/CLAUDE.md` governs substances and inheriting its rules on honesty & sourcing, the glossary, footnotes, and tone. The substantive departures from the substance template:
- **No four-tradition comparative frame.** A Chinese formula is a Chinese artifact; manufacturing an Ayurvedic or Tibb reading of one would be exactly the dressing-up-reasoned-extension-as-canon that this project's honesty standard forbids. Cross-system parallels go in a closing note, marked as comparison.
- **Ingredients get 君臣佐使 roles** and their function *inside that formula*, not a generic description of the herb.
- **Self-contained property summaries are mandatory** — each ingredient block opens with 性/味/歸經 plus principal actions, so a formula entry reads without opening the substance entries for each herb. This was the user's explicit requirement and is the rule most likely to be quietly economized on.
- **No Typst tables.** A five-column ingredient table is unreadable on a 5-inch page and arrives unstyled through the site's HTML pipeline; bulleted per-ingredient blocks instead.
- Template: Name & Meaning / Source & History / Composition (with per-ingredient subsections) / Formula Architecture / Indications & Pattern / Modifications & Derived Formulas / Preparation & Administration / Cautions & Contraindications / Modern Pharmacology / Sources.

**New: `formula-entry` skill** (`.claude/skills/formula-entry/SKILL.md`), the formula-side counterpart of `herb-entry`. It carries one instruction worth noting: match the substance entries' own attributions for shared herbs, and surface a genuine conflict rather than silently picking a side — the substance entries are where this project's property and dose attributions live, and a formula entry that quietly contradicts them would corrupt both.

**First formula entry: Four Gentlemen Decoction (四君子湯).** Chosen as the base case deliberately — it is the 基礎方 of the entire 補氣 category, so its derived family (異功散, 六君子湯, 香砂六君子湯, 參苓白朮散, 八珍湯, 十全大補湯) gives the new entry kind something substantial to be the parent of, and three of its four ingredients already have substance entries to summarize and cross-reference. Notes from writing it:
- The name turns on the Confucian 君子 — drugs that work by sustained support rather than force — with a pun on 君 as the technical term for a formula's sovereign drug. Both readings are current; the entry gives both rather than choosing.
- 白朮 has no substance entry yet, so its summary is given in full and the gap is stated in the entry rather than left as a silent omission.
- Formula-level modern evidence is thinner than the constituent herbs' — most of what exists concerns the Kampo derivative 六君子湯 (Rikkunshitō), not 四君子湯 itself. The entry says so, and explicitly does not import the single-herb literature as evidence for the compound.
- The practical ceiling on the formula is its 炙甘草: glycyrrhizin pseudoaldosteronism is what limits duration and dose, and is the reason modern practice reduces the licorice below the classical equal parts.

**Glossary:** ~20 new terms, including a new *Formula construction* subsection under the Chinese-medicine section (君臣佐使, 基礎方, 加減, 補中有瀉, 另煎, 錢, 顆粒) — plus 運化, 脾虛生濕, and the drug and formula names the entry introduces (白朮/蒼朮, 炙甘草, 四物湯, 理中丸, and an expanded 四君子湯 entry listing the derived family). 補中有瀉 and 君臣佐使 had both been *used* in earlier entries without ever being defined; that gap is now closed.

---

## 2026-10-03 — Four titled parts in the PDF; three-level table of contents

Follow-up to the restructure earlier today, from reading the result: the book had two section dividers (*Substance Entries*, *Formulas*) but the foundational references and the glossary floated outside any part, and the table of contents listed only entry titles — so you could jump to an entry but not to a section within one, in a 1,400-page book.

**Four titled parts, each with a divider page:** **Substances** → **Recipes & Formulas** → **Miscellaneous** (the two foundational framework entries, `climates.typ` and `tibb-al-arabi.typ`) → **Glossary**.

*On the ordering:* the glossary is placed last rather than third as listed in the request, because this project already encodes "glossary goes last" in the `zz-` filename prefix, and the website's index orders it last too — keeping book and site consistent mattered more than literal list order. Swapping the last two parts is a two-line change in `materia-medica.typ` if the other order is preferred.

*On the naming:* the PDF part is called **Miscellaneous** per the request, while `site/build.py` still labels the same two files **Foundational references** (`CATEGORY_LABELS`). Deliberately left divergent because the request was scoped to the PDF, but it is a real inconsistency for anyone using both — aligning it is a one-line change.

**The Makefile's `MM_REFERENCE` / `reference=` input was renamed `MM_MISC` / `misc=`** so the build inputs match the part names.

**Three-level table of contents.** The enabling trick is `#set heading(offset: 1)` around each included group: a part divider is a level-1 heading, and inside a group every entry's own `=` title becomes level 2 and its `==` sections level 3. *Entry files are untouched and keep using `=` / `==` as before* — the offset lives entirely in the root document, which is what makes this possible across 90 files without editing any of them.

`outline(depth: 3, indent: 0.6em)` then lists parts, entries, and sections, with `show outline.entry.where(level: …)` rules styling each level: parts at 1.15em bold with space above, entry titles bold, section names at 0.82em. Two iterations were needed — the first pass made parts and entry titles both plain bold (indistinguishable at a glance) and left section names large enough that long headings like "Traditional Arabic & Islamic Medicine (Ṭibb al-ʿArabī wa-l-Islāmī / Unani)" wrapped to three lines in a 1.85in column. Enlarging the part level and dropping sections to 0.82em fixed both and *reduced* total page count. Part divider titles were also enlarged to 1.9em, since a default level-1 heading alone on an otherwise blank page read as undersized.

**Cost:** the TOC grew from ~3 pages to ~19, and the book from 1,410 to 1,426 pages. Worth it for a reference work that is navigated rather than read through — the point is being able to jump to a specific entry's *Climate, Constitution & Regional Diet*, not just to the entry.

---

## 2026-10-03 — Four Substances Decoction; new required "Misapplication & Look-Alike Patterns" section

**Second formula entry: Four Substances Decoction (四物湯)**, the blood-nourishing counterpart to 四君子湯 — the two were built by the tradition as a matched pair and now sit as a matched pair in the book.

Notes from writing it:
- **The formula's history is a repurposing.** Its canonical source is the Song _Hejijufang_ (1107–1110), but the combination appears earlier in the Tang _Xiān Shòu Lǐ Shāng Xù Duàn Mì Fāng_ as a **trauma** formula — for moving damaged blood, not nourishing deficient blood. The residue of that origin is still visible in the composition: a purely nourishing formula would have no need of 川芎 at all.
- **An in-book divergence, flagged rather than smoothed.** `substances/rehmannia.typ` describes 四物湯 as using 生地黃 "or 熟地黃 in tonifying-blood variants"; `substances/dang-gui.typ` gives 熟地黃 flatly. The standard transmitted composition uses the prepared root, and the entry says so while noting that the rehmannia entry's phrasing is the looser of the two and would be worth tightening. This is the case the `formula-entry` skill's "surface a genuine conflict rather than silently picking a side" rule was written for, and it came up on the very next entry.
- 白芍 and 川芎 have **no substance entries**, so their properties are given in full and the gap is stated, as was already done for 白朮.

**New required section, added to the template: `== Misapplication & Look-Alike Patterns`**, with two subsections — *If given to the wrong pattern* and *Patterns mistaken for this one*. It sits immediately after *Indications & Pattern*, as its negative image.

The reasoning for making it required rather than optional: the classical literature is generous about what a formula treats and comparatively terse about what happens when it is given wrongly, and that asymmetry is exactly where a reference book can add something. So the spec demands **mechanism, consequence, and correction** — not merely "contraindicated in X" — plus, for each look-alike pattern, the **one distinguishing sign** that decides it and what to give instead.

**Division of labour, written into the spec** because three sections were otherwise going to say overlapping things:
- *Indications → Differentiation* — comparing formulas once the pattern is **correctly** identified.
- *Misapplication* — **diagnostic error**: being wrong about the pattern, and what that costs.
- *Cautions* — **pharmacological safety**: interactions, dose ceilings, risk groups.

Applying this immediately paid off on the existing entry: Four Gentlemen's *Cautions* section had been listing pattern contraindications at length, which now duplicated the new section, so it was cut back to a one-line summary plus a pointer.

**Each entry must include at least one *modern* trap** — a biomedical label routinely equated with the pattern but not identical to it. For 四物湯 that is **anaemia ≠ 血虛** (a haemoglobin value is not a prescription, and the two diverge in both directions); for 四君子湯, **chronic fatigue ≠ 氣虛** (fatigue is the presenting complaint of a dozen patterns and of a long list of biomedical conditions). Both entries also mark the point at which pattern reasoning should defer to biomedical workup rather than compete with it.

**Backfilled Four Gentlemen** with the same section. Writing it surfaced a failure mode worth recording: for a *mild* formula the usual consequence of misapplication is not harm but **nothing at all**, while weeks pass and the real pattern goes untreated — a clinical problem that the formula's reputation for gentleness actively conceals. Flagged in the entry as this book's own observation rather than a classical statement.

**Updated:** `materia-medica/formulas/CLAUDE.md` (template + full section spec + division of labour), `.claude/skills/formula-entry/SKILL.md` (template + a non-negotiable bullet). **Glossary:** 閉門留寇, 滋膩, 補血而不滯血, 血虛, 肝鬱, 白芍/赤芍, 川芎, and an expanded 四物湯 entry.
