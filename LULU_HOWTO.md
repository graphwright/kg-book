# How to submit to Lulu.com

The book came back and while it looks good, it still needs work. I want to give it an index and references. (Do references come after the index or before?)

---

**Cursor**


Here’s what I found:

## Lulu instructions

**What’s there:** The Makefile has Lulu-related setup:

- 6×9 geometry and margins
- Interior PDF build (no cover, xelatex)
- Separate cover PDF for Lulu upload

**What’s missing:** There’s no step-by-step “how to submit to Lulu.com” guide. Nothing about:

- Upload workflow
- Trim size / binding options
- Account or project setup
- Interior vs. cover upload steps
- Print specs (bleed, etc.)

So the build targets are there, but the submission process itself is not documented.

---

## Index vs. references order

**References come before the index.**

Typical back-matter order:

1. Appendix (if any)
2. Notes (if any)
3. **References / Bibliography**
4. **Index** (last)

The index is almost always last so readers can look up terms after reading and after checking sources.

---

## Index and references in your setup

The Makefile uses `--toc` but no index or bibliography. To add them with Pandoc:

- **Index:** needs `makeindex` or `xindy` and LaTeX index commands in the template.
- **References:** needs a `.bib` file and `--citeproc` (or biblatex/natbib) in the Pandoc command.

I can help draft Lulu submission instructions or outline how to add index and bibliography to the Makefile when you’re ready.

---

**User**

If I'm starting with Markdown, how do I notate "this goes in the index" and "this should be a reference"?

---

**Cursor**


With Pandoc and Markdown, you can do it like this:

## Index entries

Pandoc doesn’t have built‑in index syntax, so you use raw LaTeX:

```markdown
Knowledge graphs are useful for extraction.
```

With an index entry:

```markdown
Knowledge graphs are useful for extraction.\index{knowledge graph}
```

Or inline:

```markdown
A \index{knowledge graph} is a structure of nodes and edges.
```

Subentries:

```markdown
\index{extraction!LLM-based}
\index{provenance!trust signal}
```

To keep LaTeX in the output, use:

```bash
pandoc ... -f markdown+raw_tex
```

(or `-f markdown-native_divs+raw_tex` if you use divs). Then run `makeindex` (or `xindy`) on the generated `.idx` file when producing PDF.

---

## References (citations)

Pandoc supports citations directly in Markdown:

```markdown
As Minsky argued, frames are the direct ancestors of the knowledge graph [@minsky1975].
```

Or with a page number:

```markdown
Semantic networks date to Quillian [@quillian1968, p. 410].
```

You need:

1. A `.bib` file, e.g. `references.bib`:

   ```bibtex
   @techreport{minsky1974framework,
     author      = {Minsky, Marvin},
     title       = {A Framework for Representing Knowledge},
     institution = {Massachusetts Institute of Technology},
     address     = {Cambridge, MA, USA},
     year        = {1974},
     number      = {AIM-306}
   }
   ```

2. In your Pandoc command:

   ```bash
   pandoc outline.md --citeproc --bibliography=references.bib -o outline.pdf ...
   ```

The bibliography is generated from the `.bib` file and placed before the index.

---

## Summary

| What        | Syntax                          | Requires                          |
|------------|----------------------------------|-----------------------------------|
| Index entry | `\index{term}` or `\index{term!sub}` | `+raw_tex`, `makeindex`/`xindy`   |
| Citation   | `[@key]` or `[@key, p. 42]`      | `.bib` file, `--citeproc`         |
