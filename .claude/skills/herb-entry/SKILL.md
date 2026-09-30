---
name: herb-entry
description: Create a new substance entry for the comparative materia medica (materia-medica/). Use when the user asks to add, write, or draft a materia-medica entry for a food, herb, spice, or medicinal — e.g. "add a materia medica entry for saffron", "write up nutmeg for the materia medica", "new herb entry: clove". Produces a Typst entry file following the project's scholarly template, updates the glossary, and builds the PDF.
---

# herb-entry — add a materia medica entry

Create a new substance entry in `materia-medica/` that conforms to the project's scholarly standards.

## Step 0 — Read the rules first (mandatory)

Before writing anything, read **`materia-medica/CLAUDE.md`**. It is the authoritative specification and OVERRIDES anything summarized here. In particular apply its:

- Standard entry template (8 sections, in order)
- Languages & naming requirements (Latin/English/Chinese/Sanskrit + Arabic where classical in Tibb)
- Prabhāva rule, Viruddha rule (source-tier tagging), Tibb rule, Climate rule, Dosage rule
- Glossary rule (mandatory-update protocol)
- Honesty & sourcing standards, output format (footnotes), tone

Also skim one or two existing entries that resemble the new substance, to match register and structure:
- A classical, fully-attested drug: `materia-medica/licorice-root.typ`, `ginger.typ`, `honey.typ`
- A reasoned-only / New-World or East-Asian item: `acai.typ`, `guarana.typ`, `green-tea.typ`
- Foundational references cited by every entry: `tibb-al-arabi.typ`, `climates.typ`, `zz-glossary.typ`

## Step 1 — Confirm the referent

Pin down exactly which substance and which drug-form(s) before drafting (species, part used, distinct named forms). If the common name is ambiguous across systems, note the scope up front. If the user hasn't specified, ask.

## Step 2 — Pick the slug and create the file

- Slug = short lowercase hyphenated name (e.g. `saffron.typ`, `black-pepper.typ`). Check it doesn't already exist in `materia-medica/`.
- The file lives at `materia-medica/<slug>.typ`. **No** `#import`, no frontmatter — it starts directly with the top-level heading `= Substance Name` and flows through the template using Typst headings (`=`, `==`, `===`).
- New files are picked up automatically by the Makefile glob; no registration needed.

Template skeleton (see `materia-medica/CLAUDE.md` for the full section spec — do not skip sections; mark genuinely-inapplicable ones as such rather than padding):

```typ
= Substance Name

== Nomenclature & Etymology

== Classical Chinese Medicine (中醫) View

== Ayurvedic Dravyaguna (द्रव्यगुण)

=== Viruddha (विरुद्ध — incompatibilities)

== Traditional Arabic & Islamic Medicine (Ṭibb al-ʿArabī wa-l-Islāmī / Unani)

== Classical Formulas & Preparations

=== Chinese medicine (中醫)

=== Ayurveda

=== Western / Greco-Roman

=== Tibb (Arabic-Islamic)

== Climate, Constitution & Regional Diet

== Modern Nutrition & Pharmacology

== Sources
```

## Step 3 — Write the entry

Follow the standards in `materia-medica/CLAUDE.md` exactly. Non-negotiables:

- **Footnote every claim at its point of assertion** with `#footnote[...]`, and keep the end-of-entry **Sources** bibliography as well.
- **Cite specific classical texts/editions.** Do not fabricate precise page numbers — name work, section, edition.
- **Distinguish citing a tradition from applying it.** For substances outside a system's canon (New-World, post-classical, purely regional), mark the section "reasoned analysis, not classical" — don't dress reasoned extension as canonical authority.
- **Flag** interpretive/modern/lower-tier claims, cross-system divergences, and things you'd want to verify against a specific edition.
- Native scripts with transliteration (characters + pinyin; Devanāgarī + IAST; Arabic script + Romanization). Etymology from lexicographic sources (Monier-Williams, LSJ, Lewis & Short, de Vaan, OED), not the medical texts; flag folk etymologies.

## Step 4 — Update the glossary (mandatory, same change)

Every foreign-language technical term newly used in the entry that is not already in `materia-medica/zz-glossary.typ` MUST be added there in this same change — no exceptions. Follow the glossary's per-tradition organization and per-term format (native script, transliteration, gloss, 1–2 sentence definition, register note, cross-references). If a needed climate/Tibb concept is missing from `climates.typ` / `tibb-al-arabi.typ`, add it there first, then cite it.

## Step 5 — Build and verify

```sh
make materia-medica
```

Confirm it compiles cleanly to `out/materia-medica.pdf` and fix any Typst errors. Devanagari renders via the bundled Noto Serif Devanagari fallback — no font setup needed.

**Pre-build check (run this first — it catches most failures before compiling):** scan each new file for lines with an odd number of unescaped `*` (unbalanced bold), the single commonest cause of `error: unclosed delimiter`:

```sh
awk '{ l=$0; gsub(/\\\*/,"",l); n=gsub(/\*/,"*",l); if (n%2==1) print FILENAME":"NR": ("n") "$0 }' materia-medica/<slug>.typ
```

Also grep for `\*/` and `/\*` (see first gotcha). Fix everything these flag, then `make materia-medica`.

**Known Typst gotchas (each has caused a failed build in practice — scan for them before building):**
- **`*/` adjacency** — a bold span immediately followed by a slash (e.g. `*kṣāraṇa*/_saṃgrāhī_`) is parsed as a block-comment close (`error: unexpected end of block comment`). Put a space or a word between them, or reword. Grep the new file for `\*/` and `/\*`.
- **Linguistics/reconstruction asterisk** — a reconstructed form written `*_h₂ébōl_` or `*_aplaz_` (the `*form` convention for PIE/Proto-Germanic etymons) is read as a bold-toggle and unbalances the line (`error: unclosed delimiter`). **Escape the leading asterisk as `\*`** — e.g. `\*_h₂ébōl_`. This is easy to hit in the Nomenclature & Etymology section.
- **Missing closing `*` in a long bold-item list** — enumerations of many `*term (gloss)*` items (cultivar lists, drug-form lists) frequently drop one closing `*`, after which the next item's `*` becomes the closer and the whole tail is mis-parsed. The odd-`*`-count check above catches this.
- **Detached/unbalanced `_` emphasis in long scope lines** — in the italic `_Scope: …_` paragraphs, mixing many `_word_` spans with inline parentheticals and em-dashes easily produces a space-before-underscore (`system _—`) that *opens* emphasis instead of closing it, giving `error: unclosed delimiter`. Safest pattern: wrap the whole scope sentence in **one** `_…_` block and use *bold* (`*…*`) for the emphasised terms inside it, rather than alternating italic on/off. An opening `_` must be preceded by whitespace and followed by non-space; a closing `_` must be preceded by non-space.
- Also watch: unescaped `#`/`@` at line start, unbalanced `#footnote[...]` brackets, and stray unmatched `_`/`*`.

## Step 6 — Maintenance

If a non-trivial decision was made (new template section, convention change, tooling), update `log.md` and, if conventions changed, `CLAUDE.md` / `materia-medica/CLAUDE.md` per the repo's Maintenance Rules.

**Do not commit.** Leave git staging and committing to the user.
