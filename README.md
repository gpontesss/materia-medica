# Materia Medica

A comparative materia medica of foods and medicinals, synthesizing Classical Chinese Medicine, Ayurvedic dravyaguna, Tibb (Greco-Arabic medicine), and modern nutrition & pharmacology.

Entries are written in [Typst](https://typst.app/) and compiled to a print-ready PDF; the same sources are also published as a searchable website via GitHub Pages (see `site/`).

## Build

```sh
make materia-medica # compile materia-medica.pdf → out/materia-medica.pdf
make site            # generate the website → out/site/
make serve-site       # generate the website and serve it at localhost:8000
```

See `CLAUDE.md` for the full architecture, and `materia-medica/CLAUDE.md` for the entry template and scholarly standards.
