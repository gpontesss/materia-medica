# CLAUDE.md — Materia Medica Project

This file defines how to help with my personal materia medica. Follow these rules on every entry unless I explicitly override them in a given message.

## Scope of this file

**This file governs substance entries** — `materia-medica/substances/*.typ` and the two foundational reference entries. **Formula entries have their own authoritative spec at [`materia-medica/formulas/CLAUDE.md`](formulas/CLAUDE.md)**, which inherits this file's rules on honesty & sourcing, the glossary, footnote format, and tone, but replaces the 8-section template with a formula-specific one. Use the `formula-entry` skill for those.

## File structure

```
materia-medica/
  substances/            ← substance entries live here (one file per substance)
    wheat.typ
    milk.typ
    licorice-root.typ
  formulas/              ← formula entries (see formulas/CLAUDE.md)
    CLAUDE.md
    four-gentlemen-decoction.typ
  climates.typ           ← foundational reference (climate frameworks & world climate taxonomy)
  tibb-al-arabi.typ      ← foundational reference (Greco-Arabic medical framework)
  CLAUDE.md              ← this file
  zz-glossary.typ        ← back-matter glossary; zz- prefix lands it last
materia-medica.typ       ← root document (at repo root, NOT inside materia-medica/)
```

The book assembles these as four ordered groups — foundational references, substances, formulas, glossary — with section dividers between the latter two. New files in `substances/` or `formulas/` are picked up automatically by the Makefile's globs; no registration needed. Slugs share one flat namespace across both folders, because the website generates one `<slug>.html` per entry.

**`climates.typ` is a *foundational reference* entry, not a substance entry**: it sets out the Ayurvedic / 中醫 / Greco-Roman / Tibetan climate frameworks and catalogues the world's climate types in those terms. All substance entries' *Climate, Constitution & Regional Diet* sections cite and apply it rather than restating the framework. See the *Climate rule* below.

**Root document** (`materia-medica.typ`, at repo root): sets page size (5×8 in), margins, EB Garamond + Noto Serif Devanagari font stack, a two-column outline on page 1, then `#include`s the entry files. They arrive at compile time as **four ordered groups** — `sys.inputs.reference`, `substances`, `formulas`, `glossary` — built by the Makefile's globs, with centered *Substance Entries* and *Formulas* divider pages emitted between the groups. New entries are picked up automatically; just put the file in the right folder.

**Entry files** (`materia-medica/<slug>.typ`): one file per substance, named by a short lowercase hyphenated slug (e.g. `licorice-root.typ`, `wheat.typ`). No frontmatter, no `#import` needed — each file starts directly with the top-level heading and flows through the standard template sections using Typst headings (`=`, `==`). Footnotes use `#footnote[...]` inline.

A minimal new entry stub looks like:

```typ
= Substance Name

== Nomenclature & Etymology

== Classical Chinese Medicine (中醫) View

== Ayurvedic Dravyaguna (द्रव्यगुण)

=== Viruddha (Incompatibilities)

== Classical Formulas & Preparations

=== Chinese Medicine

=== Ayurveda

=== Western / Greco-Roman

== Modern Nutrition & Pharmacology

== Sources
```

## Project overview

A personal comparative materia medica of foods and medicinals, synthesizing three systems plus modern science:

1. **Classical Chinese Medicine (中醫)** — properties, channels, actions, formulas.
2. **Ayurvedic dravyaguna (द्रव्यगुण)** — rasa, guṇa, vīrya, vipāka, prabhāva, doṣa effect, karma, viruddha.
3. **Western / Greco-Roman medicine** — historical use, galenic preparations, modern survivals.
4. **Modern nutrition & pharmacology** — composition, mechanisms, dosage/safety.

The guiding principle: engage each system **on its own terms** — internal coherence, classical sources, precise technical vocabulary — then note cross-system convergences and divergences honestly. I am doing serious, scholarly work, not casual lookup. Match that register.

## Languages and naming (required for every entry)

Always give, where they exist:

- **Latin** — binomial + family + the drug/pharmacy name; with **etymology**.
- **English** — common name(s); with **etymology**.
- **Chinese** — name in **characters + pinyin transliteration**; note distinct drug-forms where the tradition treats them as separate drugs (e.g. 生薑 fresh vs. 乾薑 dried ginger; 小麥 vs. 浮小麥).
- **Sanskrit** — name in **Devanāgarī + IAST transliteration**; note distinct forms (e.g. ārdraka vs. śuṇṭhī).

For etymology, cite the actual lexicographic sources (Monier-Williams, Liddell & Scott, Lewis & Short, de Vaan, OED, Watkins/Indo-European roots) — **not** the medical texts. Flag folk etymologies as folk etymologies (e.g. godhūma = "cow-smoke" is folk, true origin uncertain).

## Standard entry template (in this order)

1. **Nomenclature & Etymology** — the four languages above, with etymology and notes on distinct named forms. *For substances classical in Tibb (Greco-Arabic medicine), add the Arabic name in script + transliteration here; Persian and Urdu/Hakeemi as relevant.*
2. **Classical Chinese Medicine (中醫) View** — Property (性/氣), Flavor (味), Channels (歸經), Actions & indications, Cautions.
3. **Ayurvedic Dravyaguna (द्रव्यगुण)** — Rasa, Guṇa, Vīrya, Vipāka, **Prabhāva**, Doṣa effect, Karma, then **Viruddha** as a subsection.
4. **Traditional Arabic & Islamic Medicine (Ṭibb al-ʿArabī wa-l-Islāmī / Unani Tibb)** — *Mizāj* (temperament: Hot/Cold + Dry/Moist, with *darajāt* degree 1–4 where the source texts give it), *Af'āl* (actions), *Istemālāt* (indications), *Mawāne'* / *Iḥtirāzāt* (contraindications and cautions), *Muṣliḥ* (corrective/adjuvant), *Badal* (substitute) where named, and *Tibb al-Nabawī* (Prophetic medicine) attestation where the substance has Qur'ānic or hadith provenance. See the **Tibb rule** below for the full specification.
5. **Classical Formulas & Preparations** — split into four labelled sub-parts: Chinese medicine, Ayurveda, Western/Greco-Roman, Tibb (Arabic-Islamic) — named formulas, classical preparations, modern survivals.
6. **Climate, Constitution & Regional Diet** — for each major climatic zone where the substance is traditionally cultivated or consumed, give the climate type, the dravyaguna/_doṣa_ + 中醫/_liù yín_ + Tibb _mizāj_ reading, the traditional preparation(s) of that zone, and the climate-appropriate *cares*. Close with a *Modern transposition* (_deśa-viruddha_) paragraph. See the **Climate rule** below for the full specification.
7. **Modern Nutrition & Pharmacology** — composition (with per-100g or per-serving basis stated), key constituents, pharmacology of note, and **Safe daily dosage / upper limit**.
8. **Sources** — full bibliography at the end.

Sections that genuinely don't apply (e.g. no Western tradition for a purely Asian item) should be marked as such, not padded.

## Prabhāva rule

Always include prabhāva in the Ayurvedic section. Prabhāva = the specific action **not** predictable from rasa-guṇa-vīrya-vipāka. If the classical texts assign **no** distinct prabhāva (because the actions follow from the standard parameters), **say so explicitly** rather than inventing one. Where a prabhāva-level reading is interpretive/commentarial/modern rather than stated in the canon, flag it as interpretive.

## Viruddha rule

List all recorded incompatibilities in the Ayurvedic section, **tagged by source tier**:

- **(S)** = core saṃhitā (Caraka, Suśruta, Aṣṭāṅga Hṛdaya) — highest authority.
- **(N)** = later nighaṇṭu / commentarial.
- **(F)** = folk / regional.
- **(M)** = modern / pharmacological (a *de facto* incompatibility, e.g. an herb-drug interaction or a clinical contraindication like gluten in celiac disease) — explicitly flagged as non-classical.

Cover both named combination (saṃyoga) incompatibilities and the relevant conditional categories (doṣa, kāla, mātrā, krama, saṃskāra, avasthā, etc.) where the texts specify them. Note where sources disagree.

## Tibb rule

Always include a **Traditional Arabic & Islamic Medicine (Ṭibb al-ʿArabī wa-l-Islāmī / Unani Tibb)** section as item 4 of the standard template. This covers the *Greco-Arabic medical tradition* — the synthesis of Hippocratic-Galenic humoral medicine with Persian, Indian, and indigenous Arabic medicine that flowered from the 8th–13th c. in the Abbasid, Andalusian, and Persian medical schools, was preserved continuously in *Unani Tibb* in South Asia (still regulated under AYUSH in India), in *Ṭibb-e Sonnati* in Iran, and in Maghrebi and Levantine folk medicine — and includes the related but distinct **Ṭibb al-Nabawī** (Prophetic medicine) layer drawing on Qur'ān and hadith.

**Foundational reference entry.** `materia-medica/tibb-al-arabi.typ` is the foundational frame for *all* substance-entry Tibb sections: it sets out the humoral framework (the four humors *akhlāṭ* — *dam*, *balgham*, *ṣafrā'*, *sawdā'* — and the four primary qualities with degree-grading *darajāt*), the *mizāj* (temperament) system, the *asbāb sittah* (six necessary causes), and the major source texts. Substance entries **cite this entry and apply the framework** — they do not re-derive the canonical frame.

**Canonical frame (summary, for quick reference — see `tibb-al-arabi.typ` for full treatment).** The principal medieval Arabic-Islamic pharmacological texts: Ibn Sīnā (*Avicenna*, d. 1037), *al-Qānūn fī al-Ṭibb* Book II (*al-Adwiya al-Mufrada*, simple drugs); Abū Bakr al-Rāzī (*Rhazes*, d. 925), *Kitāb al-Ḥāwī*; Ibn al-Bayṭār (d. 1248), *Kitāb al-Jāmi' li-Mufradāt al-Adwiya wa-l-Aghdhiya* (the great Maghrebi-Andalusian pharmacopoeia, ~1400 simples); al-Zahrāwī (*Albucasis*, d. ~1013), *al-Taṣrīf*; Da'ūd al-Anṭākī (d. 1599), *Tadhkirat ūlī al-albāb*. Unani Tibb in South Asia: Hakim Akbar Arzani, *Tibb-e Akbarī*; Hakim Mohammad Kabīruddīn, *Bayāz-e Kabīr*; Hakim Najmul Ghani Khan, *Khazāyin al-Adwiya*. Prophetic medicine: Ibn Qayyim al-Jawziyya, *al-Ṭibb al-Nabawī*; al-Suyūṭī, *al-Manhaj al-Sawī*.

**Per-substance structure.** Give:
- **Arabic name** in script + transliteration; **Persian** name where distinct; **Urdu/Hakeemi** name where distinct.
- **Mizāj (temperament)** — *Hot/Cold + Dry/Moist*, with *darajāt* (degree 1–4) where the classical text gives it. E.g. honey: *Hot and Dry in the 2nd degree* per Avicenna.
- **Af'āl (actions)** — the canonical Tibb actions: e.g. *mufattiḥ* (deobstruent), *muḥallil* (resolvent), *muqawwī* (tonic), *mulayyin* (laxative), *muḥarrik al-rūḥ* (mood-elevating).
- **Istemālāt (indications)** — humoral disease categories: e.g. *amrāḍ al-balgham* (phlegmatic diseases), *amrāḍ al-mafāṣil* (joint diseases), etc.
- **Mawāne' / Iḥtirāzāt (contraindications)** — *mizāj*-mismatch cautions; for hot-mizāj drugs, the *ṣafrāwī* (bilious / Pitta-equivalent) and hot-pattern conditions; for cold-mizāj drugs, the converse.
- **Muṣliḥ (corrective adjuvant)** — the substance traditionally paired to correct a drug's adverse property; classical Unani practice gives specific pairings (e.g. *muṣliḥ* of honey is a small amount of vinegar; *muṣliḥ* of ghee is honey).
- **Badal (substitute)** — the classical alternative drug used where the principal is unavailable.
- **Ṭibb al-Nabawī attestation** — for substances mentioned in the Qur'ān (e.g. honey 16:69; olive oil 24:35; figs 95:1; pomegranate 6:99; dates 19:25) or in the canonical hadith collections (e.g. black seed; senna; mistletoe; vinegar; truffle for the eyes; talbīna barley-broth), cite the text and traditional commentary.
- **Classical Tibb formulas** — *Murakkabāt* (compound preparations) where the substance is canonical: e.g. *Ma'jūn* class (electuaries); *Sharbat* class (syrups); *Sufūf* (powders); *Anushdārū*; *Itrīfal* (Persian/Unani triphala-equivalent compounds — though the Indian triphala is itself in Unani usage as *Itrīfal*).

**Scope honesty.** Where the substance is canonical in Tibb (most Mediterranean / Persian / South-Asian-shared substances — honey, olives, dates, figs, dairy, barley, wheat, ginger, fennel, cumin, coriander, anise, cinnamon, jasmine, rose, licorice, asafoetida, basmati, mung, lentils, almonds, citrus), give substantive treatment with specific source citation. Where the substance is *not* classical in Tibb (most New World substances — açaí, guaraná, rapadura; most East Asian items — adzuki, pu-erh tea, Japanese fish traditions; indigenous-American items), say *that*, briefly, and treat the modern Unani extension (if any) as reasoned post-classical placement on the humoral axis.

**Sourcing.** Tibb claims should cite specific classical text + chapter + reasonable modern edition: Ibn Sīnā, *al-Qānūn* (the standard 5-volume Arabic edition published by Dar al-Kutub al-'Ilmiyya, Beirut; or the partial Latin Gruner translation); Ibn al-Bayṭār, *al-Jāmi'* (Cairo Bulaq edition or modern reprints; partial Leclerc French translation); modern Unani: AYUSH Ministry of India, *National Formulary of Unani Medicine*; Central Council for Research in Unani Medicine (CCRUM) publications.

## Dosage rule

Always include a "Safe daily dosage / upper limit" line in the modern pharmacology section. The *type* of figure varies honestly by food:

- **Whole foods** — usually no toxicological ceiling; give the meaningful practical figure instead (a limiting component like mercury, iodine, sodium; or dietary-pattern guidance, clearly marked as not a safety threshold).
- **Medicinals / potent spices** — give an actual therapeutic-dose and/or upper-limit figure, **naming the limiting compound** (e.g. glycyrrhizin for licorice, caffeine/EGCG for tea, antiplatelet effect for ginger).

Always tag dosage figures as reference thresholds needing current verification, and note relevant risk groups. This is reference information, **not personalized medical advice** — say so, and point genuinely high-risk items (real dose-dependent toxicity) toward clinician consultation.

## Climate rule

Always include a **Climate, Constitution & Regional Diet** section. The classical-formulas section catalogues *what* preparations exist; the climate section makes the *why* — climate ↔ constitution ↔ preparation — explicit, and exposes mismatches in modern globalized eating.

**Foundational reference entry.** `materia-medica/climates.typ` is the foundational frame for *all* substance-entry climate sections: it sets out the canonical Ayurvedic _ṛtucaryā_ + _deśa_, Chinese 五運六氣 + 六淫 + 五方, Greco-Roman humoral, and Tibetan Sowa Rigpa frameworks; defines the world climate-type taxonomy; and discusses cross-system convergences and divergences. Substance entries **cite this entry and apply the framework** — they do not re-derive the canonical frame, and they treat only the climates relevant to their own cultivation/consumption. If a needed concept is missing from `climates.typ`, *add it there first* and only then cite it from the substance entry.

**Canonical frame (summary, for quick reference — see `climates.typ` for full treatment).** Caraka Sūtrasthāna 6 and Aṣṭāṅga Hṛdaya Sūtrasthāna 3 (_ṛtucaryā_, seasonal regimen) and Caraka Vimānasthāna 3 + Sūtrasthāna 25 (_deśa_: _jāṅgala_/_sādhāraṇa_/_ānūpa_) for the Ayurvedic side; _Huang Di Nei Jing_, _Su Wen_ chs. 2 (_si qi tiao shen da lun_ 四氣調神大論), 5 (_yin yang ying xiang da lun_ 陰陽應象大論, the 五方 table), 12 (_yi fa fang yi lun_ 異法方宜論, regional therapeutics), and 66–74 (_wu yun liu qi_ 五運六氣) for the Chinese side; the 六淫 six external excesses (風寒暑濕燥火) with their organ-correspondences (風→Liver, 寒→Kidney, 暑→Heart, 濕→Spleen, 燥→Lung, 火→Heart/Pericardium); Hippocrates' _De aëre, aquis, locis_ and Galen's _De temperamentis_ for the Greco-Roman humoral side.

**Organize by climate zone, not by region.** Same climate type can span continents (warm-dry Mediterranean ↔ Levantine ↔ North African; cool-damp Atlantic ↔ Baltic ↔ Pacific Northwest). Zoning by climate makes the constitutional logic transparent; the standard taxonomy:

- **Warm-dry** (Mediterranean, Middle Eastern, North African) — Pitta-aggravating; external 燥 + 熱; Lung/Liver loaded; corrective: cooling, moisture-retaining, long-decocted preparations, dairy/yogurt accompaniments, sour-cool flavors.
- **Cold-dry, high-altitude** (Tibetan, Himalayan, Central Asian) — extreme Vāta; external 寒 + 風; Kidney-yang loaded; corrective: roasting (_agnisaṃskāra_), heavy snigdha fats (butter), salt, warming drinks (tea).
- **Cool-damp** (Atlantic North European, Baltic, Pacific Northwest) — Vāta-Kapha; external 寒濕; Spleen-yang loaded; corrective: long-cooked, salted, with warming root vegetables/spices; fermentation as _saṃskāra_ inversion (raw-cool → finished-warm: beer, whisky, kvass).
- **Continental-extreme** (Germanic, Slavic, Russian) — seasonal swing across the year; *summer* forms (kvass-type cooling ferments) and *winter* forms (porridge with dairy fat) are *both* climatically apt — eating the wrong form for the season is _kāla-viruddha_.
- **Hot-humid** (South/Southeast Asian monsoonal, sub-Saharan, Caribbean) — Pitta-Kapha; external 濕熱; Spleen + Heart loaded; corrective: light, bitter-pungent, drying, with carminative spices and fermented sour foods; avoid heavy snigdha preparations except in cool/dry season.

**Per-zone structure.** For each zone treated: (a) name the climate type, (b) give the dravyaguna/_doṣa_ reading (which doṣa is aggravated, which _ṛtu_/season carries the load) *and* the 中醫 reading (which 六淫 is in play, which organ is loaded), (c) name the traditional preparation(s) of that zone, (d) state the *cares* — what preparation parameters (salt vs. sugar, hot vs. cold, fat vs. dry, fermented vs. fresh) are constitutive, not optional, and *why* in classical terms.

**Mandatory closing paragraph.** End the section with a *Modern transposition (_deśa-viruddha_)* paragraph: name the globalized cross-climate preparation mismatch (e.g. cold overnight oats in cool-damp climates; hot tsampa in tropics), and cite Caraka Sū. 26 _viruddha_ for the _deśa-viruddha_ category. Use _kāla-viruddha_ in parallel for the seasonal-shift category.

**Scope honesty.** If a substance has only one traditional climate (oats: cool-damp only), say so plainly and treat its introduction into non-traditional climates as post-classical extension — flagged. If a substance is genuinely pan-climatic (rice, milk), treat all the relevant zones. If the substance is too geographically narrow for the section to add anything (e.g. a substance grown and consumed in a single ecological niche), say *that*, briefly, and don't pad.

**Sourcing.** Climatic-medical claims should cite classical text + chapter (Caraka Sū. 6, _Su Wen_ ch. 2, _rGyud bzhi_ dietetic chapters, etc.). Regional preparation claims may cite reputable food-history secondary literature (Roden, McNeill, Davidson's _Oxford Companion to Food_, Notaker, Pokhlebkin, etc.) — but flag where a dravyaguna or 中醫 reading of a preparation is interpretive-by-extension rather than classical-by-citation.

## Glossary rule

`materia-medica/zz-glossary.typ` is the **back-matter glossary** that defines every foreign-language technical term used anywhere in the book. The file is named with a `zz-` prefix so it lands last under the Makefile's alphabetical `sort -u` ordering. It is organized as **one section per major tradition** (Classical Chinese Medicine; Ayurvedic Dravyaguna; Traditional Arabic & Islamic Medicine / Tibb; Greco-Roman & Hippocratic-Galenic; Japanese Tradition; Brazilian / Portuguese / Indigenous Amazonian; Persian — with the last being mostly cross-referenced to Tibb), plus a cross-tradition concordance for terms that span systems.

**The glossary is the single source of truth for foreign-term definitions.** Substance entries may briefly gloss a term inline on first use, but the canonical definition lives in the glossary; readers consult the glossary for terms not glossed in context, and authors maintain it as the controlled vocabulary of the project.

**Mandatory update rule.** Every time a substance entry uses a foreign-language technical term (Chinese, Sanskrit, Arabic, Persian, Greek, Latin, Japanese, Portuguese, indigenous-Amazonian, etc.) that is not already in the glossary, the term **must** be added to the glossary in the same change. *No exceptions.* This applies to: drug-form names, action-vocabulary words, anatomical / physiological terms, formula-class names, named diseases, classical-source titles, regional preparation names, ritual / cultural terms. If a term recurs across multiple entries with the same meaning, define it once in the glossary and cite the glossary by referring to it in subsequent entries.

**Per-term format.** Each glossary entry should give: (a) the term in its native script where applicable, (b) the transliteration (pinyin / IAST / Arabic-script Romanization), (c) a literal-translation or etymological gloss in parentheses where useful, (d) a one-to-two-sentence definition, (e) a note on the source-tradition register (classical / late-classical / modern / regional / disputed) where relevant, (f) cross-references to the most-relevant substance entries (e.g. "see _ginger.typ_ for the canonical drug-form distinction") or to other glossary terms with `→` or "cf."

**Organization within each tradition section.** Group thematically — *fundamentals* (Yin-Yang / 五行 / dośa / mizāj), *pharmacological framework* (rasa-guṇa-vīrya-vipāka / 性味歸經 / mizāj-degrees), *action vocabulary* (清熱解毒 / dīpana-pācana / mufattiḥ-muḥallil), *drug-form vocabulary* (生薑/乾薑 / cūrṇa / sufūf), *anatomical-physiological terms* (āma-ojas / akhlāṭ / 三焦), *formula classes* (湯/丸 / ariṣṭa / maʿjūn), *named-disease vocabulary*, *classical-source titles*. Alphabetize within each thematic group.

**Cross-system concordance.** End the glossary with a brief concordance table mapping convergent concepts across traditions (e.g. *cooling-and-moistening*: 涼潤 / śīta-snigdha vīrya / Cold-and-Moist mizāj / cool-and-moist humoral; *aphrodisiac / virilifying*: 補陽 / vājīkara / muḥarrik al-bāh; *deobstruent / channel-opening*: 通利 / srotośodhana / mufattiḥ). This makes cross-system convergences visible at a glance.

**Sourcing.** Glossary definitions should cite the canonical source-text where the term is foundational (e.g. *prabhāva* → Caraka Sūtra 26.67–72; *darajāt* → Avicenna, _Qānūn_ II; *五行* → _Su Wen_ ch. 5). Cite `tibb-al-arabi.typ` and `climates.typ` where they treat the term substantively; the glossary is the *summary*, those entries are the *full treatment*.

## Honesty and sourcing standards (important)

- **Cite the specific text/edition** each claim traditionally derives from. I work from classical sources; name them (with translator/edition where relevant).
- I cannot verify live page numbers — name the work, section, and edition; don't fabricate precise citations.
- **Distinguish *citing* a tradition from *applying* it.** Some foods have a genuine classical entry (milk, ginger, wheat, licorice); some can only be analyzed *by* the system's principles because they postdate or fall outside the canon (tea, and New-World foods like potato, tomato, chili). For the latter, **mark the section "reasoned analysis, not classical"** and don't dress reasoned extension as canonical authority.
- Flag when a "type" postdates the source texts (e.g. oolong postdates the 1578 Bencao Gangmu; its placement is on the classical oxidation→temperature axis, not a dedicated classical entry).
- **Prefer classical, book-based primary sources** over web aggregators, especially for the traditional systems. Modern pharmacology should point to current literature (PubMed reviews, EFSA/JECFA, USDA FoodData Central) and be flagged for verification, since that field moves.
- Note cross-system **convergences** (e.g. licorice's sweet-root naming + 中滿/śotha caution = the 11β-HSD2 mechanism; gingerol→shogaol = the fresh/dried doctrine) **and divergences** (e.g. wheat cooling in Asia but warming-moistening in Greco-Roman humoral theory). Don't smooth divergences over.
- Don't overstate modern health claims; popular sources frequently exaggerate (green tea EGCG, oolong weight loss). Mark evidence as modest where it is.

## Output format

- **Footnote every source with `#footnote[...]` anchored at the point of claim**, not only in a list at the end. Keep the end-of-entry **Sources** bibliography as well (footnotes and bibliography serve different purposes).
- Anchor footnotes at the end of the relevant claim or block (not after every sentence) to keep markup readable and numbering clean.
- In footnotes, state when a claim is interpretive, modern, lower-tier, or postdates the source texts.

## Tone and conventions

- Scholarly, precise, direct. Assume fluency in both systems; don't over-explain basics I clearly know.
- Lead with a brief scope/referent note when a term is ambiguous across systems (e.g. "yogurt" = dadhi; matcha is Japanese not Chinese; trikatu is a formula not a food).
- It's fine — encouraged — to flag uncertainty, contested points, and where I'd want to verify against a specific edition.
- Use my established sweetener/sourcing preferences and personal context only when relevant to a given entry; otherwise keep entries general.

## Standing offers / open conventions

- "Classical Formulas & Preparations" is now a permanent template section (added after the licorice/wheat entries).
- "Climate, Constitution & Regional Diet" is now a permanent template section (added after the barley/oats entries). Organize by climate zone, not by region; use _deśa-viruddha_ as the closing modern-transposition category and _kāla-viruddha_ for seasonal-shift cases.
- "Traditional Arabic & Islamic Medicine (Ṭibb al-ʿArabī wa-l-Islāmī / Unani Tibb)" is now a permanent template section (added after the jasmine entries). Cite `tibb-al-arabi.typ` and apply its framework. Mark substances absent from the Greco-Arabic canon explicitly. Include the Ṭibb al-Nabawī (Prophetic medicine) layer where the substance has Qur'ānic/hadith attestation.
- The back-matter glossary `zz-glossary.typ` is the controlled vocabulary of the project. Every foreign-language technical term used in any entry must be defined in the glossary. The `zz-` prefix lands it last in the Makefile's alphabetical file-ordering. See the **Glossary rule** for the per-term format and the mandatory-update protocol.
- "Relation to parent food" one-liner for derivatives (curd ← milk; ghee ← butter ← curd) when relevant.
- An "Ayurvedic status: classical / reasoned-only" header flag distinguishes canonical from imported foods.
