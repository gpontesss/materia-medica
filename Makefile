OUTDIR := ./out
FONT_PATH := ./fonts

MATERIA_MEDICA_MAIN := ./materia-medica.typ
MATERIA_MEDICA_ENTRIES := $(wildcard ./materia-medica/*.typ)
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
	@typst compile --font-path $(FONT_PATH) --input "files=$$(echo $(filter-out $<,$^) | sort -u | tr ' ' ',')" \
		$< $@

$(OUTDIR):
	@mkdir -p $@

.PHONY: clean
clean:
	@rm -r $(OUTDIR)
