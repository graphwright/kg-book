## Summary

### Two Tracks

The project documentation is being rebuilt from scratch, with the Python source code as the single source of truth for the technical track. The existing markdown files — scattered across PLANn.md, TODOn.md, STATUS files, and docs/ — are being discarded rather than updated, as they've drifted too far from the current codebase to be worth maintaining.

We *do* need to keep `kgserver/index.md` because it is used as the front page for the KGserver. All other markdown files are to be discarded and replaced.

As stuff is discarded, we look to the Python source files in the `kgraph` repository as the single source of truth for the tech docs, and for the part of the book that is not simply my opinion.

This `kg-book` repository is for the first of the two tracks.

Raw URL for `outline.md`: https://raw.githubusercontent.com/wware/kg-book/main/outline.md

```bash
pandoc outline.md \
    --metadata title="Knowledge Graphs from Unstructured Text" \
    --epub-cover-image=CoverImage.png \
    -o outline.epub
```

---

### Track 1: The Book

**Audience**: Practitioners approaching knowledge graph construction who may or may not follow this specific implementation. The book should be useful even if the reader ends up taking a different path.

**Voice**: Personal and opinionated — grounded in real implementation experience, with first-person texture (including the Framerd anecdote). Willing to discuss alternatives honestly, including classical NLP approaches and cases where you get a knowledge graph "for free" from structured or instrument-generated data. The core thesis is that LLMs make extraction-based KG construction practical in a way no prior technology achieved, but this is argued rather than assumed.

**Target platform**: LeanPub and/or Kindle.

**Cross-referencing policy**: The technical docs reference the book prominently. The book stands alone — if it seems to depend on the tech docs, that's a signal something needs rethinking.

**Structure**:

**Part I: The Landscape**
- Chapter 1: A Brief History of Knowledge Representation — semantic nets, frames, Framerd, expert systems, RDF/OWL, Google's KG, and the extraction bottleneck as the recurring wall
- Chapter 2: The Dream — Star Trek computer, Adam and Eve (Ross King), the cross-disciplinary insight argument, HAL as a philosophical argument about capability entailment (plants a thematic tension that pays off in Part IV), SF romp through Asimov/Hitchhiker's/Gibson
- Chapter 3: What Is a Knowledge Graph, Really? — working definition, nodes/edges/semantics, provenance, canonical identity, what KGs are and aren't good for, build vs. buy
- Chapter 4: The Extraction Problem — classical NLP honestly assessed, the annotation treadmill, why LLMs are a phase transition, what they still don't solve

**Part II: LLMs Change the Equation**
- Chapter 5: Why LLMs Make This Practical Now
- Chapter 6: The Free KG Cases
- Chapter 7: Designing Your Schema

**Part III: Building It**
- Chapter 8: The Ingestion Pipeline
- Chapter 9: Identity and Canonicalization
- Chapter 10: Provenance and Trust
- Chapter 11: Querying and Using Your Graph

**Part IV: What It Means**
- Chapter 12: The Augmented Researcher — cognitive biases, combinatorial scale, linguistic/geographic blind spots, Adam and Eve revisited with full implementation context
- Chapter 13: Who Benefits, Who Decides — democratization, compressed discovery timelines, the rare disease problem, credit and provenance as ethical questions, who owns the graph
- Chapter 14: The Inference You Didn't Intend — HAL revisited in full, dual use at graph scale, bias encoded at scale, the epistemic responsibility of the builder
- Chapter 15: What's Next — open problems, where the field is going, what I'd do differently, an invitation

---

### Track 2: Technical Docs

**Audience**: Both contributors (who need internals and extension points) and domain users (who want to adapt the framework to their own corpus and schema). These are served by the same documents, structured with clear layering.

**Cross-referencing policy**: References the book prominently for motivation and conceptual background.

**Structure**:

1. **Overview** — What this codebase is and the problem it solves. Link to book for motivation.
2. **Architecture** — The major components (kgschema, kgraph, kgbundle, kgserver, examples) and how they relate.
3. **Schema Design Guide** — How to define entities, relationships, and documents using kgschema.
4. **The Pipeline** — Each stage in detail: parsing, chunking, extraction, dedup, resolution, bundle building.
5. **Canonical IDs and Entity Resolution** — How identity works, authority lookups, the synonym cache.
6. **Storage and Export** — In-memory storage, bundle format, query interface.
7. **Adapting to Your Domain** *(first-class chapter)* — Step-by-step: define your schema, write your extraction prompts, configure your pipeline, validate your output.
8. **The medlit Example** — Annotated walkthrough of the reference implementation.
9. **The Sherlock Example** — A simpler/literary contrast case showing the framework's generality.
10. **Deployment and Operations** — kgserver, Docker, MCP integration, running at scale.
11. **`kgserver/index.md`** — The KGserver home page, living at the server's web root, covering what the server exposes, how to connect to it, and how to query a running graph instance.
12. **Contributing** — Internals, extension points, testing approach.
