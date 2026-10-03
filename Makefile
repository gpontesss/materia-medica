OUTDIR := ./out
FONT_PATH := ./fonts

MATERIA_MEDICA_MAIN := ./materia-medica.typ

# The book is assembled from four ordered groups, not one flat glob, so each
# becomes its own titled part in the PDF: Substances, Recipes & Formulas,
# Miscellaneous (the foundational framework entries), Glossary. The glossary
# (zz- prefix) lands last, as its name has always been designed to.
MM_SUBSTANCES := $(sort $(wildcard ./materia-medica/substances/*.typ))
MM_FORMULAS := $(sort $(wildcard ./materia-medica/formulas/*.typ))
MM_MISC := ./materia-medica/climates.typ ./materia-medica/tibb-al-arabi.typ
MM_GLOSSARY := ./materia-medica/zz-glossary.typ

MATERIA_MEDICA_ENTRIES := $(MM_SUBSTANCES) $(MM_FORMULAS) $(MM_MISC) $(MM_GLOSSARY)
MATERIA_MEDICA_PDF := $(OUTDIR)/materia-medica.pdf

SITE_DIR := $(OUTDIR)/site

.PHONY: all
all: materia-medica

.PHONY: materia-medica
materia-medica: $(MATERIA_MEDICA_PDF)

.PHONY: site
site: $(MATERIA_MEDICA_ENTRIES) site/build.py site/assets/style.css site/assets/search.js site/assets/nav.js
	@python3 site/build.py --out $(SITE_DIR)

.PHONY: serve-site
serve-site: site
	@python3 -m http.server --directory $(SITE_DIR) 8000

$(MATERIA_MEDICA_PDF): $(MATERIA_MEDICA_MAIN) $(MATERIA_MEDICA_ENTRIES) | $(OUTDIR)
	@typst compile --font-path $(FONT_PATH) \
		--input "substances=$$(echo $(MM_SUBSTANCES) | tr ' ' ',')" \
		--input "formulas=$$(echo $(MM_FORMULAS) | tr ' ' ',')" \
		--input "misc=$$(echo $(MM_MISC) | tr ' ' ',')" \
		--input "glossary=$$(echo $(MM_GLOSSARY) | tr ' ' ',')" \
		$< $@

$(OUTDIR):
	@mkdir -p $@

.PHONY: clean
clean:
	@rm -r $(OUTDIR)
