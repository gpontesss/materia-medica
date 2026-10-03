# CLAUDE.md — Formula Entries

This file is the authoritative specification for **formula entries** (`materia-medica/formulas/*.typ`). It is the formula-side counterpart of `materia-medica/CLAUDE.md`, which governs substance entries. Where this file is silent, the substance-entry rules apply — in particular the **honesty & sourcing standards**, the **glossary rule**, the **footnote output format**, and the **tone** requirements, all of which carry over unchanged.

## What a formula entry is, and how it differs from a substance entry

A substance entry asks *what is this drug, across four traditions?* A formula entry asks a different question: *why these drugs, in these proportions, for this pattern?* The unit of analysis is the **composition and its internal logic**, not the comparative pharmacology of a single plant.

Consequences:

- **No four-tradition comparative frame.** A Chinese formula is a Chinese artifact. Do not manufacture an Ayurvedic or Tibb reading of it. (Cross-system *parallels* — e.g. an Ayurvedic formula occupying the same clinical slot — belong in a short closing note, clearly marked as comparison, not as attestation.)
- **The ingredient roster carries the weight.** Every ingredient gets its function *inside this formula* spelled out, by its classical hierarchical role (君臣佐使 — sovereign, minister, assistant, envoy).
- **Self-contained property summaries are mandatory.** See the rule below.

## The self-contained-summary rule (non-negotiable)

Each ingredient's block **must** open with a compact property line giving at minimum its **性 (property), 味 (flavor), 歸經 (channels entered)**, and its **principal classical actions** — so that the formula entry can be read and understood on its own, without opening the substance entries for each herb. A reader should never have to navigate away to follow the argument.

Cross-reference the substance entry as well (`see substances/fuling.typ`) for the full treatment — but the summary must stand alone. Where an ingredient has **no** substance entry yet, say so plainly rather than silently omitting the cross-reference.

**Do not use Typst tables for this.** The book page is 5 inches wide and a multi-column table of five ingredients is unreadable there; tables also arrive unstyled through the site's HTML pipeline. Use the bulleted per-ingredient blocks the template specifies.

## Standard entry template (in this order)

```typ
= Formula Name (Pinyin, 中文)

== Name & Meaning

== Source & History

== Composition

=== <Ingredient> (君 — sovereign)

=== <Ingredient> (臣 — minister)

== Formula Architecture

== Indications & Pattern

== Modifications & Derived Formulas

== Preparation & Administration

== Cautions & Contraindications

== Modern Pharmacology

== Sources
```

Section specifications:

1. **Opening scope line** (italic, before the first `==`, as in substance entries) — what the formula is, its category, its source text and date, and a one-sentence statement of the pattern it treats. A reader skimming should get the whole formula from this paragraph.
2. **Name & Meaning** — the characters, pinyin, and *literal* translation; the standard English rendering(s); and what the name actually alludes to. Formula names are frequently metaphorical, allusive, or drawn from literature and should be unpacked properly, with etymological/lexicographic sourcing where the allusion is literary rather than medical. Flag homonymous traps (e.g. 四君子湯 the formula vs. 四君子 the painting trope).
3. **Source & History** — the earliest text that carries the formula (title, author, date, edition), the transmission since, and its standing in modern practice. Where attribution is contested or the formula predates its earliest surviving source, say so and flag it.
4. **Composition** — the full roster with **doses** (classical proportions and modern clinical grams), then one `===` subsection per ingredient, headed with its **君臣佐使 role**. Each subsection carries: the compact property line (see above); what the ingredient *does in this formula specifically*; and why it, rather than a near-neighbour, is the one used. Note processing/drug-form requirements (e.g. 炙甘草 honey-fried, not raw) — these are part of the composition, not a detail.
5. **Formula Architecture** — the argument of the formula: how the roles compose, what pathological mechanism the structure addresses, and what would break if an ingredient were removed. This is the section that distinguishes a formula entry from a list.
6. **Indications & Pattern** — the classical pattern (症候) with its presenting signs, including tongue and pulse; the modern biomedical correlates where they can be stated honestly; and the **differentiation** from formulas treating adjacent patterns.
7. **Modifications & Derived Formulas** — the classical modifications (加減) and the named derived formulas built on this base, each with what the addition changes. For a base formula like 四君子湯 this section is substantial and is one of the entry's main justifications for existing.
8. **Preparation & Administration** — the classical method (decoction, powder, pill; water volume, reduction, order of addition, pre- or post-decoction of particular drugs), dose, timing relative to meals, course length, and the modern forms (granules, patents) with their differences flagged.
9. **Cautions & Contraindications** — patterns in which the formula is wrong, classical incompatibilities among or affecting its ingredients (十八反 / 十九畏 where relevant), modern herb-drug interactions arising from the constituents, and risk groups. Tag modern-tier claims as such.
10. **Modern Pharmacology** — brief and honestly tiered: what has been studied *as the whole formula* (not just the isolated herbs), and where the evidence is preclinical, small-trial, or absent. Formula-level evidence is usually thinner than single-herb evidence; say so rather than importing the herbs' literature wholesale.
11. **Sources** — full bibliography, as in substance entries.

Sections that genuinely do not apply should be marked as such, not padded.

## Naming and slugs

- Slug = lowercase hyphenated **English** name (`four-gentlemen-decoction.typ`), not pinyin — the English names are what a reader searches for, and pinyin romanization of formula names is inconsistent across sources.
- Slugs share **one flat namespace** with substances, since the site generates one `<slug>.html` per entry. `site/build.py` fails the build on a collision.
- Title line gives English, pinyin, and characters: `= Four Gentlemen Decoction (Sì Jūnzǐ Tāng, 四君子湯)`.

## Cross-references

Reference substance entries by bare filename as the rest of the book does (`fuling.typ`), or with the folder where it aids clarity (`substances/fuling.typ`). **Do not rewrite the existing corpus's bare-filename references into paths** — they are human-readable pointers, filenames are unique across the project, and the churn would be pure cost.

## Glossary rule

Applies in full, per `materia-medica/CLAUDE.md`. Formula entries introduce a lot of new vocabulary — formula names, role terms (君臣佐使), preparation verbs, pattern names — and **every new foreign-language technical term must be added to `zz-glossary.typ` in the same change**. Formula *names* are glossed when the name is itself allusive or a known source of confusion; otherwise the entry carries them.

## Build

Formula files are picked up automatically by the Makefile's `MM_FORMULAS` glob and by `site/build.py`'s `formulas/` scan — no registration needed. They form their own section in the PDF (after the substances, before the glossary) and their own group on the site index.
