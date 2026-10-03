# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A personal, public comparative materia medica of foods and medicinals — synthesizing Classical Chinese Medicine, Ayurvedic dravyaguna, Tibb (Greco-Arabic medicine), and modern nutrition & pharmacology. Entries are written in Typst (`.typ`), compiled to a print-ready PDF, and also published as a searchable website via GitHub Pages.

This repository was split out from a larger private personal-writings repository so it could be public (GitHub Pages requires that, or a paid plan for private Pages) without exposing unrelated personal content. See `log.md` for that split and the full decision history before it.

## Build Commands

```sh
make materia-medica # compile materia-medica.pdf → out/materia-medica.pdf
make site           # generate the website → out/site/
make serve-site     # generate the website and serve it at localhost:8000
make clean          # remove out/
```

The build tool is [Typst](https://typst.app/).

## Architecture

Entries are organized into two folders plus three non-entry files:

```
materia-medica/
  substances/     ← one file per substance (herb, spice, food, medicinal)
  formulas/       ← one file per classical formula
  climates.typ        ← foundational reference (climate frameworks)
  tibb-al-arabi.typ   ← foundational reference (Greco-Arabic framework)
  zz-glossary.typ     ← back-matter glossary
```

`materia-medica.typ` (root) receives **four** comma-separated groups via `sys.inputs` — `reference`, `substances`, `formulas`, `glossary` — and `#include`s each group in that order, emitting a *Substance Entries* and a *Formulas* section divider between them. The Makefile builds the groups by glob (`MM_SUBSTANCES`, `MM_FORMULAS`) and passes them at compile time, so **new entries are picked up automatically — just put the file in the right folder, no registration needed.**

Entry **slugs share one flat namespace** (the site generates one `<slug>.html` per entry); `site/build.py` fails the build on a collision.

**Cross-references between entries are written as bare filenames** in prose (`fuling.typ`), sometimes with the folder for clarity (`substances/fuling.typ`). These are human-readable pointers, not resolved links — nothing in the build turns them into hyperlinks. Do **not** mass-rewrite the corpus's existing bare-filename references into paths; filenames are unique project-wide and the churn would be pure cost.

**Shared library** (`lib/`): `lib/page.typ` — `numbered-footer()` for centered italic page numbers, used by `materia-medica.typ`'s page footer.

## Fonts

Bundled in `fonts/`; the Makefile passes `--font-path ./fonts` to every `typst compile` call.

- **Noto Serif Devanagari** (Regular + Bold, OFL 1.1) — Devanagari fallback for Sanskrit text, set via `#set text(font: ("EB Garamond", "Noto Serif Devanagari"))` in `materia-medica.typ`. Typst falls through to it for any codepoint EB Garamond can't render. Sourced from `notofonts/noto-fonts` on GitHub.

## The website (`site/`)

For anything related to `site/` — the generated website, its build pipeline, layout, typography, navigation, or search — **always read and apply [`site/CLAUDE.md`](site/CLAUDE.md) first**. It defines the build pipeline, the typography and layout system, the floating-navigation components (with several hard-won CSS/JS gotchas worth reading before touching that code), and the CI deploy setup.

The one rule worth repeating here: `site/` holds a *generator*, not a website. **The generated HTML is never hand-written and never committed** — `out/site/` is gitignored and rebuilt from the Typst sources every time, locally via `make site` or in CI (`.github/workflows/pages.yml`, on every push to `main` touching `materia-medica/**`, `fonts/**`, or `site/**`). GitHub Pages must have its source set to "GitHub Actions" in the repo's Settings → Pages — a one-time manual step, not something the workflow can do for itself.

## Entry content (`materia-medica/`)

Two authoritative specs, by entry kind:

- **Substance entries** — for anything related to `materia-medica/substances/` or the foundational references: creating or editing entries, formatting, sourcing, nomenclature, or any content decision, **always read and apply [`materia-medica/CLAUDE.md`](materia-medica/CLAUDE.md) first**. It defines the 8-section entry template, scholarly standards, language requirements, prabhāva/viruddha/Tibb/climate/dosage rules, the glossary rule, honesty/sourcing standards, and output format.
- **Formula entries** — for anything under `materia-medica/formulas/`, **always read and apply [`materia-medica/formulas/CLAUDE.md`](materia-medica/formulas/CLAUDE.md) first**. It defines the formula template (君臣佐使 ingredient roles, mandatory self-contained property summaries, architecture, preparation method, cautions) and inherits the substance-entry rules on honesty, sourcing, footnotes, glossary, and tone.

Two skills automate these end-to-end (template, glossary update, build, pre-build lint for the common Typst unbalanced-delimiter mistakes) — use them rather than hand-rolling an entry:

- **`herb-entry`** (`.claude/skills/herb-entry/SKILL.md`) — a single substance.
- **`formula-entry`** (`.claude/skills/formula-entry/SKILL.md`) — a classical formula.

## Maintenance Rules

- **Update `log.md`** whenever a non-trivial decision is made (font choice, architecture change, new document type, tooling change). Record the problem, the decision, the reasoning, and alternatives considered.
- **Update `CLAUDE.md`** (this file, `materia-medica/CLAUDE.md`, or `site/CLAUDE.md`) when commands, architecture, or conventions change.
- **Do not commit.** Leave git staging and committing to the user.
