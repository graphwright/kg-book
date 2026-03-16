IMAGES := $(wildcard *.png *.jpg *.jpeg *.svg)
PANDOC := pandoc
SRC := outline.md

# Lulu interior geometry: 6x9, inner margin slightly wider for binding
GEOMETRY := paperwidth=6in,paperheight=9in,top=0.75in,bottom=0.75in,inner=0.875in,outer=0.625in

all: outline.epub outline.pdf cover.pdf

clean:
	rm -f outline.epub outline.pdf outline.tex outline.aux outline.idx outline.ind outline.ilg outline.log outline.out cover.pdf

# epub still uses cover-image from YAML frontmatter
outline.epub: $(SRC) $(IMAGES)
	$(PANDOC) $(SRC) -o $@

# Interior PDF for Lulu — no cover, xelatex for font embedding
# Two-step: pandoc → LaTeX, then xelatex + makeindex + xelatex (makeindex needs a separate pass)
outline.pdf: outline.tex $(IMAGES)
	xelatex -interaction=nonstopmode outline.tex || true
	-makeindex -s index.ist outline
	xelatex -interaction=nonstopmode outline.tex
	xelatex -interaction=nonstopmode outline.tex

outline.tex: $(SRC) index-header.tex index-footer.tex
	$(PANDOC) $(SRC) \
	  -f markdown+raw_tex \
	  --top-level-division=part \
	  --toc \
	  -V documentclass=book \
	  -V fontsize=11pt \
	  -V classoption=openright \
	  -V geometry:"$(GEOMETRY)" \
	  --include-in-header=index-header.tex \
	  --include-after-body=index-footer.tex \
	  --citeproc \
	  --bibliography=references.bib \
	  --metadata cover-image= \
	  -o $@

# Separate cover PDF for Lulu upload (they want it as a standalone PDF)
cover.pdf: Cover6x9.png
	convert Cover6x9.png \
	  -density 300 \
	  -units PixelsPerInch \
	  -compress jpeg \
	  cover.pdf
