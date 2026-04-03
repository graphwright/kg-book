# Knowledge Graphs from Unstructured Text — Outline

## Preface

Introduction to LLM hallucination as the motivating problem, knowledge graphs as the solution, and an overview of the book's structure and the `kgraph`/`medlit` example project.

---

## Part I: The Landscape

### Chapter 1: Why Do We Want to Build Knowledge Graphs?

- **Large Language Models Work Great** — LLMs fluently answer questions about well-known facts and achieve high accuracy on familiar domains.
- **Until They Don't** — Hallucination is baked into LLM design; they fail systematically outside their training distribution with no mechanism to signal uncertainty.
- **The Scale of the Problem** — For high-stakes domains (medicine, law, science), hallucination is unacceptable and requires grounded, traceable answers.
- **Retrieval-Augmented Generation or "RAG"** — RAG helps by retrieving passages, but unstructured text requires the model to parse and infer structure every time.
- **Graph RAG** — Giving LLMs a knowledge graph with typed relationships provides explicit structure they can reason over and cite.
- **Why Bother Building One?** — Knowledge graphs offer high ROI, are simple to understand, increasingly buildable with current tools, and naturally support LLM grounding.

### Chapter 2: A Brief History of Knowledge Representation

- **The Idea That Wouldn't Die** — Decades of ambitious projects sought to build machines that understand rather than merely retrieve, but all stumbled on getting knowledge *in*.
- **What the Frog's Eye Tells Us** — Perception and intelligence require structured, selective feature extraction—not passive accumulation of raw data.
- **Semantic Networks and the Frame Problem** — Quillian's semantic networks and Minsky's frames introduced structured relationships and context-dependent knowledge representation as alternatives to flat facts.
- **Meaning is Relational** — Hofstadter's analysis: meaning arises from symbol systems and relationships, not individual symbols; the knowledge graph embodies this principle.
- **The Logic Wars** — Expert systems succeeded on narrow domains but failed to scale; formal logic remained brittle; the field moved to statistical methods.
- **Doug Lenat and Cyc** — Cyc attempted to hand-encode common sense; it demonstrated that the extraction bottleneck, not reasoning capability, is the fundamental limit.
- **The Semantic Web and the RDF Era** — The vision of machine-readable linked data faced adoption barriers; Linked Data emerged as pragmatic but still unable to extract from unstructured text.
- **The Industrial Knowledge Graph** — Google's Knowledge Graph succeeded at scale using curated structured sources; it revealed that extraction from unstructured text remained the unsolved problem.
- **The Extraction Bottleneck** — Every knowledge representation approach in the past 60 years hit the same wall: the cost and difficulty of reliably extracting structured knowledge from natural language prose.
- **The Robot Scientist** — Adam and Eve demonstrated autonomous scientific reasoning over knowledge graphs; they were limited only by the bottleneck of hand-curated domain knowledge.
- **The Cross-Disciplinary Machine** — Cross-domain reasoning requires recognizing identical entities across fields; canonical identity resolution anchored to ontologies enables this.
- **The Gap Is the Book** — The infrastructure now exists to extract knowledge at scale; this book addresses how to build it.

### Chapter 3: What Is a Knowledge Graph, Really?

- **A Working Definition in Four Parts** — Nodes are entities; edges are typed relationships; every entity has canonical identity; every relationship carries provenance.
- **The Semantics Matter** — Typed relationships carry meaning; generic labels like "associated with" are nearly useless; the type is the knowledge.
- **Provenance and the Epistemics of a Fact** — Claims have epistemological status; provenance records source, method, confidence, and evidence type so downstream systems can weight them appropriately.
- **Identity: The Hard Problem** — Canonical identity resolves multiplicity (synonyms, aliases, misspellings) to single nodes and anchors entities to authoritative ontologies.
- **What a KG Is Good For** — Querying (structured answers), traversal (multi-hop reasoning), hypothesis generation (pattern matching), and LLM grounding (explicit sources).
- **Build vs. Buy** — Existing graphs cover some domains; building is necessary for novel domains, proprietary corpora, custom schemas, and full provenance traceability.
- **What a KG Is Not Good For** — Quality reflects sources; coverage gaps create false negatives; maintenance is ongoing; bias encodes and amplifies at scale.

### Chapter 4: Representation Is Reasoning

- **From Fluency to Grounded Reasoning** — LLMs are fluent but ungrounded; explicit structured knowledge enables tracing, correcting, and bounding the reasoning.
- **Experts Have Internal Knowledge Graphs** — Domain experts reason over structured mental models; the graph makes that structure explicit and machine-accessible.
- **Grounded Representation as the Fix** — Giving the model explicit claims to reason from produces fundamentally different behavior than asking it to retrieve from statistical memory.
- **Provenance, Auditability, Trust** — Explicit graphs are inspectable; implicit neural networks are black boxes; auditability is a requirement in high-stakes domains.

### Chapter 5: The Extraction Problem

- **Humans Are Smarter Than You Think** — Scientific text is complex, with hedging, negation, implicit relationships, cross-sentence dependencies, and domain jargon.
- **NLP Was Insufficient to the Task** — Classical NLP made progress on narrow tasks but was brittle on hedging, implicit relationships, long-range dependencies, and domain adaptation.
- **Economics of LLMs for Extraction** — LLMs handle hedging, negation, implicit relationships, and jargon naturally, with the marginal cost of new extraction tasks dropping dramatically.

---

## Part II: LLMs Change the Equation

### Chapter 6: LLMs Make This Practical Now

- **The Economics Argument First** — Classical NLP required months of domain adaptation; LLMs require hours of prompt iteration, opening the technology to smaller organizations.
- **What LLMs Actually Are, For This Purpose** — LLMs are pattern-completion engines with internalized knowledge of domain relationships; the prompt binds that knowledge to a schema.
- **The Prompt as Schema Binding** — Schema in the prompt (not in model weights) enables rapid iteration, collaborative review with domain experts, and version control.
- **Handling What Classical Systems Couldn't** — LLMs handle hedging, negation, implicit relationships, cross-sentence dependencies, and domain jargon far better than classical systems.
- **The Remaining Limitations, Honestly** — Hallucination occurs; context windows are finite; cost accumulates; non-determinism complicates reproducibility; LLMs reflect their training distribution.
- **Why This Moment** — Model capability (GPT-4 threshold), API accessibility, and tooling ecosystem all matured simultaneously around 2023–present.

### Chapter 7: The Free KG Cases

- **When You Don't Need Extraction** — Structured sources (databases, APIs, equipment) don't require extraction; integration and schema mapping suffice.
- **Lab Instruments and Measured Data** — Genomics produces structured data; graphs like STRING are high-precision over their narrow coverage but miss the literature.
- **Generated and Synthetic Graphs** — Ontologies and databases provide high-precision relationships but only cover what was explicitly encoded.
- **Curated Graphs at Scale** — Wikidata and encyclopedias achieve breadth through human curation but cannot scale to full literature in technical domains.
- **What These Cases Teach Us** — Structured sources set the quality benchmark; extraction targets that benchmark for knowledge not yet structured.
- **Hybrid Approaches** — Most real graphs combine extraction (coverage) with authority lookup (identity resolution) rather than pure extraction or pure curation.
- **The Goal** — The free cases show what high-quality looks like; extraction pipelines should aim for similar precision while reaching knowledge the structured sources miss.

### Chapter 8: Designing Your Schema

- **Schema Design as Intellectual Work** — Schema design is epistemological; it determines what the domain *is* and what reasoning becomes possible.
- **Entities: What Gets to Be a Thing** — Entity versus property depends on questions the graph must answer; entities participate in relationships as subjects and objects.
- **Relationships: Meaning and Direction** — Typed relationships carry meaning; generic "associated with" is useless; semantic granularity must balance extraction feasibility and reasoning support.
- **Hierarchy and Inheritance** — Hierarchies enable useful queries but add complexity; add hierarchy only if it supports reasoning that flat schemas cannot.
- **Provenance as a First-Class Schema Concern** — Provenance design affects all downstream phases; source, method, confidence, and evidence type should be captured from the start.
- **Designing for Extraction** — Some relationship types are easy to extract; others are not; schema and extraction prompt should co-evolve.
- **Designing for Evolution** — Schemas will change; versioning and single-source-of-truth modules reduce drift and migration pain.

---

## Part III: Building It

### Chapter 9: Diagnostic Tools

A good graph visualization is the most valuable diagnostic tool, revealing duplicates, missing connections, and graph structure. Search, entity coloring, traversal controls, statistics, relationship labels, and interactive details enable inspection of extraction quality and graph coherence.

### Chapter 10: Design Priorities

This chapter examines key design decisions before building, particularly provenance, which is painful to retrofit.

- **Provenance** — Provenance importance depends on use case; high-stakes domains require full traceability; it must be architectural, not an add-on.
- **Confidence as a Signal, Not a Guarantee** — LLM confidence correlates with accuracy but is not calibrated; combine with provenance and domain judgment.
- **Multi-Source Relationships** — Aggregating evidence across sources is meaningful; replication signals robustness; design the data model for this aggregation.
- **Provenance at Query Time** — Query interfaces should support "show me evidence" as a first-class operation for domains requiring verification.

### Chapter 11: The Identity Server

- **Identity Is Load-Bearing** — Canonical entities with canonical IDs are what separate a useful graph from sophisticated extraction; everything else is in service of identity.
- **The Scale of the Problem** — One entity appears under dozens of forms; deduplication at scale is computationally tractable but requires care.
- **Canonical IDs as Primary Keys** — Using external authority IDs as primary keys forces early identity resolution, enables interoperability, and prevents isolated graphs.
- **Authority Lookup** — Established authorities exist in most domains; treating them as primary identifier sources creates interoperable graphs.
- **The Lookup Chain** — Multi-stage resolution (exact → fuzzy → embedding) balances API cost with match quality.
- **Provisional Entities and Promotion** — Not all entities resolve immediately; provisional entities participate fully until promotion thresholds are met.
- **Provenance-Derived Entities and the Citation Graph** — Provenance-derived entities (papers, authors, citations) from document metadata are more reliable than extracted ones.
- **Responsibilities** — Identity server handles canonical ID assignment, promotion, synonym recognition, and merging.
- **Abstract Interface and Reference Implementation** — Abstract base class with domain-pluggable behavior; Postgres-backed `medlit` implementation uses advisory locks and pgvector.

### Chapter 12: The Ingestion Pipeline

- **Why Multiple Passes at All** — Multiple stages provide isolation, recoverability, debuggability, and natural units of work (per-document bundles).
- **Parsing: Getting to Text** — Extract structured text from source formats; preserve section boundaries for semantic weight.
- **Extraction: The LLM Pass** — Schema-binding prompts describe entity and relationship types precisely; balance specificity (precision) with flexibility (recall).
- **Vocabulary: Building a Shared Terminology** — Optional dedicated pass that builds a shared vocabulary and injects it into extraction for consistency.
- **Deduplication** — Group mentions, resolve to canonical forms; authority lookup handles many cases; embedding and co-occurrence help with residue.
- **Assembly** — Merge per-document extractions; aggregate evidence across sources; design bundle structure carefully.
- **Progress Tracking and Resumability** — Design for large-scale runs that fail partway; checkpointing and resumability prevent restart overhead.
- **Stages** — Fetch, Extract, Ingest (with identity resolution), and Build Bundle; Postgres work queue with `SKIP LOCKED` for distribution.
- **Work Queue, Artifact Files, and Reference Implementation** — Full implementation notes for Postgres, per-paper JSON artifacts, parallelism strategy, and batch invocation.

---

## Part IV: What It Makes Possible

### Chapter 13: What Your Graph Can Do

- **The Server Is Not the Point** — Graph capabilities are independent of serving layer; REST, GraphQL, MCP, or custom APIs all work.
- **Direct Querying** — Entity lookup, relationship queries, traversal; design primitives that map to domain questions.
- **Graph Visualization** — Force-directed visualization reveals structure, clusters, bridges, and outliers better than tabular output.
- **Grounding LLM Inference** — Instead of asking the model to remember, give it retrieved graph to reason over; shifts from "hallucination" to "synthesis from sources."
- **MCP as the Integration Point** — Model Context Protocol makes the graph a discoverable, queryable, active participant in agentic reasoning.
- **BFS Queries** — Breadth-first search query language designed for LLM friendliness; topology and presentation are orthogonal.
- **Hypothesis Generation** — Traverse the graph to surface candidates (drug-disease pairs, structural analogies, gap-based suggestions) for human evaluation.
- **Should Hypothesis Generation Be Baked In?** — Framework should provide primitives (traversal, similarity, subgraph queries); domain code interprets what's interesting.
- **Returning to the Dream** — The vision of machines reasoning over explicit knowledge is finally reachable; the representation was the bottleneck.

### Chapter 14: The Augmented Researcher

- **What Machines Would See That We Can't** — Graphs surface patterns filtered out by confirmation bias, prestige bias, and recency bias; different views complement each other.
- **The Combinatorial Argument** — Important discoveries sit at domain intersections; graphs enumerate candidate connections humans couldn't hold in mind.
- **Linguistic and Geographic Blind Spots** — Graphs built from diverse corpora surface work citation networks systematically hide; particularly valuable for rare diseases and regional research.
- **The Robot Scientist, Revisited** — Adam and Eve demonstrated the pattern; extraction pipelines now make building the knowledge representation practical at scale.

### Chapter 15: Who Benefits, Who Decides

- **Democratization and Its Limits** — Building remains resource-intensive, but technology enables democratization if policy and incentives align.
- **Compressed Discovery Timelines** — The knowledge synthesis bottleneck becomes quicker; research pace accelerates in drug discovery, rare disease, and materials science.
- **The Rare Disease Problem** — Small communities can't synthesize full literature; graphs serve as coordination and knowledge synthesis mechanisms.
- **Credit, Priority, and Provenance** — When machines surface connections, credit attribution and scientific priority depend on provenance tracking; technical choices have ethical implications.
- **Who Owns the Graph** — Open versus proprietary carries consequences for the scientific commons; the governance question mirrors GenBank and clinical trial data tensions.

### Chapter 16: The Inference You Didn't Intend

- **The Architecture of Expertise** — Knowledge graphs capture the deep structure of expert understanding; systems reasoning over them have access to that architecture.
- **Capability Is Not Bounded by Intent** — Rich, structured, provenance-tracked knowledge enables inferences builders didn't anticipate; capability transcends intended use.
- **Dual Use at Graph Scale** — The same facts support both beneficial and harmful applications; responsible practice requires access control, provenance transparency, logging, and auditability.
- **Bias at Scale** — Graphs encode and amplify source biases; diverse sourcing and provenance transparency help but don't eliminate the problem.
- **The Epistemic Responsibility of the Builder** — Builders owe honesty about limits, infrastructure for verification, and consideration of foreseeable consequences.

### Chapter 17: What's Next

- **Open Problems** — Very long documents, multi-hop reasoning during extraction, real-time updating, and schema evolution without re-extraction remain challenging.
- **Where the Field Is Going** — LLMs will change; the need for this grounding layer is permanent; RAG and structured world models converge on the same architectural insight.
- **An Invitation** — The extraction bottleneck held for 50 years; it's now breakable; this opens the capability to build cross-domain knowledge synthesis at scale.

---

## Appendix A: BFS Query Language Reference

Reference for the breadth-first search query language designed for LLM-friendly graph traversal.

- **Query Format** — `seeds`, `max_hops`, `node_types`, `predicates`, `topology_only` parameters for breadth-first subgraph retrieval.
- **Response Format** — Full nodes (metadata), stub nodes (ID only), full edges (provenance), stub edges (topology) structure and examples.
- **LLM Prompt Template** — Template for instructing LLMs to construct BFS queries with three worked examples.
- **Design Considerations** — Topology and presentation orthogonality, why stubs over omission, edge provenance cost, multiple seeds for relational queries, independent filter composition, and BFS depth guidance.

## Appendix B: Reference Implementation Notes

Detailed implementation guidance for the identity server and ingestion pipeline.

- **Identity Server Abstract Interface** — Python ABC defining `resolve`, `promote`, `find_synonyms`, `merge`, and `on_entity_added` operations.
- **Domain-Pluggable Behaviour** — Table of concerns left to domain: authority lookup, synonym criteria, survivor selection, promotion thresholds.
- **Survivor Selection** — `DomainSchema.preferred_entity` method for choosing merge survivors.
- **Entity Status** — Three statuses: provisional, canonical, merged; status rules for merges and promotion.
- **Idempotency Contract** — All operations must be safe to retry; mechanisms described for each operation.
- **Postgres-Backed Implementation** — Locking strategies per operation, authority lookup caching in Redis, synonym detection via pgvector, schema notes, multi-replica deployment safety.
- **Ingestion Pipeline: Work Queue** — Postgres `ingest_jobs` table structure for distributed work claiming with `SKIP LOCKED`.
- **Paper Artifact Files** — Atomic write-then-rename strategy; serves recovery, auditability, and retraction purposes.
- **Parallelism** — Per-stage bottlenecks and independent concurrency limits.
- **Batch Ingestion** — Shell script orchestrating four stages; each stage as a Python module invoked via `uv run`.
- **MCP Tool** — Single-paper convenience for interactive queries; calls same pipeline stages as batch CLI.
- **Extraction Output Format** — JSON artifact structure: mentions with locations, relationships with evidence locations, no IDs (assigned post-extraction by identity server).
- **Shared Pipeline Code** — `_run_pass2_pass3_load` shared between batch and MCP paths.
