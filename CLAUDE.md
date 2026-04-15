# Book Formatting Conventions

This file documents the formatting practices used in `text.md` and previously in `outline.md`, so they don't need to be re-established in each working session.

---

## Source File

The book text lives in `text.md`. `outline.md` is a chapter-by-chapter bullet-point summary of content, not prose. Do not confuse the two.

## Build

```
make          # builds text.epub, text.pdf, cover.pdf
make clean    # removes all generated files
```

The PDF build pipeline is: `pandoc → text.tex`, then `xelatex` (×2) with `makeindex` between passes. SVG diagrams are pre-converted to PDF via Inkscape.

---

## Markdown Formatting

### Dashes

- Use `--` (double hyphen) for em dashes, not `—` (Unicode em dash) and not `---`.
- Example: `The model doesn't know -- it just guesses.`

### Quotation Marks

- Use straight double quotes `"..."`, not curly/smart quotes `"..."`.
- This applies to both dialogue and technical terms in quotes.

### Italics

- Use `*word*` for emphasis and book/paper titles in running text.
- Example: `*Gödel, Escher, Bach*`, `*Science*`, `*this is the key point*`

### Headings

The book uses pandoc with `--top-level-division=part`:

- `#` → Part
- `##` → Chapter
- `###` → Section (within a chapter)

Chapter headings use title case: `## Chapter 2: A Brief History of Knowledge Representation`

Section headings use sentence case: `### The idea that wouldn't die`

(Exception: section headings that are proper names or established phrases keep their capitalization.)

### YAML Frontmatter

The file begins with YAML frontmatter delimited by `---` / `...` (not `---` / `---`):

```yaml
---
title: Knowledge Graphs from Unstructured Text
author: Will Ware
rights: © 2026 Will Ware, MIT License
language: en-US
description: "A practitioner's guide..."
...
```

---

## LaTeX Inline Markup

Raw LaTeX is passed through pandoc using the `{=latex}` attribute on inline code spans.

### Chapter/section running headers

Every chapter needs a `\chaptermark` immediately after the `##` heading line:

```markdown
## Chapter 6: LLMs Make This Practical Now

`\chaptermark{LLMs Make This Practical Now}`{=latex}
```

For the Foreword (which uses `\markboth` instead):

```markdown
`\markboth{Foreword}{Foreword}`{=latex}
```

Use a shortened title that fits in the running header if the full chapter title is long.

---

## Index Entries

Index entries are placed inline in the text using `\index{...}` inside a raw LaTeX span. Since pandoc processes inline raw LaTeX directly (no `{=latex}` needed for `\index`), they appear as:

```
word\index{entry}
```

or immediately after a name/term without a space:

```
Douglas Hofstadter's\index{Hofstadter, Douglas} argument...
```

### Placement

- Place the `\index{...}` tag immediately after the word or phrase it marks, with no space before it.
- For a person, index at first mention in each chapter. Format: `Lastname, Firstname`.
- For a concept or topic, index at the defining or most significant mention.

### Index entry rules

1. **Do not start an index entry with "The"** -- invert it: `Automation of Science, The (King)` not `The Automation of Science (King)`.

2. **People**: `Lastname, Firstname` -- e.g., `\index{Hofstadter, Douglas}`, `\index{King, Ross}`.

3. **Books and papers**: Use `Title (Author)` format, omitting leading "The" -- e.g., `\index{Automation of Science, The (King)}`, `\index{Elements (Euclid)}`.

4. **Italicized titles in the index** use a sort key to avoid the `@` being treated as a name separator:
   ```
   \index{Godel Escher Bach@\textit{Gödel, Escher, Bach} (Hofstadter)}
   ```
   The part before `@` is the sort key (ASCII, no special chars); the part after `@` is the displayed text.

5. **Subtopics** use `!` separator: `\index{knowledge graph!definition}`, `\index{prompt engineering!schema binding}`.

6. **Cross-references** use `|see{...}`: `\index{RAG|see{retrieval-augmented generation}}`.

7. **Topics with parenthetical qualifiers**: `\index{Adam (robot scientist)}`, `\index{bias (knowledge graph)}`.

---

## Citations

Citations use pandoc-citeproc with BibTeX. Format in text: `[@citekey]` immediately after the title or claim being cited.

```markdown
"What the Frog's Eye Tells the Frog's Brain." [@lettvin1959frog]\index{...}
```

BibTeX entries live in `references.bib`. Entry types in use: `@article`, `@book`, `@phdthesis`, `@techreport`.

BibTeX key convention: `lastnameYYYYkeyword` -- e.g., `hofstadter1979geb`, `king2009automation`.

In BibTeX entries:
- Page ranges use `--` (double hyphen): `pages = {1940--1951}`
- Author names: `Lastname, Firstname and Lastname2, Firstname2`

The References section is generated automatically by pandoc-citeproc and gets its own Part heading and TOC entry via `index-header.tex`.

---

## Images

Images referenced as `![](filename.png)` or `![](filename.pdf)`.

- PNG and JPG images are included directly.
- SVG diagrams must be pre-converted to PDF by `make` (via Inkscape) before xelatex can include them. Reference them as `.pdf` in the markdown: `![](diagram.pdf)`.
- Captions go on the line immediately after the image tag, as plain text (not a separate paragraph).

---

## Code Blocks

Fenced code blocks with no language tag are used for ASCII diagrams and pipeline illustrations:

````
```
Unstructured Text
       |
       v
  Extraction (LLM)
```
````

---

## Document Structure Notes

- The Foreword appears before the Preface and before Part I. It is shared across all three Graphwright series volumes.
- Parts are numbered with Roman numerals in headings: `# Part I: The Landscape`
- Chapters are numbered with Arabic numerals: `## Chapter 1: Why Do We Want to Build Knowledge Graphs?`
- Appendices follow the main chapters: `## Appendix A: ...`
- The Index is appended automatically via `index-footer.tex` (`\printindex`).
- The References section is inserted automatically before the index by pandoc-citeproc.

---

## Lulu Print Specs

The PDF is formatted for Lulu 6×9 interior upload:

- Paper: 6in × 9in
- Margins: top 0.75in, bottom 0.75in, inner 0.875in (binding), outer 0.625in
- Font size: 11pt
- `classoption=openright` (chapters start on right-hand pages)
- Cover is a separate PDF uploaded independently.
