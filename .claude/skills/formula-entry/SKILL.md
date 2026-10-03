---
name: formula-entry
description: Create a new formula entry for the comparative materia medica (materia-medica/formulas/). Use when the user asks to add, write, or draft an entry for a classical formula, decoction, powder, pill, or compound preparation — e.g. "add Four Gentlemen Decoction", "write up Liu Wei Di Huang Wan", "new formula entry: Sang Ju Yin", "add Guī Pí Tāng to the book". Produces a Typst formula entry following the project's formula template — full ingredient roster with 君臣佐使 roles and self-contained property summaries, history, architecture, preparation method, and cautions — updates the glossary, and builds the PDF. For single substances (a herb, spice, food), use herb-entry instead.
---

# formula-entry — add a formula entry

Create a new formula entry in `materia-medica/formulas/` that conforms to the project's scholarly standards.

## Step 0 — Read the rules first (mandatory)

Read **`materia-medica/formulas/CLAUDE.md`** — the authoritative specification for formula entries, which OVERRIDES anything summarized here. Then read **`materia-medica/CLAUDE.md`** for the rules that carry over unchanged: honesty & sourcing standards, the glossary rule, footnote output format, and tone.

Also skim one existing formula entry for register and structure, and one or two of the **substance** entries for the herbs in the formula — you will be summarizing their properties, and the substance entries are where the project's own attributions live. Matching them is mandatory: **do not introduce a property, dose, channel, or source attribution that contradicts the substance entry for the same herb.** If you find a genuine conflict, say so rather than silently picking one.

- Formula entries: `materia-medica/formulas/four-gentlemen-decoction.typ`
- Substance entries for typical ingredients: `materia-medica/substances/fuling.typ`, `korean-ginseng.typ`, `chinese-licorice.typ`
- Foundational references cited throughout: `materia-medica/climates.typ`, `tibb-al-arabi.typ`, `zz-glossary.typ`

## Step 1 — Confirm the referent

Pin down *which* formula before drafting:

- **Which source text and which version.** Many formulas exist in several versions with different ingredient lists (e.g. 歸脾湯 as transmitted by Yan Yonghe vs. the later expanded version). Name the one being treated.
- **Which name.** Formula names are ambiguous across romanizations and translations; give characters + pinyin + the standard English rendering. Check for homonymous traps (四君子湯 the formula vs. 四君子 the literati painting trope; 生脈散 vs. its injectable modern derivative).
- **Base or derivative.** If the user names a derived formula (六君子湯), establish whether the base (四君子湯) already has an entry — the derivative should reference it rather than restate its architecture.

If genuinely ambiguous and the user has not specified, ask.

## Step 2 — Pick the slug and create the file

- Slug = lowercase hyphenated **English** name: `four-gentlemen-decoction.typ`, `six-flavor-rehmannia-pill.typ`. Not pinyin.
- Check the slug does not already exist **anywhere** — slugs share one flat namespace with substances (`materia-medica/substances/`, `materia-medica/formulas/`, and the three root files). `site/build.py` fails the build on a collision.
- The file lives at `materia-medica/formulas/<slug>.typ`. No `#import`, no frontmatter — it starts directly with `= Formula Name (Pinyin, 中文)` and flows through the template using `=`, `==`, `===`.
- New files are picked up automatically by the Makefile's `MM_FORMULAS` glob and by `site/build.py` — no registration needed.

## Step 3 — Write the entry

Follow `materia-medica/formulas/CLAUDE.md` exactly. The template:

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

Non-negotiables specific to formula entries:

- **Every ingredient gets its 君臣佐使 role** in its `===` heading, and its function *inside this formula* in the body — not a generic description of the herb.
- **Every ingredient block opens with a self-contained property line**: 性 (property), 味 (flavor), 歸經 (channels), principal actions. The entry must be readable without opening any other page. This is the rule the user cares most about — do not economize on it.
- **No Typst tables.** The 5-inch page and the site's HTML pipeline both make them a bad fit; use the bulleted per-ingredient blocks.
- **Doses**: give both classical proportions (as the source states them) and modern clinical grams, and flag that modern ranges are reference figures needing verification.
- **Preparation method is substantive**, not a footnote: decoction vs. powder vs. pill, water volume and reduction, order of addition, any pre- or post-decocted ingredient, dose, timing, course length, and how modern granules/patents differ.
- **Processing forms are part of the composition** — 炙甘草 (honey-fried licorice) is not 甘草, and saying so is required.
- **No four-tradition comparative frame.** A Chinese formula is a Chinese artifact; do not manufacture Ayurvedic or Tibb readings. Cross-system parallels go in a short closing note, marked as comparison.
- **Footnote every claim at its point of assertion** with `#footnote[...]`, and keep the end-of-entry **Sources** bibliography.
- **Cite specific texts/editions**; do not fabricate page numbers. Flag contested attributions.
- **Formula-level modern evidence is usually thin** — report what was studied *as the formula*, and do not import the constituent herbs' literature as if it were evidence for the compound.

## Step 4 — Update the glossary (mandatory, same change)

Every foreign-language technical term newly used that is not already in `materia-medica/zz-glossary.typ` MUST be added there in this same change. Formula entries introduce these in volume: role terms (君臣佐使), formula names, pattern names, preparation verbs, dose units. Follow the glossary's per-tradition organization and per-term format. If a needed climate/Tibb concept is missing from `climates.typ` / `tibb-al-arabi.typ`, add it there first, then cite it.

## Step 5 — Build and verify

```sh
make materia-medica      # PDF → out/materia-medica.pdf
make site                # website → out/site/ (verify the Formulas group appears)
```

**Pre-build check (run first — it catches most failures before compiling).** Scan the new file for lines with an odd number of unescaped `*` (unbalanced bold) and for mismatched emphasis:

```sh
f=materia-medica/formulas/<slug>.typ
awk '{ l=$0; gsub(/\\\*/,"",l); n=gsub(/\*/,"*",l); if (n%2==1) print FILENAME":"NR": ("n")" }' "$f"
awk '{ l=$0; gsub(/\\_/,"",l);  n=gsub(/_/,"_",l);  if (n%2==1) print FILENAME":"NR": ("n")" }' "$f"
grep -n '\*/\|/\*' "$f"
```

**Known Typst gotchas (each has caused a failed build in practice):**
- **`*/` adjacency** — a bold span immediately followed by a slash (`*白朮*/茯苓`) parses as a block-comment close. Put a space or a word between them. Grep for `\*/` and `/\*`.
- **Mixed delimiters** — opening with `*` and closing with `_` (or vice versa) on the same span. The two awk checks above catch this; it is the single most common error in practice, and especially easy in ingredient lines that mix bold terms with italic Latin binomials.
- **Missing closing `*` in a long bold-item list** — ingredient rosters and dose lists are exactly where this happens; the odd-`*` check catches it.
- **Reconstruction asterisk** — escape a leading etymological `*` as `\*`.
- Also watch: unescaped `#`/`@` at line start, unbalanced `#footnote[...]` brackets, and stray `_`/`*`.

## Step 6 — Maintenance

If a non-trivial decision was made (template change, new convention, tooling), update `log.md`, and `CLAUDE.md` / `materia-medica/formulas/CLAUDE.md` per the repo's Maintenance Rules.

**Do not commit.** Leave git staging and committing to the user.
