# Knowledge Graphs from Unstructured Text -- Outline

## Foreword: A Manifesto for Machine Knowledge

*This foreword appears in all three volumes of the Graphwright series.*

- **The Stakes** -- Machine reasoning is now deployed in high-stakes domains:
  medicine, law, engineering, spaceflight. The cost of error is real.
- **What LLMs Cannot Do** -- Mastery of syntax without identity: no persistent
  notion of what things *are*, no stable reference, no chained causality.
- **Why RAG Is Not Enough** -- Retrieval improves relevance but still operates
  on strings, not things; it cannot say "this refers to that."
- **The Three Requirements** -- Identity (canonical IDs, deduplication, a fixed
  entity type set), Type (a finite predicate vocabulary with domain/range
  constraints), and Provenance (source traceability, evidence aggregation,
  confidence grounded in origin).
- **The Typed Graph** -- A data model that satisfies all three: well-formed
  claims, grounded identities, traceable sources. Not a guarantee of truth,
  but a guarantee of inspectability, reproducibility, and correctness.
- **The Pipeline** -- Unstructured text → extraction → mentions → identity
  resolution → typed graph → queries/traversals → machine reasoning.

---

## Preface

Introduction to LLM hallucination as the motivating problem, knowledge graphs as the solution, and an overview of the book's structure and the `kgraph`/`medlit` example project.

---

## Part I: The Landscape

### Chapter 1: Why Do We Want to Build Knowledge Graphs?

- **Large Language Models Work Great** -- LLMs fluently answer questions about well-known facts and achieve high accuracy on familiar domains.
- **Until They Don't** -- Hallucination is baked into LLM design; they fail systematically outside their training distribution with no mechanism to signal uncertainty.
- **The Scale of the Problem** -- For high-stakes domains (medicine, law, science), hallucination is unacceptable and requires grounded, traceable answers.
- **Retrieval-Augmented Generation or "RAG"** -- RAG helps by retrieving passages, but unstructured text requires the model to parse and infer structure every time.
- **Graph RAG** -- Giving LLMs a knowledge graph with typed relationships provides explicit structure they can reason over and cite.
- **Why Bother Building One?** -- Knowledge graphs offer high ROI, are simple to understand, increasingly buildable with current tools, and naturally support LLM grounding.

### Chapter 2: A Brief History of Knowledge Representation

- **The Idea That Wouldn't Die** -- Decades of ambitious projects sought to build machines that understand rather than merely retrieve; the goal was always right, the tools were always insufficient.
- **Meaning is Relational** -- From Minsky's frames to Hofstadter's symbol systems: knowledge isn't a list of facts, it's a web of typed relationships. The knowledge graph is what that insight looks like as buildable infrastructure.
- **The Bottleneck Was Always Extraction** -- Expert systems, Cyc, the Semantic Web, Google's Knowledge Graph -- all hit the same wall: getting knowledge in from natural language prose. Not a failure of reasoning; a failure of economics.
- **LLMs Change the Economics** -- The marginal cost of a new extraction task dropped from months to hours. That's the only thing that changed, and it changes everything.

### Chapter 3: What Is a Knowledge Graph, Really?

- **A Working Definition in Four Parts** -- Nodes are entities; edges are typed relationships; every entity has canonical identity; every relationship carries provenance.
- **The Semantics Matter** -- Typed relationships carry meaning; generic labels like "associated with" are nearly useless; the type is the knowledge.
- **Provenance and the Epistemics of a Fact** -- Claims have epistemological status; provenance records source, method, confidence, and evidence type so downstream systems can weight them appropriately.
- **Identity: The Hard Problem** -- Canonical identity resolves multiplicity (synonyms, aliases, misspellings) to single nodes and anchors entities to authoritative ontologies.
- **What a KG Is Good For** -- Querying (structured answers), traversal (multi-hop reasoning), hypothesis generation (pattern matching), and LLM grounding (explicit sources).
- **Build vs. Buy** -- Existing graphs cover some domains; building is necessary for novel domains, proprietary corpora, custom schemas, and full provenance traceability.
- **What a KG Is Not Good For** -- Quality reflects sources; coverage gaps create false negatives; maintenance is ongoing; bias encodes and amplifies at scale.

### Chapter 4: Representation Is Reasoning

- **From Fluency to Grounded Reasoning** -- LLMs are fluent but ungrounded; explicit structured knowledge enables tracing, correcting, and bounding the reasoning.
- **Experts Have Internal Knowledge Graphs** -- Domain experts reason over structured mental models; the graph makes that structure explicit and machine-accessible.
- **Grounded Representation as the Fix** -- Giving the model explicit claims to reason from produces fundamentally different behavior than asking it to retrieve from statistical memory.
- **Provenance, Auditability, Trust** -- Explicit graphs are inspectable; implicit neural networks are black boxes; auditability is a requirement in high-stakes domains.

### Chapter 5: The Extraction Problem

- **Humans Are Smarter Than You Think** -- Scientific text is dense with hedging, negation, implicit relationships, cross-sentence dependencies, and domain jargon; a single sentence can carry a finding, a population, a comparison structure, a statistical qualifier, and a subgroup caveat.
- **Classical NLP Was Brittle Here** -- Progress was real but narrow; domain adaptation required months of annotation work per new field, and the hard cases (negation, implicit claims, long-range dependencies) remained stubbornly resistant.
- **LLMs Handle It Naturally** -- The marginal cost of a new extraction task is now a prompt, not a research project; the same model that handles hedging in oncology handles it in law or materials science without retraining.

---

## Part II: LLMs Change the Equation

### Chapter 6: LLMs Make This Practical Now

- **What LLMs Actually Are, For This Purpose** -- LLMs are pattern-completion engines with internalized knowledge of domain relationships; the prompt binds that knowledge to a schema.
- **The Prompt as Schema Binding** -- Schema in the prompt (not in model weights) enables rapid iteration, collaborative review with domain experts, and version control.
- **Handling What Classical Systems Couldn't** -- LLMs handle hedging, negation, implicit relationships, cross-sentence dependencies, and domain jargon far better than classical systems.
- **The Remaining Limitations, Honestly** -- Hallucination occurs; context windows are finite; cost accumulates; non-determinism complicates reproducibility; LLMs reflect their training distribution.
- **Why This Moment** -- Model capability (GPT-4 threshold), API accessibility, and tooling ecosystem all matured simultaneously around 2023–present.

### Chapter 7: The Free KG Cases

- **When You Don't Need Extraction** -- Structured sources (databases, APIs, equipment) don't require extraction; integration and schema mapping suffice.
- **Lab Instruments and Measured Data** -- Genomics produces structured data; graphs like STRING are high-precision over their narrow coverage but miss the literature.
- **Generated and Synthetic Graphs** -- Ontologies and databases provide high-precision relationships but only cover what was explicitly encoded.
- **Curated Graphs at Scale** -- Wikidata and encyclopedias achieve breadth through human curation but cannot scale to full literature in technical domains.
- **What These Cases Teach Us** -- Structured sources set the quality benchmark; extraction targets that benchmark for knowledge not yet structured.
- **Hybrid Approaches** -- Most real graphs combine extraction (coverage) with authority lookup (identity resolution) rather than pure extraction or pure curation.
- **The Goal** -- The free cases show what high-quality looks like; extraction pipelines should aim for similar precision while reaching knowledge the structured sources miss.

### Chapter 8: Designing Your Schema

- **Schema Design as Intellectual Work** -- Schema design is epistemological; it determines what the domain *is* and what reasoning becomes possible.
- **Entities: What Gets to Be a Thing** -- Entity versus property depends on questions the graph must answer; entities participate in relationships as subjects and objects.
- **Relationships: Meaning and Direction** -- Typed relationships carry meaning; generic "associated with" is useless; semantic granularity must balance extraction feasibility and reasoning support.
- **Hierarchy and Inheritance** -- Hierarchies enable useful queries but add complexity; add hierarchy only if it supports reasoning that flat schemas cannot.
- **Provenance as a First-Class Schema Concern** -- Provenance design affects all downstream phases; source, method, confidence, and evidence type should be captured from the start.
- **Designing for Extraction** -- Some relationship types are easy to extract; others are not; schema and extraction prompt should co-evolve.
- **Designing for Evolution** -- Schemas will change; versioning and single-source-of-truth modules reduce drift and migration pain.

---

## Part III: Building It

### Chapter 9: Diagnostic Tools

A good graph visualization is the most valuable diagnostic tool, revealing duplicates, missing connections, and graph structure. Search, entity coloring, traversal controls, statistics, relationship labels, and interactive details enable inspection of extraction quality and graph coherence.

### Chapter 10: Design Priorities

This chapter examines key design decisions before building, particularly provenance, which is painful to retrofit.

- **Provenance** -- Provenance importance depends on use case; high-stakes domains require full traceability; it must be architectural, not an add-on.
- **Confidence as a Signal, Not a Guarantee** -- LLM confidence correlates with accuracy but is not calibrated; combine with provenance and domain judgment.
- **Multi-Source Relationships** -- Aggregating evidence across sources is meaningful; replication signals robustness; design the data model for this aggregation.
- **Provenance at Query Time** -- Query interfaces should support "show me evidence" as a first-class operation for domains requiring verification.

### Chapter 11: The Identity Server

The pipeline's view of the identity server: what to call, what comes back, and what provisional entities mean for the pipeline. Full architecture is in the companion volume *The Identity Server*.

- **Identity Is Load-Bearing** -- Canonical entities with canonical IDs are what separate a useful graph from sophisticated extraction; everything else is in service of identity.
- **The Pipeline's View** -- The ingest stage calls `resolve(mention, entity_type)` as a black box and receives a stable ID; provisional IDs are valid graph nodes that participate fully.
- **Provenance-Derived Entities and the Citation Graph** -- Papers, authors, and citations from document metadata enter with canonical IDs already known; the citation graph enables corpus expansion and surfaces the intellectual neighborhood of the corpus.

### Chapter 12: The Ingestion Pipeline

- **Why Multiple Passes at All** -- Multiple stages provide isolation, recoverability, debuggability, and natural units of work (per-document bundles).
- **Parsing: Getting to Text** -- Extract structured text from source formats; preserve section boundaries for semantic weight.
- **Extraction: The LLM Pass** -- At minimum one prompt per document; staging into multiple focused calls is often worth the added complexity. Either way, the prompt must be grounded in the schema -- entity types and predicates injected from the domain spec so the model works within a closed vocabulary.
  - **What every extraction prompt needs** -- the closed entity-type list; the predicate list with domain/range guidance (to reach for specific predicates over generic ones like `ASSOCIATED_WITH`); corpus vocabulary as preferred names (to suppress surface variation before deduplication); domain instructions for classification edge cases and output format.
  - **The closed-world constraint** -- every relationship subject and object must be an ID from the entities extracted in the same response. The model cannot assert a relationship involving a participant it didn't also classify and type.
  - **Staging tradeoffs** -- one combined call is simpler and often sufficient; splitting (entities first, then relationships over the resolved set) reduces hallucination surface at the cost of latency. Ancillary metadata (study design, author affiliations) belongs in separate lightweight calls.
  - **Required output contract** -- per entity: local ID, type, surface name, synonyms, authority ID hints; per relationship: subject ID, predicate, object ID, evidence span ID, confidence, linguistic trust (`asserted` / `suggested` / `speculative`); per evidence span: passage text, section, paragraph index.
  - **Example prompt** -- Appendix B shows an abstracted version of the medlit extraction prompt, illustrating how entity types, predicates, and vocabulary slot into a template. A starting point for readers implementing their own schema.
- **Vocabulary: Building a Shared Terminology** -- Optional dedicated pass that builds a shared vocabulary and injects it into extraction for consistency.
- **Deduplication** -- Group mentions, resolve to canonical forms; authority lookup handles many cases; embedding and co-occurrence help with residue.
- **Assembly** -- Merge per-document extractions; aggregate evidence across sources; design bundle structure carefully.
- **Progress Tracking and Resumability** -- Design for large-scale runs that fail partway; checkpointing and resumability prevent restart overhead.
- **Stages** -- Fetch, Extract, Ingest (with identity resolution), and Build Bundle; Postgres work queue with `SKIP LOCKED` for distribution.
- **Work Queue, Artifact Files, and Reference Implementation** -- Full implementation notes for Postgres, per-paper JSON artifacts, parallelism strategy, and batch invocation.

---

## Part IV: What It Makes Possible

### Chapter 13: What Your Graph Can Do

- **The Server Is Not the Point** -- Graph capabilities are independent of serving layer; REST, GraphQL, MCP, or custom APIs all work.
- **Direct Querying** -- Entity lookup, relationship queries, traversal; design primitives that map to domain questions.
- **Graph Visualization** -- Force-directed visualization reveals structure, clusters, bridges, and outliers better than tabular output.
- **Grounding LLM Inference** -- Instead of asking the model to remember, give it retrieved graph to reason over; shifts from "hallucination" to "synthesis from sources."
- **MCP as the Integration Point** -- Model Context Protocol makes the graph a discoverable, queryable, active participant in agentic reasoning.
- **BFS Queries** -- Breadth-first search query language designed for LLM friendliness; topology and presentation are orthogonal.
- **Hypothesis Generation** -- Traverse the graph to surface candidates (drug-disease pairs, structural analogies, gap-based suggestions) for human evaluation.
- **Should Hypothesis Generation Be Baked In?** -- Framework should provide primitives (traversal, similarity, subgraph queries); domain code interprets what's interesting.
- **Returning to the Dream** -- The vision of machines reasoning over explicit knowledge is finally reachable; the representation was the bottleneck.

### Chapter 14: The Augmented Researcher

- **What Machines Would See That We Can't** -- Graphs surface patterns filtered out by confirmation bias, prestige bias, and recency bias; different views complement each other.
- **The Combinatorial Argument** -- Important discoveries sit at domain intersections; graphs enumerate candidate connections humans couldn't hold in mind.
- **Linguistic and Geographic Blind Spots** -- Graphs built from diverse corpora surface work citation networks systematically hide; particularly valuable for rare diseases and regional research.
- **The Robot Scientist** -- Adam reasoned over a knowledge graph of yeast biology, formed hypotheses, ran experiments, and confirmed results -- autonomously. Eve extended the pattern to drug discovery. The bottleneck wasn't capability; it was that building the knowledge representation required a team of domain experts working by hand. That bottleneck is gone.

### Chapter 15: Who Benefits, Who Decides

- **Democratization and Its Limits** -- Building remains resource-intensive, but technology enables democratization if policy and incentives align.
- **Compressed Discovery Timelines** -- The knowledge synthesis bottleneck becomes quicker; research pace accelerates in drug discovery, rare disease, and materials science.
- **The Rare Disease Problem** -- Small communities can't synthesize full literature; graphs serve as coordination and knowledge synthesis mechanisms.
- **Credit, Priority, and Provenance** -- When machines surface connections, credit attribution and scientific priority depend on provenance tracking; technical choices have ethical implications.
- **Who Owns the Graph** -- Open versus proprietary carries consequences for the scientific commons; the governance question mirrors GenBank and clinical trial data tensions.

### Chapter 16: The Inference You Didn't Intend

- **The Architecture of Expertise** -- Knowledge graphs capture the deep structure of expert understanding; systems reasoning over them have access to that architecture.
- **Capability Is Not Bounded by Intent** -- Rich, structured, provenance-tracked knowledge enables inferences builders didn't anticipate; capability transcends intended use.
- **Dual Use at Graph Scale** -- The same facts support both beneficial and harmful applications; responsible practice requires access control, provenance transparency, logging, and auditability.
- **Bias at Scale** -- Graphs encode and amplify source biases; diverse sourcing and provenance transparency help but don't eliminate the problem.
- **The Epistemic Responsibility of the Builder** -- Builders owe honesty about limits, infrastructure for verification, and consideration of foreseeable consequences.

### Chapter 17: What's Next

- **Open Problems** -- Very long documents, multi-hop reasoning during extraction, real-time updating, and schema evolution without re-extraction remain challenging.
- **Where the Field Is Going** -- LLMs will change; the need for this grounding layer is permanent; RAG and structured world models converge on the same architectural insight.
- **An Invitation** -- The extraction bottleneck held for 50 years; it's now breakable; this opens the capability to build cross-domain knowledge synthesis at scale.

---

## Appendix A: BFS Query Language Reference

Reference for the breadth-first search query language designed for LLM-friendly graph traversal.

- **Query Format** -- `seeds`, `max_hops`, `node_types`, `predicates`, `topology_only` parameters for breadth-first subgraph retrieval.
- **Response Format** -- Full nodes (metadata), stub nodes (ID only), full edges (provenance), stub edges (topology) structure and examples.
- **LLM Prompt Template** -- Template for instructing LLMs to construct BFS queries with three worked examples.
- **Design Considerations** -- Topology and presentation orthogonality, why stubs over omission, edge provenance cost, multiple seeds for relational queries, independent filter composition, and BFS depth guidance.

## Appendix B: Reference Implementation Notes

Implementation guidance for the medlit ingestion pipeline. Identity server specification (Python ABC, domain plugin contract, Postgres schema, Docker setup) is in the companion volume *The Identity Server*, Appendix A and B.

- **Ingestion Pipeline: Work Queue** -- Postgres `ingest_jobs` table structure for distributed work claiming with `SKIP LOCKED`.
- **Paper Artifact Files** -- Atomic write-then-rename strategy; serves recovery, auditability, and retraction purposes.
- **Parallelism** -- Per-stage bottlenecks and independent concurrency limits.
- **Batch Ingestion** -- Shell script orchestrating four stages; each stage as a Python module invoked via `uv run`.
- **MCP Tool** -- Single-paper convenience for interactive queries; calls same pipeline stages as batch CLI.
- **Extraction Output Format** -- JSON artifact structure: mentions with locations, relationships with evidence locations, no IDs (assigned post-extraction by identity server).
- **Shared Pipeline Code** -- `_run_pass2_pass3_load` shared between batch and MCP paths.
- **Extraction Prompt Template** -- Abstracted Jinja2 template with three injection points (`{{ entity_types }}`, `{{ predicates }}`, `{{ vocab_section }}`), the closed-world subject/object constraint, linguistic trust classification, and evidence ID format. Medlit domain instructions shown as a worked example of encoding entity classification rules and predicate guidance for a specific domain.
