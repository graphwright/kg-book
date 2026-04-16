# Knowledge Graphs from Unstructured Text -- Outline

## Background information that does not go in the book

A *typed knowledge graph* is one with a fixed finite set of entity types and
a fixed finite set of permitted predicates. Each predicate has a domain, which
is a fixed finite set of allowable entity types, and a range, which is also a
fixed finite set of allowable entity types. Therefore "aspirin treats migraine"
is permitted because "drug" is in the domain for "treats" and "condition"
(a migraine headache) is in the range for "treats". But "BRCA1 treats schoolbus"
is not permitted.

First book (../identity-book): *The Typed Graph: How Machine Knowledge Earns Trust*
Second book (this book): *Knowledge Graphs from Unstructured Text*
Third book (../bfl-qs-book): *BFS-QL: A Graph Query Protocol for Language Models*

(Writing style guidance is in CLAUDE.md.)


## Foreword: A Manifesto for Machine Knowledge

*This foreword appears in all three volumes of the Graphwright series. This foreword is already written.*

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

Introduction to LLM hallucination as the motivating problem, *typed* knowledge graphs as the solution, and an overview of the book's structure and the two example domains used throughout: `medlit` (medical literature, with authority-backed canonical IDs) and `sherlock` (Sherlock Holmes stories, no external authorities -- a simpler template for non-medical domains). Both are reference implementations in the `kgraph` repo.

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
  This is a *typed* knowledge graph as described in the other book (../identity-book).
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
- **Why This Moment** -- Model capability (GPT-4 threshold), API accessibility, and tooling ecosystem all matured simultaneously in the last two or three years.
- **Domain Generality** -- The same framework handles medical literature (authority-backed canonical IDs, UMLS/HGNC/RxNorm) and literary fiction (domain-minted IDs, no external authority). Swapping domains means swapping the schema and extraction prompts, not the pipeline code.

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
- **The Single Source of Truth Module** -- Entity types, predicates, prompt instructions, and vocabulary guidance belong in one module (e.g. `domain_spec.py`); the extraction prompt, validation logic, and dedup all import from it. One edit propagates everywhere; no drift between prompt and schema.

---

## Part III: Building It

### Chapter 9: Diagnostic Tools

A good graph visualization is a very valuable diagnostic tool, revealing duplicates, missing connections, and graph structure. Force-directed layout makes structural problems legible before they surface in logs.

- **Force-Directed Visualization** -- Nodes laid out by spring forces reveal clusters, bridges, and outliers not apparent in tabular output; entity types are color-coded; clicking a node shows its full metadata and relationships.
- **What to Look For** -- Duplicate nodes with slight name variations (dedup failures), high-degree hubs that may represent under-specified entity types, disconnected components suggesting extraction gaps, and relationships with low confidence clustered by source.
- **Visualization as Pipeline Signal** -- Unexpectedly long evidence spans or malformed relationship metadata are often first exposed as visual anomalies -- a sprawling hub where there should be none, or a cluster of nodes that should have resolved to one.

### Chapter 10: Design Priorities

This chapter examines key design decisions before building, particularly provenance, which is painful to retrofit.

- **Provenance** -- Provenance importance depends on use case; high-stakes domains require full traceability; it must be architectural, not an add-on.
- **Confidence as a Signal, Not a Guarantee** -- LLM confidence correlates with accuracy but is not calibrated; combine with provenance and domain judgment.
- **Multi-Source Relationships** -- Aggregating evidence across sources is meaningful; replication signals robustness; design the data model for this aggregation.
- **Provenance at Query Time** -- Query interfaces should support "show me evidence" as a first-class operation for domains requiring verification.

### Chapter 11: The Identity Server

Shallow treatment -- full architecture is in the first book, *The Typed Graph: How Machine Knowledge Earns Trust*.

- **Identity Is Load-Bearing** -- Canonical entities with canonical IDs are what separate a useful graph from sophisticated extraction; everything else is in service of identity.
- **The Pipeline's View** -- The ingest stage calls the identity server as a black box: given a mention and entity type, it returns a stable ID (canonical if an authority matched, provisional otherwise). Provisional IDs are valid graph nodes; the pipeline does not handle them specially.
- **Provenance-Derived Entities and the Citation Graph** -- Papers, authors, and citations from document metadata enter with canonical IDs already known; the citation graph enables corpus expansion and surfaces the intellectual neighborhood of the corpus.

### Chapter 12: The Ingestion Pipeline

- **The Framework's Five Abstractions** -- Parser, entity extractor, entity resolver, relationship extractor, and bundle export; each a pluggable interface implemented per domain. Domain code implements these; the framework orchestrates them.
- **Why Two Passes** -- Resolving entities first produces a stable vocabulary before relationship extraction runs, enabling cross-document linking and making each pass independently debuggable and recoverable.
- **Parsing: Getting to Text** -- Extract structured text from source formats; preserve section boundaries for semantic weight and provenance.
- **Extraction: The LLM Pass** -- The prompt binds entity types and predicates from the domain spec, enforces a closed-world constraint (relationships may only reference entities extracted in the same response), and requires structured output with confidence and linguistic trust. Details and a worked example in Appendix A.
- **Deduplication** -- Group mentions, resolve to canonical forms; an optional vocabulary pre-pass reduces surface variation before deduplication runs; embedding similarity handles residue.
- **Assembly and Bundle Export** -- Merge per-document extractions; aggregate evidence across sources; export to a versioned bundle format that is the contract between the ingestion pipeline and the query layer.
- **Progress Tracking and Resumability** -- Design for large-scale runs that fail partway; each document tracks its own status; durable per-document artifacts allow restart without re-fetching or re-paying LLM costs.

---

## Part IV: What It Makes Possible

### Chapter 13: What Your Graph Can Do

- **The Serving Layer Is Not the Point** -- Graph capabilities are independent of serving layer; REST, MCP, or custom APIs all work; the graph is the data structure, the server is a delivery mechanism.
- **Direct Querying** -- Entity lookup, relationship queries, traversal; design primitives that map to domain questions.
- **Graph Visualization** -- Force-directed visualization reveals structure, clusters, bridges, and outliers better than tabular output.
- **Grounding LLM Inference** -- Instead of asking the model to remember, give it retrieved graph to reason over; shifts from "hallucination" to "synthesis from sources."
- **MCP as the Integration Point** -- Model Context Protocol makes the graph a discoverable, queryable, active participant in agentic reasoning.
- **BFS Queries** -- Breadth-first search query language designed for LLM friendliness; topology and presentation are orthogonal. Refer to third book.
- **Hypothesis Generation** -- Traverse the graph to surface candidates (drug-disease pairs, structural analogies, gap-based suggestions) for human evaluation.
- **Returning to the Dream** -- The vision of machines reasoning over explicit knowledge is finally reachable; the representation was the bottleneck.

### Chapter 14: The Augmented Researcher

- **What Machines Would See That We Can't** -- Graphs surface patterns filtered out by confirmation bias, prestige bias, and recency bias; different views complement each other.
- **The Combinatorial Argument** -- Important discoveries sit at domain intersections; graphs enumerate candidate connections humans couldn't hold in mind.
- **Linguistic and Geographic Blind Spots** -- Graphs built from diverse corpora surface work citation networks systematically hide; particularly valuable for rare diseases and regional research.
- **The Robot Scientist** -- Adam reasoned over a knowledge graph of yeast biology, formed hypotheses, ran experiments, and confirmed results -- autonomously. Eve extended the pattern to drug discovery. The bottleneck wasn't capability; it was that building the knowledge representation required a team of domain experts working by hand. That bottleneck is gone.

### Chapter 15: Consequences

- **Democratization and Its Limits** -- Building remains resource-intensive, but technology enables democratization if policy and incentives align.
- **Compressed Discovery Timelines** -- The knowledge synthesis bottleneck becomes quicker; research pace accelerates in drug discovery, rare disease, and materials science.
- **The Rare Disease Problem** -- Small communities can't synthesize full literature; graphs serve as coordination and knowledge synthesis mechanisms.
- **Credit, Priority, and Provenance** -- When machines surface connections, credit attribution and scientific priority depend on provenance tracking; technical choices have ethical implications.
- **Who Owns the Graph** -- Open versus proprietary carries consequences for the scientific commons; the governance question mirrors GenBank and clinical trial data tensions.
- **Capability Is Not Bounded by Intent** -- Rich, structured, provenance-tracked knowledge enables inferences builders didn't anticipate; capability transcends intended use.
- **Dual Use at Graph Scale** -- The same facts support both beneficial and harmful applications; responsible practice requires access control, provenance transparency, logging, and auditability.
- **Bias at Scale** -- Graphs encode and amplify source biases; diverse sourcing and provenance transparency help but don't eliminate the problem.
- **The Epistemic Responsibility of the Builder** -- Builders owe honesty about limits, infrastructure for verification, and consideration of foreseeable consequences.
- **Open Problems** -- Very long documents, multi-hop reasoning during extraction, real-time updating, and schema evolution without re-extraction remain challenging.
- **Where the Field Is Going** -- LLMs will change; the need for this grounding layer is permanent; RAG and structured world models converge on the same architectural insight.

---

## Appendix A: Reference Implementation Notes

Implementation guidance for the medlit ingestion pipeline. The BFS-QL query language spec is in the companion volume *BFS-QL: Graph Queries for Language Models*. The identity server spec is in the companion volume *The Identity Server: Canonical Identity for Knowledge Graphs*.

- **Ingestion Pipeline: Work Queue** -- Postgres `ingest_jobs` table structure for distributed work claiming with `SKIP LOCKED`.
- **Paper Artifact Files** -- Atomic write-then-rename strategy; serves recovery, auditability, and retraction purposes.
- **Parallelism** -- Per-stage bottlenecks and independent concurrency limits.
- **Batch Ingestion** -- Shell script orchestrating four stages; each stage as a Python module invoked via `uv run`.
- **MCP Tool** -- Single-paper convenience for interactive queries; calls same pipeline stages as batch CLI.
- **Extraction Output Format** -- JSON artifact structure: mentions with locations, relationships with evidence locations, no IDs (assigned post-extraction by identity server).
- **Shared Pipeline Code** -- Functions shared between batch and MCP paths.
- **Extraction Prompt Template** -- Abstracted Jinja2 template with three injection points (`{{ entity_types }}`, `{{ predicates }}`, `{{ vocab_section }}`), the closed-world subject/object constraint, linguistic trust classification, and evidence ID format. Medlit domain instructions shown as a worked example of encoding entity classification rules and predicate guidance for a specific domain.
