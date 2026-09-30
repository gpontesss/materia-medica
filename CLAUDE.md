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

`materia-medica.typ` (root) receives a comma-separated list of entry files via `sys.inputs.files`, then `#include`s each one. The Makefile builds that list from `./materia-medica/*.typ` and passes it at compile time — new entries are picked up automatically, no registration needed.

**Shared library** (`lib/`): `lib/page.typ` — `numbered-footer()` for centered italic page numbers, used by `materia-medica.typ`'s page footer.

## Fonts

Bundled in `fonts/`; the Makefile passes `--font-path ./fonts` to every `typst compile` call.

- **Noto Serif Devanagari** (Regular + Bold, OFL 1.1) — Devanagari fallback for Sanskrit text, set via `#set text(font: ("EB Garamond", "Noto Serif Devanagari"))` in `materia-medica.typ`. Typst falls through to it for any codepoint EB Garamond can't render. Sourced from `notofonts/noto-fonts` on GitHub.

## The website (`site/`)

For anything related to `site/` — the generated website, its build pipeline, layout, typography, navigation, or search — **always read and apply [`site/CLAUDE.md`](site/CLAUDE.md) first**. It defines the build pipeline, the typography and layout system, the floating-navigation components (with several hard-won CSS/JS gotchas worth reading before touching that code), and the CI deploy setup.

The one rule worth repeating here: `site/` holds a *generator*, not a website. **The generated HTML is never hand-written and never committed** — `out/site/` is gitignored and rebuilt from the Typst sources every time, locally via `make site` or in CI (`.github/workflows/pages.yml`, on every push to `main` touching `materia-medica/**`, `fonts/**`, or `site/**`). GitHub Pages must have its source set to "GitHub Actions" in the repo's Settings → Pages — a one-time manual step, not something the workflow can do for itself.

## Entry content (`materia-medica/`)

For anything related to `materia-medica/` — creating or editing entries, formatting, sourcing, nomenclature, or any content decisions — **always read and apply [`materia-medica/CLAUDE.md`](materia-medica/CLAUDE.md) first**. It defines the entry template, scholarly standards, language requirements, prabhāva/viruddha/dosage rules, honesty/sourcing standards, and output format.

A **`herb-entry` skill** (`.claude/skills/herb-entry/SKILL.md`) automates adding a new substance entry end-to-end (template, glossary update, build, pre-build lint for the common Typst unbalanced-delimiter mistakes) — use it rather than hand-rolling a new entry.

## Maintenance Rules

- **Update `log.md`** whenever a non-trivial decision is made (font choice, architecture change, new document type, tooling change). Record the problem, the decision, the reasoning, and alternatives considered.
- **Update `CLAUDE.md`** (this file, `materia-medica/CLAUDE.md`, or `site/CLAUDE.md`) when commands, architecture, or conventions change.
- **Do not commit.** Leave git staging and committing to the user.
