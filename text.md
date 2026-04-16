---
title: Knowledge Graphs from Unstructured Text
author: Will Ware
rights: © 2026 Will Ware, MIT License
language: en-US
description: "A practitioner's guide to building knowledge graphs from unstructured text using LLMs."
...

## Foreword: A Manifesto for Machine Knowledge

`\markboth{Foreword}{Foreword}`{=latex}

*This foreword appears in all three volumes of the Graphwright series.*

We are now in an age of machine reasoning, and some of this reasoning is done
in high-stakes domains: medicine, law, engineering, spaceflight. Lives and
livelihoods can be affected by incorrect conclusions or decisions. The cost of
error is real and significant. LLMs are here, they are staying, and there is no
turning back the clock.

As we all know, LLMs have weaknesses. Their mastery of language syntax is
astonishing, but they don't understand "this refers to that," or "these two
things are the same." They have no persistent notion of identity. They do not
inhabit a world of things connected by relationships. They do not track logical
consequence from one step to the next.

They cannot reason across multiple causal steps because they cannot reliably
reason across a single causal step. They do not know what things *are* or how
they *behave*, only how they are *talked about*.

And so we build RAG (retrieval-augmented generation) systems, hoping to improve
the situation. We improve the LLM's focus on material that is more relevant,
more similar, better connected to sources of information, and it helps.

But we are still dealing with strings, not things.

We still cannot say "this refers to that," or "these two mentions refer to the
same entity." We still cannot follow a chain of causality or enforce a sequence
of logical steps. We retrieve passages, but we do not operate on meaning.

If RAG doesn't close the gap, what would?

- **Identity -- what are we talking about?**
  - Canonical IDs -- identifiers anchored in curated human knowledge (think Wikipedia)
  - Authoritative ontologies -- shared bodies of reference (think dictionaries, taxonomies)
  - Deduplication across sources -- recognizing that the same thing may be named
    in different ways ("tumor" vs "neoplasm")
  - A fixed set of entity types

- **Type -- which relationships are meaningful?**
  - A fixed set of predicates
  - Domain and range for each predicate -- constraints on which kinds of things
    can be related, so we do not assert things like "aspirin inhibits New York"
  - Structural validity -- a claim is valid if it is well-formed with respect to
    the graph's type system, independent of whether it is true or false

- **Provenance -- where did this claim come from?**
  - Source traceability
  - Evidence aggregation
  - Confidence grounded in origin

A system cannot reason reliably about the world unless it represents that world
with stable identities, constrained relationships, and explicit evidence.

Machine reasoning requires a data model, not just a model.

### The Typed Graph

When we build a knowledge graph where we

- fix the set of entity types and the set of predicates
- establish domain and range constraints for each predicate
- require that entities be assigned canonical IDs whenever possible
- preserve provenance information for all relationships

we are no longer dealing with strings, but with a structured representation of
the world. This is what we call a *typed graph*\index{typed graph}.

A typed graph does not guarantee that its conclusions are true. It guarantees
something more fundamental: that its claims are well-formed, grounded in
identifiable entities, and traceable to their sources.

Large classes of nonsense and hallucination are not corrected -- they are never
admitted into the system at all. Category errors are rejected. Ambiguous
references are resolved or made explicit. Unsupported claims are visible as such.

The result is a system whose outputs may still be wrong, but are always
inspectable, reproducible, and subject to correction.

That is the minimum standard for reasoning in high-stakes domains.

```
Unstructured Text
       |
       v
  Extraction (LLM)
       |
       v
  Mentions (strings)
       |
       v
  Identity Resolution
  -- canonical IDs, deduplication
       |
       v
  Typed Graph
  -- entity types, predicates, domain/range, provenance
       |
       v
  Queries / Traversals
       |
       v
  Machine Reasoning
  -- multi-step, composable, inspectable
```

## Preface

My brother told an LLM:

> I live near a carwash and the weather is warm and sunny. I want to get my car washed. Should I walk or drive there?

and of course he was told that on a nice day like this, he could use the exercise, so he should walk to the carwash. The model didn't know he would need his car in order to get it washed. The wrong answer was delivered with the same tone and confidence as a right one. That's the problem this book is about.

Large language models are fluent, capable, and unreliable in ways that are hard to predict in advance. They fail not randomly but systematically: at the boundary of what their training covered, at questions that require grounded reasoning about specific domains, at any task where being wrong matters. The fix is not to distrust them entirely. It is to give them something reliable to reason from — a structured, inspectable, domain-specific representation of what is actually known. That is a knowledge graph.

This is a book written in the age of Large Language Models, but the central thesis is about machine reasoning in general, now and in the future. Knowledge graphs predate LLMs and will outlast them, because they capture something essential to how humans understand and reason about complex fields in an explicit, structured form that can be shared and curated. A machine cannot reason reliably about such fields without knowledge encoded in some form of graph. The software projects described here are demonstrations of this thesis, not the subject of it. LLMs are enablers for the creation of knowledge graphs, which were much discussed in the past but only practical at scale now.

This book intentionally addresses two kinds of reader. Some readers will come for the argument — the history of knowledge representation, the case for explicit structure, the implications of what becomes possible when extraction is tractable. Others will come for the engineering — the schema design, the pipeline architecture, the identity resolution, the serving layer. The book tries not to exclude either. Readers who want the argument can follow Part I and Part IV without getting lost in Part III. Readers who want the engineering will find it in Parts II and III, grounded in the argument of Part I.

![](ExampleGraph.png)

A simple knowledge graph: nodes represent entities, edges represent typed relationships between them. The labels carry meaning; without them, the structure is just topology.

This book builds its argument around a concrete project: a knowledge graph for medical literature, available at https://github.com/wware/kgraph. The project is the worked example throughout the book -- when the engineering chapters describe extraction pipelines, identity servers, and graph serving, that is the code they are describing.

The `kgraph` repository contains two example domains. `examples/medlit` is the medical literature implementation: parsing PubMed Central articles, extracting entities and relationships with an LLM (large language model), and resolving them to canonical IDs from biomedical authorities (UMLS, HGNC, RxNorm). `examples/sherlock` is a simpler literary example -- Sherlock Holmes stories from Project Gutenberg, characters and locations extracted, no external authority lookup needed -- that shows the same framework applied to a domain without canonical ID infrastructure. The medlit example is the primary worked case throughout the book; sherlock appears where a simpler illustration is useful. Both produce the same output format: a bundle that a query layer can load and serve.

The gist of this book (beyond providing a lot of how-to information) is that a knowledge graph in some form is

- a necessity, not just a convenience, for reliable machine reasoning
- an explicit representation of how human experts understand difficult topics

# Part I: The Landscape

## Chapter 1: Why do we want to build Knowledge Graphs?

`\chaptermark{Why build Knowledge Graphs?}`{=latex}

### Large Language Models Work Great

We ask them questions about the capitals of countries, or about a chemical formula, or how long to bake something in the oven, and usually we get an answer that is articulate, confident, intelligent-sounding, and correct. We can go to Wikipedia or Google and confirm that, yes, that is the right answer. It's a feel-good moment. The fluency is real. The models have internalized an enormous amount of statistical pattern from human text, and for a large class of questions that pattern is enough.

### Until They Don't

Correctness was never a primary design priority for LLMs. They are neural networks trained on large corpora. They try to predict the next bit of text, following statistical patterns derived from the training set. As long as our questions stay well within the training set, we can expect answers that are correct most of the time.

When we stray outside the training set contents, the LLM has no mechanism or structure to gauge correctness and no way to correct an answer. We get answers that are articulate, confident, intelligent-sounding, and wrong. There is no internal signal that says "I'm extrapolating here" or "I'm not sure." The machine has no way to distinguish a retrieval from memory from a plausible guess. This is **hallucination**\index{hallucination} -- the model producing confident, fluent, false output because it is doing what it was designed to do (generate statistically plausible text) in a situation where the right answer is not well represented in its training. Hallucination is not a bug to be patched; it is a predictable consequence of how LLMs work.

### The Scale of the Problem

For casual use, hallucination might be acceptable. For anything that matters -- medical advice, legal research, scientific synthesis, technical decisions -- we need more than fluency. We need answers that are grounded in something checkable, that can be traced to a source, that can be updated when the world changes, and that reflect the structure of the domain rather than the statistics of the training corpus. That is a different kind of system.

### Retrieval-Augmented Generation or "RAG"\index{retrieval-augmented generation}\index{RAG|see{retrieval-augmented generation}}

We can artificially extend the scope of the training set by adding content to the prompt for the parts the LLM is likely to get wrong. My brother might have created a prompt describing car wash operations and mentioning that the car must be physically present for the operations to work. With the prompt extended in this way, eventually the LLM would stop making that kind of mistake. That would have been a laborious manual process of tinkering and re-wording, and seeing what worked best. This approach would not scale to large bodies of knowledge.

In practice, RAG usually means retrieving relevant passages from a document store and stuffing them into the prompt. That helps: the model can reason from the retrieved text instead of relying solely on training. But retrieved passages are still just text. The model has to parse them, resolve references, and combine information across snippets on the fly. There is no explicit representation of *what* entities are in play or *how* they are related. The structure of the domain stays implicit in the prose, and the model is left to infer it every time. For narrow, one-off questions that can be answered from a few paragraphs, this often works. For complex reasoning that depends on many entities and relationships, or for questions you didn't know to ask in advance, passage retrieval hits its limits.

### Graph RAG\index{Graph RAG}

The LLM is given a knowledge graph to consult. Instead of raw passages\index{passage retrieval}, it gets entities and typed relationships: this drug *treats* this condition, this gene *encodes* this protein, this study *reports* this finding. The graph answers "what is connected to what" and "what kind of connection is it" in a form the model can traverse and cite. The entities and the links between them provide facts, context, names, dates, and meaningful connections. You knew you were asking an egg question for your omelette but you didn't realize in advance that you might also want to know how to tell if an egg has gone bad; the graph can expose that connection because the structure is explicit.

A knowledge graph built from your domain gives the model something to reason *from* rather than something to paraphrase. Claims can be traced to sources. Gaps and conflicts in the graph are visible. When the underlying evidence changes, you update the graph instead of retraining the model. The graph is a shared, inspectable representation of what the system is allowed to "know" in that domain.

### Why Bother Building One?

Knowledge graphs provide a unique return on investment. They are simple data structures, easy to understand, not too difficult to build with the tools we have now, and easy for an LLM to query. They reflect the shape of human knowledge with surprising accuracy when the extraction is done well. The rest of this book is about when you want one, how to design it, and how to build it from the unstructured text where most of that knowledge still lives.

## Chapter 2: A Brief History of Knowledge Representation

`\chaptermark{Knowledge Representation History}`{=latex}

### The Idea That Wouldn't Die

There is a fantasy at the heart of computing that is almost as old as computers themselves: the machine that doesn't just store and retrieve facts but *understands* them.\index{machine understanding} Not a filing cabinet you query with the right syntax. Not a search engine that hands you links and wishes you luck. A machine that knows things the way a person knows things -- that can draw on what it understands about a subject and tell you something true and useful in return.

This fantasy has motivated some of the most ambitious projects in the history of computer science, and it has stalled, repeatedly, in the same place. Not at the reasoning end -- researchers got surprisingly far at encoding the logic of a domain. The wall was always at the other end: getting knowledge *in*. Turning the vast, ambiguous record of what humans know -- written in papers and case notes and specifications, in the imprecise medium of natural language -- into something a machine could actually reason from.

### Meaning is Relational\index{semantic networks}

The intellectual lineage of the knowledge graph runs through two mid-twentieth-century ideas that turned out to be more right than their authors could fully demonstrate at the time.

Marvin Minsky's\index{Minsky, Marvin} 1974 paper "A Framework for Representing Knowledge" [@minsky1974framework]\index{A Framework for Representing Knowledge (Minsky)} argued that knowledge isn't a list of facts -- it's a web of structured relationships. When you walk into a restaurant you don't reason from first principles; you retrieve a pre-existing frame with slots for host, menu, food, check, tip, and fill in the details from observation. The relationships *are* the knowledge. A node in isolation is just a label; a node embedded in a typed graph of relationships to other nodes is a concept, with context, with implications, with a place in a web of meaning.

Douglas Hofstadter's\index{Hofstadter, Douglas} argument in *Gödel, Escher, Bach* [@hofstadter1979geb]\index{Godel Escher Bach@\textit{Gödel, Escher, Bach} (Hofstadter)} sharpened this: meaning isn't a property of individual symbols but of symbol systems -- of the relationships and transformations between symbols. "BRCA1" as a string of characters means nothing. It means something because of its typed relationships to other nodes: it *encodes* a protein, it *increases risk* of breast cancer, it *interacts with* other genes. The meaning is in the web, not in the label. A sufficiently rich relational representation doesn't just store knowledge -- it participates in reasoning over it.

The knowledge graph as built today is the realization of what both were pointing at: a rigorous, computable, queryable structure where entities have typed relationships and the graph itself carries meaning. The difference is that Minsky and Hofstadter were working at the level of cognitive theory. We are building infrastructure.

### The Bottleneck Was Always Extraction

The decades that followed produced ambitious attempts to build on these foundations. Expert systems\index{expert systems} in the 1970s and 80s encoded domain knowledge as explicit rules -- MYCIN\index{MYCIN} could outperform medical residents on bacterial infection diagnosis; XCON\index{XCON} saved DEC tens of millions of dollars a year configuring computer systems. Cyc\index{Cyc} attempted to hand-encode common sense at scale, accumulating millions of assertions over decades. The Semantic Web\index{Semantic Web} envisioned machine-readable linked data published across the entire web. Google's Knowledge Graph\index{knowledge panel} demonstrated the value of structured entity knowledge at production scale, built from curated databases and encyclopedias.

Every approach hit the same wall. Expert systems couldn't capture the tacit knowledge experts exercise without noticing. Cyc's hand-encoding phase -- the phase that was supposed to precede the self-learning phase -- never ended. The Semantic Web couldn't solve the adoption problem: structuring content for others' benefit costs more than it returns to the publisher. And Google, with essentially unlimited engineering resources, found it easier to rely on human-curated structured sources than to extract reliably from unstructured text. The bottleneck was never the reasoning. It was always getting knowledge in from natural language prose.

### LLMs Change the Economics

Large language models don't solve every problem in this space, but they dissolve the specific bottleneck that stopped everything else. The marginal cost of a new extraction task dropped from months of domain adaptation and annotation work to a prompt that describes what you're looking for. A cardiologist can review an extraction prompt, understand what it's asking for, and suggest improvements -- without understanding machine learning. Schema changes require editing the prompt, not retraining a model. The cycle from "I want to extract this relationship" to "I have a working extractor" is measured in hours.

That is the only thing that changed. It changes everything. The rest of this book is about how to build what it makes possible.

## Chapter 3: What Is a Knowledge Graph, Really?

`\chaptermark{What Is a Typed Knowledge Graph?}`{=latex}

### A working definition\index{knowledge graph!definition}

A typed knowledge graph has four distinguishing properties. *Entities* are discrete, identifiable things -- people, substances, concepts, events -- each with a *canonical identity*\index{canonical entity}\index{canonical ID}: a stable identifier that persists across documents, authors, and time, anchored where possible to an accepted authority. *Relationships* are typed directed predicates with a defined domain and range; "inhibits" between a drug and an enzyme is a different kind of claim from "co-occurs with," and that distinction is not cosmetic. And every relationship carries *provenance*\index{provenance}: a traceable record of where the claim came from, by what method, and with what confidence. A relationship without provenance is an assertion of unknown quality; with provenance, it is evidence.

Any of these properties can be relaxed for pragmatic reasons -- and sometimes they should be -- but relaxing them has costs that are worth understanding before you do it. The rest of this chapter examines each in turn.

### The Semantics Matter

An edge without a type is nearly useless. Knowing that a drug and a disease are *connected* tells you almost nothing; knowing that the drug *treats* the disease, or *causes* it, or *is contraindicated in* patients with it, tells you something actionable. The meaning of the edge is the knowledge. The edge itself is just the plumbing.

![](link_without_metadata.pdf)

An edge with no label or metadata tells us very little, just that two things are connected in
some way.

![](link_with_metadata.pdf)

Even a very simple label on an edge gives us a more engaging narrative.

Software engineers will recognize this intuition from type systems. An untyped variable that could hold anything is harder to reason about than one whose type tells you what operations are valid on it and what guarantees it carries. The same principle applies to edges in a knowledge graph: a typed relationship isn't just a label, it's a contract. It tells you what the subject and object are allowed to be, what direction the relationship runs, and what it means to assert it. A graph with well-typed edges is one that can catch its own errors -- an "inhibits" edge between two diseases, for instance, is probably a mistake, and a schema that defines valid subject and object types for each predicate will flag that mistake rather than silently incorporate it.

This seems obvious stated plainly, but it has consequences that are easy to underestimate during schema design. The temptation -- especially early, when you're trying to get extraction working at all -- is to start with a small number of generic relationship types and plan to refine them later. "Associated with" is the classic offender: it's easy to extract, it's never wrong, and it's almost never useful. A graph full of "associated with" edges is a graph that can support retrieval but not reasoning.

The flip side is also real: relationship types that are too narrow make extraction impractical. If your schema requires the model to distinguish between "directly inhibits," "allosterically inhibits," and "competitively inhibits," you've created a precision that the extraction step probably can't reliably deliver, and you'll spend more time correcting misclassifications than you'll gain from the distinction. The right level of semantic granularity is the one where the types are meaningfully distinct, expressible in natural language to an extraction model, and actually supported by what your sources say.

There's a third consideration that doesn't get enough attention: direction. "Drug A treats Disease B" and "Disease B is treated by Drug A" are the same fact, but in a directed graph they're different edges. Getting direction consistent across extraction runs and across sources is a detail that causes real headaches if it's not settled early. Treating direction as part of the type definition -- not just a convention but a constraint -- keeps the graph coherent as it grows.

### Provenance and the Epistemics of a Fact

Every edge in a knowledge graph is a claim. And claims, unlike data, have an epistemological status: they come from somewhere, they were established by some method, they are more or less certain, and they may conflict with other claims made by other sources. Provenance is the machinery that tracks all of this.

At minimum, provenance answers: *where did this relationship come from?* -- which source document, which section, which passage. But a well-designed provenance system goes further. It records *how* the relationship was established -- was it extracted by an LLM, identified by a named entity recognizer, asserted by a human curator? It records *confidence* -- not as a precise probability but as an ordinal signal about how much weight to give the claim. And in domains where it matters, it records the *epistemic type* of the evidence -- a randomized controlled trial is a different kind of claim from a case report, which is a different kind of claim from a computational prediction.

This last point deserves emphasis. In medicine, the Evidence and Conclusion Ontology (ECO)\index{Evidence and Conclusion Ontology (ECO)} exists precisely because "there is evidence for this relationship" is not a single thing -- it's a spectrum from "one lab observed this once under unusual conditions" to "this has been replicated across fifty independent studies in multiple populations." A knowledge graph that conflates these is not just imprecise -- it's dangerous. A knowledge graph that preserves the distinction gives downstream reasoning systems something to work with.

The practical consequence is that provenance shouldn't be an afterthought bolted onto a graph that was designed without it. It should be a first-class schema concern from the start. In kgraph, this meant treating evidence as its own entity type -- not just a property of a relationship, but a node in the graph with its own identity, its own source, and its own relationship to the claim it supports. That design decision turns out to have large downstream implications: it makes provenance queryable, traversable, and aggregable across sources in ways that a simple confidence score attached to an edge cannot be.

A graph without provenance is a collection of claims with no way to evaluate them -- no way to ask "how well-supported is this?", no way to debug "why does the graph believe this?", no way to detect when two sources are in conflict rather than in agreement. Provenance is what separates a knowledge structure from a very large list of sentences that someone decided to believe.

### Identity: The Hard Problem

A graph where "BRCA1," "breast cancer gene 1," and "BRCA1 protein" are three separate nodes isn't a knowledge graph -- it's an index.

But the stakes go deeper than deduplication. Canonical identity doesn't just help you say that two things are the same. It places those things within the body of human knowledge. The identifiers that matter -- MeSH or UMLS\index{UMLS} CUI for medical concepts (UMLS is perhaps the more complete resource, but requires a licensed API key; for development purposes MeSH is free and sufficient), Gene Ontology terms for molecular function, DBPedia URIs for cross-domain entities -- come from accepted authoritative ontologies. They are maintained by communities of experts, revised through consensus, and trusted precisely because they represent the accumulated judgment of the field. When you assign a canonical ID to an entity, you are not merely collapsing synonyms. You are connecting that entity to the history of human thought as far as that entity is concerned: its definition, its place in the taxonomy, its relationships to other concepts that the community has already established and agreed upon. A knowledge graph built on canonical IDs is not just a graph of facts -- it is a graph that inherits the epistemic authority of the ontologies it anchors to. That inheritance is what makes the graph trustworthy across sources, across time, and across the boundary between human expertise and machine reasoning.

### What a KG Is Good For

**Querying.** A knowledge graph supports structured queries over entities and relationships in ways that free-text search and document stores cannot. You can ask "what drugs treat this disease?" or "what genes are implicated in this pathway?" and get answers that are aggregated across sources, deduplicated, and typed. The query is over the structure of the domain, not over the surface form of the text. That distinction matters: a search engine returns documents that might contain the answer; a knowledge graph returns the answer, with provenance pointing back to the documents that support it.

**Traversal.** The graph structure enables path-finding and multi-hop reasoning. You can ask not just "what does A connect to?" but "how is A related to B?" -- and the graph can return paths that span multiple edges and intermediate entities. Those paths often reveal connections that no single source states explicitly: the drug and the disease might never appear together in one paper, but the graph can connect them through shared targets, shared pathways, or shared mechanisms. Traversal is what turns a collection of facts into a navigable map of a domain.

**Hypothesis generation.** Because the graph makes structure explicit, it surfaces patterns that weren't in the original sources. Drug repurposing\index{drug repurposing} -- finding that a drug approved for one indication might work for another -- often starts with noticing that two diseases share a mechanism, a target, or a pathway. A graph that connects drugs, targets, diseases, and mechanisms can suggest those connections. So can a human expert with years of training; the graph can do it systematically, at scale, and in a form that can be checked. The hypotheses still require validation -- the graph proposes, it doesn't prove -- but it narrows the search space from "everything we might try" to "things that are structurally plausible."

**LLM grounding.** A large language model reasoning from its training distribution has no way to distinguish what it actually knows from what it has statistically absorbed. Give it a knowledge graph to reason from, and the task changes: the model retrieves relevant subgraphs, synthesizes them, and produces answers that are grounded in explicit, provenance-tracked claims. The model's role shifts from "remember and generate" to "retrieve and synthesize." That shift reduces hallucination, makes the reasoning traceable, and gives downstream users something to audit. We return to this in Chapter 4; for now, the point is that grounding is not a minor application of knowledge graphs but one of their primary use cases in the current AI landscape.

### Build vs. Buy

The landscape of existing knowledge graphs is richer than it used to be. Wikidata offers broad coverage across many domains, with community curation and a flexible schema. Domain-specific graphs like SPOKE\index{SPOKE} (drug-disease-gene) and ROBOKOP\index{ROBOKOP} (pharmacogenomics) provide biomedical structure that general-purpose graphs don't. Commercial offerings from publishers, vendors, and platform providers add proprietary value and integration. The question is not whether knowledge graphs exist -- they do -- but whether one of them fits your problem.

**When existing graphs are sufficient.** If your domain is well-covered, your schema aligns with what the graph provides, and you don't need provenance that traces back to your own corpus, an existing graph may be the right choice. You get coverage, maintenance by someone else, and a shorter path to value. The tradeoff is that you inherit someone else's design decisions: their entity types, their relationship vocabulary, their choices about what to include and what to leave out. If those align with your use case, that's fine. If they don't, you'll spend time working around them.

**When you need to build.** Several situations push you toward building your own. *Novel domains* -- legal documents, niche scientific subfields, internal corporate knowledge -- often have no suitable public graph. *Proprietary corpora* matter when the knowledge you care about lives in documents you control: internal reports, unpublished studies, patient records, contracts. No public graph will have extracted from those. *Custom schemas* matter when the relationship types and entity distinctions that matter for your reasoning don't match what existing graphs provide. "Treats" and "associated with" are not interchangeable for a clinical decision support system. *Provenance requirements* matter when you need to trace every claim back to a specific source passage, with confidence and evidence type. Many public graphs aggregate without preserving that level of traceability. Building is not always the answer -- but when one or more of these conditions holds, buying often isn't either.

**An honest accounting.** This book is about building. It would be dishonest to pretend that building is always the right choice, or that the approach here is the only one. The goal is to give you the tools to make the tradeoff consciously: to know what you gain by building, what you give up, and when the calculus favors one path over the other.

### What a KG Is Not Good For

A knowledge graph is a powerful tool for certain kinds of reasoning. It is not a general-purpose solution, and overclaiming its virtues does the field no favors.

**Quality reflects sources.** A knowledge graph encodes what is in its sources. If the sources are biased, incomplete, or wrong, the graph will be too. Extraction can introduce additional errors -- misclassified relationships, wrong entity resolutions, spurious connections -- but the ceiling is set by the corpus. A graph built from low-quality literature will not magically produce high-quality knowledge. Garbage in, garbage out applies with full force.

**Coverage gaps are structural.** A graph can only represent what has been extracted. If a domain is under-studied, or if the important relationships are stated in ways the extractor doesn't recognize, the graph will have holes. Those holes are not always obvious: absence of an edge can mean "no relationship" or "we haven't seen it yet." Reasoning over an incomplete graph can produce false negatives -- "the graph doesn't show a connection" is not the same as "no connection exists." Users need to understand the difference.

**Maintenance is ongoing.** Knowledge decays. New papers are published, consensus shifts, drugs are approved or withdrawn, mechanisms are revised. A static graph becomes stale. Keeping it current requires continuous ingestion, schema evolution as the domain evolves, and curation to correct extraction errors and resolve conflicts. This is not a one-time build; it's an ongoing commitment. Organizations that treat a knowledge graph as a project rather than a product often find that the graph drifts out of usefulness within a year or two.

**Bias encodes at scale.** The literature in many domains reflects historical and structural biases: which diseases get studied, which populations are represented in trials, which research questions receive funding. A graph extracted from that literature inherits those biases. Worse, the graph can amplify them -- a pattern that appears in many papers becomes many edges, which makes it look more established than a pattern that appears in few. A knowledge graph is not neutral. It reflects the priorities and blind spots of its sources, and those need to be understood and, where possible, corrected.

## Chapter 4: Representation Is Reasoning

`\chaptermark{Representation Is Reasoning}`{=latex}

### From fluency to grounded reasoning\index{grounded reasoning}

Chapter 1 established that LLMs are fluent but not grounded -- they have no way to gauge correctness or signal uncertainty, and they fail unpredictably when we leave the training distribution. The consequence that matters here: a system reasoning from statistical patterns fails in ways that are opaque, while a system reasoning from explicit, structured knowledge about the domain fails in ways that are traceable, correctable, and bounded by what's in the representation. That distinction is what the rest of this chapter is about.

### Experts have internal knowledge graphs

Here is the argument for knowledge graphs, stated plainly: genuine reasoning about a complex domain requires a representation that makes the structure of that domain explicit, inspectable, and correctable. Not as an engineering convenience. As an epistemological necessity.

But there's a version of this argument that undersells itself, and it's worth avoiding. The weak version says: machines need explicit knowledge representations because they can't do what humans do implicitly. The strong version -- the one worth making -- says: humans need explicit knowledge representations too, for exactly the same reasons, and the best human expertise already has them, just not written down in a form that machines can use.

Think about what it means to be genuinely expert in a complex domain. A working cardiologist doesn't hold the relevant knowledge as a pile of facts. She holds it as a structured web of relationships -- this drug potentiates that pathway, this symptom cluster suggests this differential, this interaction is dangerous in patients with this history. The knowledge is relational. It has direction. It has confidence levels, implicitly -- she trusts the large randomized trials more than the case reports, the established mechanisms more than the preliminary findings. She has, in effect, a knowledge graph in her head, built over years of training and practice. What she doesn't have is an artifact that a machine can query.

The knowledge graph is not a substitute for that expertise. It's an attempt to make its structure explicit -- to take the relational model that the expert has built and put it in a form that can be shared, extended, corrected, and reasoned over by systems that didn't spend fifteen years in medical training. The central argument shifts from "machines need this" to something more interesting: machines and humans are doing the same thing, and now we can make the shared structure visible.

This reframing has a consequence that matters for how you think about the future of the field. The objection that large language models are getting better fast -- that the case for explicit knowledge representation is really just a case for not-yet-good-enough LLMs, and will dissolve as the models improve -- misses the point. A more capable language model reasons better over its training distribution. It does not, by virtue of being larger or better trained, acquire the specific, curated, provenance-tracked model of *this* domain as *this* community of experts currently understands it. That model is constructed through human judgment, domain expertise, and deliberate curation. No amount of training data substitutes for it, because training data reflects the past and the general, while a curated knowledge graph reflects the present and the specific. The cardiologist's knowledge graph, if it existed and were kept current, would contain things that aren't in any published paper yet -- the pattern she noticed last month, the contraindication that her department started flagging based on three recent cases, the consensus that has shifted but hasn't been formally written up. Training data is always behind the frontier of expert knowledge. A living graph doesn't have to be.

### Grounded representation as the fix

Chapter 1 argued that hallucination is baked in, not a bug. The fix is to give the model something to reason *from* -- explicit, structured, checkable claims. A knowledge graph does that: the model is shown edges, sources, and confidence, not asked to retrieve from statistical memory. That's a different cognitive task, and it produces different results.

### Provenance, auditability, trust

A knowledge graph is a model of a domain, not the domain itself. This distinction sounds pedantic until you think about what it implies.

The implicit "model" inside a neural network is also a model of a domain -- or rather, of many domains simultaneously, encoded in weights that are not directly interpretable. It cannot be inspected. You cannot ask the model to show you its representation of the relationship between a drug and its target protein. You cannot correct it when that representation is wrong. You cannot extend it with new knowledge without retraining. You cannot audit it for bias or gaps. The model is a black box\index{black box} with a surface -- you can probe the surface, but the interior is not accessible.

An explicit representation -- a knowledge graph -- is a different kind of thing. It can be inspected. Every entity can be examined, every relationship can be queried, every provenance record can be traced back to its source. When it's wrong, it can be corrected. When the domain changes, it can be updated. When you want to know why the system believes something, you can follow the chain of evidence. Auditability\index{auditability} is not just a nice property -- in any domain where the reasoning matters, it is a requirement. A physician using an AI system to inform a treatment decision needs to be able to ask "why" and get an answer that makes sense. A lawyer relying on an AI-assisted analysis needs to be able to trace the claim to its source. An explicit representation makes this possible. An implicit one doesn't.

The history of knowledge representation in AI is, in one reading, a long argument about this distinction. The expert systems of the 1980s had it right in principle: they reasoned over explicit representations, their inferences were in principle auditable, and when they were wrong you could usually figure out why. What they got wrong was the economics: building and maintaining those representations required armies of knowledge engineers working with domain experts, and it didn't scale. The logic-based systems were brittle because the representations were brittle -- incomplete, inconsistent, and expensive to update. The statistical revolution of the 1990s and 2000s threw out the explicit representation in favor of learned, implicit ones, and gained enormous practical capability at the cost of auditability. The current moment is the first time in the history of the field that it has been practically possible to build explicit, structured, domain-specific representations at scale without armies of knowledge engineers -- because the extraction step, the part that was always the bottleneck, can now be done by a language model with a well-designed prompt.

## Chapter 5: The Extraction Problem

`\chaptermark{The Extraction Problem}`{=latex}

### Humans are smarter than you think

Consider this sentence, something you might find in the cancer literature:

> Patients treated with the combination showed significantly reduced tumor burden compared to controls, though the effect was attenuated in those with prior platinum exposure.

Read it once and you already know, if you have any background in the domain, roughly what it's saying. There's a treatment -- a combination of something, referenced earlier in the paper -- that works against tumor growth. The evidence is significant, which means it cleared a statistical threshold. But the effect is weaker -- attenuated -- in patients who have previously received platinum-based chemotherapy. This is a clinically important qualification: prior platinum exposure is a common history in many cancer populations, so "works, but less well if you've had platinum" is a materially different clinical claim from "works".

Fifty words. A finding, a population, a comparison structure, a statistical hedge, a subgroup qualification, and an implicit clinical contraindication. A human reader with domain knowledge unpacks all of this in roughly the time it takes to read it once.

Now ask what it would take for a machine to do the same.

The finding itself is not stated as a simple subject-verb-object. "Patients treated with the combination" is the subject, but the combination is not named here -- its identity requires reading earlier in the paper, which requires co-reference resolution across sentence boundaries. "Showed significantly reduced tumor burden" is the claim, but "significantly reduced" is a statistical characterization, not a raw observation, and "tumor burden" is a clinical measurement that needs to be recognized as such and linked to its standard definition. "Compared to controls" establishes the comparison structure -- this isn't an absolute claim, it's a relative one, and losing that distinction changes the meaning. "Though the effect was attenuated" introduces hedging -- not a negation, but a qualification. And "prior platinum exposure" names a variable that modulates the effect, which means the machine needs to understand not just that platinum is a drug, but that prior exposure to it is a patient characteristic that interacts with treatment response.

This is not an unusually complex sentence for the biomedical literature. It's representative. And the extraction problem is the problem of reading sentences like this, millions of them, across thousands of papers, and producing structured, typed, provenance-tracked knowledge from them reliably enough to be useful.

### Classical NLP Was Brittle Here

It is worth being honest about what the field of natural language processing actually achieved before large language models arrived, because the temptation to either overstate or dismiss that progress is real.

Named entity recognition\index{named entity recognition (NER)} -- NER\index{NER|see{named entity recognition (NER)}} -- had become genuinely practical by the mid-2010s. Systems trained on annotated biomedical corpora could identify genes, diseases, drugs, and chemicals in text with accuracy that was useful for downstream applications. The BioBERT\index{BioBERT} family of models, pre-trained on PubMed abstracts and fine-tuned for specific tasks, set benchmarks that were hard to dismiss. Co-reference resolution\index{co-reference resolution} -- the problem of knowing that "the compound" in one sentence refers to "imatinib" in the previous one -- made real progress, though it remained brittle on the long-range dependencies that appear routinely in scientific prose. Relation extraction\index{relation extraction} -- identifying that two named entities stand in a specific relationship -- worked well in narrow domains with sufficient training data and carefully defined relationship types.

These weren't failures. They were genuine scientific and engineering progress, and the systems built on them were in production at pharmaceutical companies, biomedical literature services, and research institutions. The field knew what it was doing.

The brittleness showed up at the edges, and the edges were everywhere.

Domain adaptation\index{domain adaptation} was the first wall. A relation extraction system trained on biomedical literature needed to be substantially retrained to work on legal documents. The vocabulary was different, the sentence structures were different, the implicit conventions about how claims were stated were different. This wasn't a matter of fine-tuning a few parameters -- it was, in practice, a research project. You needed new training data, which meant new annotation\index{annotation}, which meant hiring domain experts and building annotation pipelines and managing annotator disagreement. The cycle time from "we want to build a KG in this new domain" to "we have a working extraction pipeline" was measured in months, and the result was never quite as good as you hoped.

The annotation treadmill was the second wall, and it interacted badly with the first. Supervised extraction requires labeled data. Labeled data requires human judgment. Human judgment is expensive, inconsistent, and always slightly out of date. Domain experts disagree about edge cases -- and in complex domains, there are a lot of edge cases. Schemas evolve as understanding improves, which means last year's annotations are partially wrong for this year's schema. The pipeline you trained for the schema you had in January doesn't quite fit the schema you have in June. You annotate more data. You retrain. The schema changes again. The treadmill is always moving.

There was also something more fundamental. Classical NLP worked by learning statistical proxies for semantic relationships -- patterns of words, grammatical structures, co-occurrence statistics that correlated with the relationships you cared about. This worked well when the patterns were consistent and the training data was representative. It worked poorly on hedged language\index{hedging}, because "did not inhibit" and "inhibits" have very similar statistical fingerprints but opposite meanings. It worked poorly on implicit relationships -- the kind where the text doesn't state the relationship directly but a knowledgeable reader infers it. It worked poorly on domain jargon that appeared rarely enough in training data to be statistically invisible. And it worked poorly, structurally, on anything that required integrating information across multiple sentences or multiple documents to establish a single relationship, because most classical architectures had no mechanism for that kind of extended context.

The honest summary: classical NLP built extractors that worked well on the easy cases, degraded gracefully on the medium cases, and failed in ways that were hard to characterize on the hard cases. For many applications, "works well on the easy cases" was sufficient. For building a knowledge graph from a large, diverse scientific literature, it wasn't.

### LLMs Handle It Naturally

Hedging and negation -- the bane of classical systems -- are handled naturally by a model that has learned from an enormous amount of human language, most of which contains hedging and negation. A transformer trained on tens of billions of words has encountered "the effect was attenuated" in hundreds of contexts; it does not confuse attenuation with negation, and it does not fail to recognize that "did not inhibit" means something different from "inhibits". Implicit relationships -- the ones a knowledgeable reader infers rather than reads directly -- are within reach of a model with enough domain knowledge in its training distribution. Cross-sentence co-reference, which defeated most classical architectures, is handled by the attention mechanisms\index{transformer architecture} that are foundational to the transformer architecture. Domain jargon is less of a problem when the model has been trained on a corpus large enough to have seen most of it.

The marginal cost of a new extraction task is a prompt. The cycle from "I want to extract this kind of relationship" to "I have a working extractor" is measured in hours, not months. Schema changes don't require retraining. A domain expert who can't write code can read an extraction prompt, understand what it's asking for, and suggest improvements. That feedback loop -- always important, almost always expensive to close in classical systems -- becomes something you can iterate in an afternoon.

None of this is magic, and it's worth being precise about what it isn't. Hallucination (Chapter 1) takes a specific form in extraction: the model can invent entity names that don't appear in the source, fabricate relationships the text doesn't assert, and misattribute provenance. Validation is not optional. Context windows are finite -- a relationship that spans a section boundary may be missed. And non-determinism\index{non-determinism} -- the same prompt run twice may produce slightly different output -- has implications for reproducibility that any serious pipeline needs to address; caching\index{caching} extraction results is not just an efficiency measure, it's a reproducibility measure.

The rest of the book is the engineering response to these limitations. LLMs are the best tool we have ever had for the extraction problem -- but "best we've ever had" and "good enough to use without careful engineering" are not the same thing, and conflating them leads to pipelines that work in demos and break on real corpora.

# Part II: LLMs Change the Equation

## Chapter 6: LLMs Make This Practical Now

`\chaptermark{LLMs Make This Practical Now}`{=latex}

Chapter 5 closed with the economics argument: the marginal cost of a new extraction task is a prompt, not a research project. That shift is assumed here. This chapter is about what LLMs actually are for extraction purposes, why prompts work as schema binding, what they handle well, and where the remaining limitations are.

### What LLMs Actually Are, For This Purpose

Chapter 1 established what LLMs are not: not databases, not reasoning systems, not reliable reporters of ground truth. They are pattern-completion engines trained on large text corpora, and their outputs are statistically plausible continuations of their inputs, not verified facts. This is the source of hallucination, and hallucination does not go away in the extraction context -- it takes a specific form there that we'll address directly.

What LLMs *are*, for the purposes of extraction, is something more specific and more useful than "a neural network trained on text."

A large language model has, in its training distribution, an enormous amount of human text that includes natural language descriptions of relationships between things: what drugs treat, what genes encode, what historical events caused other historical events, what legal provisions imply, what symptoms suggest. The model has learned, in a diffuse statistical sense, what it means for these relationships to hold -- not as explicit logical rules, but as patterns of co-occurrence, context, and usage that are deeply embedded in the model's weights.

When you write a prompt that says "extract all 'treats' relationships between drugs and diseases from the following text, where 'treats' means a drug is used therapeutically to address a disease," you are not teaching the model what "treats" means. You are binding the model's existing, diffuse understanding of that concept to your schema. The model already has a representation of the difference between "ibuprofen treats headache" and "ibuprofen does not treat bacterial infection." Your prompt tells it that this particular distinction, expressed in terms of your schema's relationship type, is what you want surfaced.

This is what the outline calls "the prompt as schema binding," and it's the conceptual key to why LLM-based extraction works differently from classical systems. You're not training a model to recognize patterns. You're directing a model that already has deep, broad pattern knowledge to apply that knowledge to your specific representational task. The schema description in your prompt is a set of instructions to a very knowledgeable reader, not a specification for a statistical classifier.

The implications of this are large, and we'll work through them in the next section. For now, the key point is that "LLMs understand language"\index{machine understanding} -- a claim that deserves skepticism in many contexts -- is, for the specific task of extraction, a practically useful approximation. The model doesn't need to understand language in the philosophical sense. It needs to be able to identify, in a passage of text, whether a relationship of a given semantic type holds between two given entities. It can do this because it has learned, from an enormous amount of human language use, what those relationships look like when they're present and when they're absent. That's enough.

### The Prompt as Schema Binding\index{prompt engineering!schema binding}

The central practical difference between classical NLP extraction and LLM-based extraction is this: in classical systems, the schema is baked into the model architecture and the training data. In LLM-based systems, the schema is in the prompt.

This sounds like an implementation detail. It isn't.

When the schema is baked into the model, changing the schema means changing the model. New entity types require new training data and new training runs. Renamed relationship types confuse a model trained with the old names. Distinctions that turned out to matter -- the difference between "directly inhibits" and "allosterically inhibits," say, if that distinction turns out to be clinically significant for your application -- require new annotations and new training. The schema is frozen at training time, and thawing it is expensive.

When the schema is in the prompt, changing the schema means changing the prompt. You add a new entity type by describing it. You clarify a relationship type by adding a sentence that explains the distinction. You can make these changes and run an extraction batch within the hour to see how the change affects output quality. Schema evolution, which any serious knowledge graph project will go through, stops being a recurring research project and becomes a routine iteration loop.

The other consequence is that schema design becomes a collaborative, legible activity. A classical NLP pipeline encodes schema decisions in training data and model weights that domain experts can't directly inspect or critique. A prompt encodes schema decisions in natural language that anyone who can read can evaluate. A cardiologist reviewing a proposed schema for a cardiovascular knowledge graph can read a well-written extraction prompt, notice that the distinction between "increases risk of" and "causes" is not being drawn, and say so. She doesn't need to understand machine learning. She needs to understand her domain, and she does.

This changes the knowledge engineering relationship in a way that the classical systems never managed. The expert systems of the 1980s aspired to this: the vision was always that domain experts would be able to inspect and correct the knowledge base. The execution required knowledge engineers as intermediaries, because the representation languages were not natural language. LLM-based extraction achieves, in the extraction domain, what the knowledge engineers were supposed to achieve in the representation domain: it removes the translation layer between what domain experts know and what the system can use.

There are limits. Prompts that ask for overly subtle distinctions -- semantic differences that would challenge even a careful human reader -- produce inconsistent output. Prompts that are ambiguous produce ambiguous extractions. The quality of the schema description in the prompt directly determines the quality of the extraction output, and "write a good schema description" is harder than it sounds; the whole of Chapter 10 is devoted to it. The point is not that prompts are easy to write, but that the feedback loop between "what I described" and "what I got" is short enough to be useful.

### Handling What Classical Systems Couldn't

Let's be concrete about the specific failure modes of classical NLP extraction that LLMs handle well, because "LLMs are better at language" is too vague to be useful.

**Hedging and negation.**\index{negation} The sentence "drug X did not inhibit pathway Y in this model" contains an "inhibits" relationship that is negated. A classical relation extraction system trained to recognize inhibition relationships would frequently fire on this sentence anyway, because "did not inhibit" and "inhibits" look statistically similar. The word "not" is short and common enough to be underweighted in most feature representations. A large language model, prompted to extract inhibition relationships and to exclude negated ones, handles this correctly in the vast majority of cases. The model has learned from an enormous amount of text that negation changes meaning, and it applies that knowledge. This is not a small improvement: negated relationships are common in scientific literature, and a graph that includes them as positive edges is systematically wrong in ways that are hard to detect.

**Hedged claims.** Related but distinct. "Drug X may inhibit pathway Y" and "drug X inhibits pathway Y" are different claims with different epistemic weights. Classical systems often collapsed these into the same extraction, losing the hedge. A prompted LLM can be instructed to track hedging as part of the provenance record -- to note whether a claim is stated as fact, hypothesis, or speculation -- and it will do so with reasonable consistency. This is directly relevant to provenance design, which Chapter 8 covers.

**Implicit relationships.** Some relationships are never stated directly in the text but are clear to a knowledgeable reader. "Patients receiving drug X showed a 40% reduction in tumor burden compared to controls" does not contain the word "treats." It asserts, in the language of clinical reporting, that drug X has therapeutic activity against the relevant tumor type. A classical system without an explicit "treats" pattern for this construction would miss it. A large language model, prompted to extract treatment relationships and given a description of what counts as evidence for one, will recognize this as an instance of the pattern. This matters a great deal in biomedical literature, where direct assertions are often replaced by results-focused constructions that any domain expert reads as making a relational claim.

**Cross-sentence dependencies.** "The compound was tested against a panel of cancer cell lines. It showed selective activity against BRCA1-mutant cells, with IC50 values in the nanomolar range." These two sentences together assert a relationship -- the compound has activity against a specific molecular subtype of cancer -- that doesn't fully exist in either sentence alone. Classical architectures with limited context windows would process each sentence independently and might miss the connection. A large language model operating over both sentences simultaneously -- or, in the chunking strategies we'll cover in Chapter 10, over a passage that includes both -- will recognize the implicit antecedent and extract the relationship correctly.

**Domain jargon.** A drug referred to by a trial identifier, a gene referred to by a lab-specific shorthand, a syndrome referred to by the name of its first describer -- these appear constantly in specialist literature and were frequently invisible to classical systems trained on corpora where the standard terminology dominated. LLMs trained on broad scientific text have seen a much wider range of how concepts are referred to, and they tolerate terminological variation better. This isn't complete -- genuinely novel terminology, or highly specialized jargon outside the training distribution, can still cause failures -- but the robustness is substantially better.

None of these improvements mean that LLM extraction is reliable without engineering. They mean that the specific failure modes that made classical extraction brittle in complex domains are substantially mitigated. The failure modes that remain are different in character, and the engineering response to them is different.

### The Remaining Limitations, Honestly

Chapter 1 established hallucination as a structural feature of LLMs, not a bug. Chapter 5 was honest about what classical NLP couldn't do. This chapter should be equally honest about what LLMs can't do, because the engineering in Part III is largely a response to these limitations.

**Hallucination in extraction.** The model can invent entity names that don't appear in the source text. It can assert relationships that the text implies but doesn't actually support. It can misattribute provenance, assigning a claim to a passage that doesn't contain it. These are not rare edge cases -- they occur with meaningful frequency even in well-prompted models, and the frequency increases as the task gets harder (more complex sentences, more ambiguous relationships, longer passages). Validation against the source is not optional. Chapter 12 covers the validation pipeline.

**Context window limits.**\index{context window} Scientific papers are often tens of thousands of words. The relationships that matter may span sections written pages apart -- an introduction that defines a hypothesis, a methods section that describes a test, a results section that reports an outcome. The model's context window is finite, and even the largest current context windows don't fully solve this problem; performance tends to degrade on information that appears far from the relevant extraction target within a long context. The chunking\index{chunking} strategies in Chapter 10 are a pragmatic response: break documents into manageable passages, extract relationships within each, and handle cross-chunk dependencies with a separate pass. This works, but it introduces its own complications, including relationships that span chunk boundaries and may be missed.

**Cost at scale.** A single extraction call against a single paper costs a small amount. Across a corpus of hundreds of thousands of papers, the cost accumulates. The economics are better than classical NLP at the prototype scale -- dramatically so -- and require more careful management at production scale. Caching, batching, and tiered extraction (do cheap passes first, expensive passes only where needed) are all part of managing this.

**Non-determinism.**\index{non-determinism} The same prompt, run twice against the same text, may produce different output. This matters for reproducibility: if your pipeline produces different graphs on different runs, it's difficult to debug, compare, and maintain. Caching extraction results addresses this directly and is both an efficiency measure and a reproducibility measure.

**What the model knows and doesn't know.** LLM extraction reflects what the model learned from its training data. Very recent developments, highly specialized terminology that appears rarely in broad scientific text, and concepts that are standard in one community but not in the general scientific literature can all cause degraded performance. In practice, this means that extraction quality should be evaluated on your specific domain and corpus, not assumed from general benchmarks.

The point of this honest accounting is not to undercut the argument that LLMs make knowledge graph construction newly practical. They do. The point is that "newly practical" means "practical if you engineer it carefully," not "practical if you just call the API." Part III is the careful engineering.

### Why This Moment

One more question deserves an answer before we get into the engineering: why now? The transformer architecture was introduced in 2017. GPT-2 was released in 2019. Why is this moment -- roughly 2023 through the present -- the right time to build?

The answer is the convergence of three things that had to arrive together.

The first is model capability. The capability of general-purpose language models for complex semantic understanding crossed a threshold somewhere around the GPT-4\index{GPT-4} generation. Before that threshold, prompted extraction was possible but brittle on complex constructions; after it, the failures became manageable with good engineering. Earlier models were impressive but required more hand-holding. Current models handle the hard cases -- hedging, negation, implicit relationships, cross-sentence dependencies -- with the consistency needed for production pipelines.

The second is API accessibility. Using a capable language model for extraction before the current generation of public APIs meant running your own infrastructure, which meant GPU clusters, model serving, and the full operational stack. This was possible for large organizations; it wasn't feasible for a researcher, a small company, or an individual practitioner. The existence of stable, affordable, well-documented APIs for capable models changes who can build this. You don't need infrastructure. You need an API key and a credit card to get started.

The third is the tooling ecosystem. The infrastructure for building knowledge graph pipelines -- graph databases with native support for the relevant query patterns, databases for similarity-based lookup, orchestration frameworks for multi-step LLM pipelines -- arrived, matured, and became accessible at roughly the same time as the models. A knowledge graph pipeline in 2020 would have required assembling a stack of immature tools and writing substantial infrastructure code. Today the stack exists and the components are well-documented.

These three things had to be true simultaneously, and they are now. That matters for the argument this book is making. This is not a forecast that something will soon be possible. This is a description of what is possible today, and the rest of the book is how to do it.

There is also a fourth consideration that is more speculative but worth naming. We are at an early moment in the adoption of this capability. The knowledge graphs that will have the largest impact on medicine, law, materials science, and other complex domains don't exist yet. The tooling is new enough that best practices are still being established. The organizations that will benefit most from these systems are still figuring out that this is possible. The researchers who will do the most interesting work with these systems haven't started yet.

Early maps of large territories are valuable precisely because they're early. What follows in this book is one such map, drawn from working code and real corpora. It's not complete. It's not the last word. But the territory is real, the tools are here, and the problems are interesting.

## Chapter 7: The Free KG Cases

`\chaptermark{The Free KG Cases}`{=latex}

Not every knowledge graph requires extraction. Some are built from sources that are already structured when they arrive -- from lab instruments, databases, ontologies, or human-curated encyclopedias. Understanding these "free" cases sharpens the argument for extraction by making clear what the hard problem actually is. It also sets a quality benchmark: the graphs built without extraction tend to be high-precision over their coverage, precisely because the structure was already there. The extraction problem is the problem of accessing the knowledge that *wasn't* structured -- and in most interesting domains, that's the majority of what's known.

### When You Don't Need Extraction

The central claim of this book is that extraction from unstructured text is the bottleneck that has limited knowledge graphs for decades, and that LLMs have finally made it tractable. But that claim only applies when the knowledge lives in unstructured form. In many situations, the knowledge is already structured when it reaches you, and extraction to a knowledge graph is simply a mechanical reformatting, perhaps a short shell or Python script. Structured web sources (schema.org markup, government open data) and well-documented APIs fall into the same category.

Perhaps the data comes from lab equipment that outputs well-defined records -- a sequencer, a spectrometer, a sensor network. Perhaps it comes from a database table with columns and foreign keys. Perhaps it comes from an ontology or formal specification that was designed to be machine-readable from the start. In these cases, the mapping from source to graph is often straightforward: a short script, an ETL pipeline, or a direct translation of the source schema into graph form. No LLM is required. No extraction prompt. No ambiguity about what the text meant. The structure is given.

This chapter examines several such cases. The goal is not to dismiss them -- they are important and widely used -- but to clarify the boundary. When does a knowledge graph require extraction, and when does it not? The answer determines whether the techniques in the rest of this book apply to a reader's problem, and it also illuminates what extraction is *for*: bridging the gap between the knowledge that is already structured and the knowledge that is not.

The practical question is: which case are you in? A few signals help.

If your domain has established, maintained, machine-readable authorities -- ontologies, registries, curated databases -- and your knowledge questions can be answered from those sources alone, you may not need extraction at all. The authority is the graph, or close enough that a mapping script is all that stands between them.

If your domain's knowledge lives primarily in structured form but you need to connect across sources -- linking a genomics database to a drug database to a clinical outcomes registry -- you need identity resolution and schema alignment, but not LLM-based extraction. The challenge is integration, not interpretation.

If the knowledge you need is in the literature -- in the prose of papers, reports, case notes, specifications -- then extraction is not optional. The structured sources don't have it. The only way to get it into the graph is to read the text and interpret it, and that is what the rest of this book is about.

Misidentifying your case is expensive in both directions. Building an extraction pipeline for a domain where structured authorities already cover your needs wastes time and introduces noise you didn't have to create. Assuming a structured source covers your domain when the real knowledge lives in the prose means building a graph with systematic blind spots you may not notice until a user asks the wrong question.

### Lab Instruments and Measured Data

Genomics provides the canonical example. DNA sequencers, mass spectrometers, and high-throughput assay platforms produce structured data almost by definition. A sequencer outputs base calls with quality scores; a protein-protein interaction assay outputs pairs of identifiers with confidence metrics. The data has a schema. It has identifiers that map to established ontologies. It can be loaded into a graph with minimal interpretation.

Graphs like STRING\index{STRING database} (protein-protein interactions), BioGRID\index{BioGRID} (genetic and physical interactions), and IntAct\index{IntAct} (molecular interactions) are populated primarily from such experimental measurements. They aggregate data from thousands of published studies, but the aggregation is over structured datasets that the authors deposited in repositories -- not over the free text of the papers. The extraction problem, in this context, is largely solved by the experimental design: the scientist produces structured output, and the graph ingests it.

What these graphs are good for is clear. They support queries like "what proteins interact with BRCA1?" or "what pathways involve this gene?" with high precision, because the edges correspond to actual experimental observations. What they miss is equally important: the experiment that wasn't done, or wasn't published as structured data, or was described only in the discussion section of a paper, is not in the graph. The knowledge that lives in the prose -- the mechanistic interpretation, the caveats, the connections to other domains that the authors didn't formalize -- remains inaccessible. For many biomedical questions, that's the majority of what's known. Lab instruments and measured data give you a high-quality graph over a subset of the domain.

### Generated and Synthetic Graphs

A related class of knowledge graphs is constructed from databases, ontologies, or formal specifications rather than from text or instruments. The Gene Ontology\index{Gene Ontology} is a curated hierarchy of molecular function, biological process, and cellular component terms -- it is a graph by design, with typed relationships (`is_a`, `part_of`, `regulates`) between terms. Drug interaction databases like DrugBank\index{DrugBank} or STITCH\index{STITCH} map drugs to targets, indications, and interactions using structured records. Legal code can be represented as a graph of sections, references, and amendments. In each case, the source was already formal enough that conversion to graph form is a matter of schema mapping, not interpretation.

The precision of these graphs is high. When a relationship is asserted in the Gene Ontology, it has been reviewed by curators and validated against evidence. When a drug-target interaction appears in DrugBank, it has been extracted and verified by the database maintainers. The boundary between a knowledge graph and a very well-structured relational database starts to blur here -- and that blurriness is instructive. A graph is often just a different view of the same data, with traversal and path-finding as the primary operations instead of joins and aggregations.

The limitation is coverage. These graphs contain what was explicitly encoded. They do not contain what was left implicit, or what was stated in natural language and never formalized, or what was discovered after the last curation pass. For domains where the authoritative knowledge is already in structured form, that may be sufficient. For domains where the knowledge lives in the literature, it is not.

### Curated Graphs at Scale

Wikidata,\index{Wikidata} Freebase\index{Freebase} before it, and DBpedia represent a different model: human curation at scale. Millions of entities, millions of relationships, maintained by a community of contributors who add facts, correct errors, and resolve disputes through discussion and consensus. The result is a graph that spans many domains, with reasonable quality where the community has focused effort, and gaps where it has not.

A single query can retrieve structured information about a person, a place, a chemical, a historical event -- with identifiers that are stable, with relationships that are typed, with provenance that points to sources. For many applications, that is enough. The cost is the cost of human labor: curation does not scale to the full breadth of human knowledge, and it scales least well to domains where the knowledge is technical, specialized, or rapidly evolving. Encyclopedia articles can be curated. The full text of the medical literature cannot.

DBpedia\index{DBpedia} illustrates the boundary clearly. It is extracted from Wikipedia infoboxes and structured elements -- but the extraction is from semi-structured templates, not from free prose. The infobox for a drug might have a "mechanism" field; the body of the article might have three paragraphs of nuanced explanation that never made it into the template. DBpedia has the former. It does not have the latter. Curated graphs at scale work where the community can structure the knowledge. They do not work where the knowledge lives in papers, reports, and documents that no one has the bandwidth to formalize.

### What These Cases Teach Us

The common thread across lab instruments, generated graphs, and curated encyclopedias is this: structured sources give you high-precision graphs over the knowledge that was *already structured*. The extraction problem is precisely the problem of accessing the knowledge that *wasn't* -- which, in most interesting domains, is the majority of what's known.

The free KG cases set a quality benchmark worth aiming for. When a graph is built from structured sources, the edges tend to be correct, the entities tend to be well-identified, and the schema tends to be coherent. An extraction-based graph should aspire to that level of precision where it can. The gap between that benchmark and what extraction typically achieves is the gap that schema design, prompt engineering, and pipeline architecture are trying to close.

The free cases also illustrate the shape of the gap. It is not that extraction is impossible or that extracted graphs are inherently low quality. It is that extraction is a different kind of problem -- one that requires interpreting natural language, resolving ambiguity, and making judgments about what the text implies. The tools for that problem have improved dramatically. The problem itself has not gone away.

The gap is worth being specific about. A structured-source graph rarely has a wrong relationship direction -- the schema defines which way an edge runs and the data conforms. An extracted graph will have some inverted edges, particularly for asymmetric relationships stated in passive voice. A structured-source graph has stable entity identity -- the authority assigns the ID and it doesn't drift. An extracted graph has provisional entities that may be duplicated, merged incorrectly, or resolved differently across pipeline runs. A structured-source graph has relationships with known epistemic type -- a DrugBank interaction is always a curated assertion, not a model inference. An extracted graph mixes extraction confidence levels, and the metadata that tracks them requires deliberate schema design to preserve. None of these gaps are fatal. They are all addressable by the architecture in Part III. But they are real, and knowing they exist is what motivates the engineering choices ahead.

### Hybrid Approaches

Most real knowledge graphs combine extraction with structured sources. The typical pattern: extract entities and relationships from text, then link the extracted entities to authoritative identifiers from a curated database or ontology.\index{hybrid knowledge graph} A drug mention in a paper is resolved to an RxNorm code. A disease mention is resolved to a MeSH term. A gene mention is resolved to an HGNC identifier. The extraction provides the coverage -- the connections that appear in the literature. The authority lookup provides the identity -- the canonical form that makes those connections comparable across sources.

This hybrid approach does not make the extraction problem go away. It constrains it. Instead of inventing identifiers from scratch, the extractor (or a downstream resolution pass) maps to an existing vocabulary. That mapping is itself a form of extraction -- the model must recognize that "ketoconazole" in the text refers to the same thing as RxNorm's concept for ketoconazole -- but it is a narrower problem than inventing a full schema and populating it from scratch. The schema, or at least the entity vocabulary, is given by the authority. The extraction fills in the relationships and the provenance.

The medical literature example in Part III follows this pattern. Entities are extracted from papers and resolved to MeSH, HGNC, RxNorm, or provisional IDs when no authority match exists. The Gene Ontology and other ontologies provide a backbone for relationship types. The result is a graph that combines the coverage of extraction with the identity resolution of curated sources. It is not a free KG -- extraction is central -- but it is not a purely extracted KG either. The hybrid is the norm, and understanding both the extraction side and the structured side is necessary to build one well.

### The Goal

The free KG cases are not a detour. They are the target.

The chapters that follow describe how to build a knowledge graph from unstructured text -- how to design a schema, run an extraction pipeline, resolve entity identity, track provenance, and serve the result. That engineering is substantial. But the reason to do it carefully is precisely that you want to arrive somewhere close to where the free cases already are: high-precision edges, stable entity identities, queryable provenance, confident relationship types. The structured sources set the standard. Extraction is the attempt to meet that standard in the domains where structured sources don't reach.

That gap -- between what the structured sources cover and what the literature knows -- is where the most interesting knowledge lives. The well-curated ontologies cover the established, the agreed-upon, the formalized. The literature covers the recent, the contested, the preliminary, the cross-disciplinary connection that nobody has formalized yet. A graph built from extraction can in principle reach all of it. Whether it reaches it at the quality level required for reliable reasoning depends on the decisions in Parts II and III.

This is the bridge the chapter is standing on. Behind it: decades of attempts to build knowledge representations, the bottleneck that stopped them, and the LLM-based tools that finally make extraction tractable. Ahead: the engineering of a system that tries to capture the knowledge in the text at a quality level worth reasoning over. The free cases show what that looks like when you get there.

## Chapter 8: Designing Your Schema

`\chaptermark{Designing Your Schema}`{=latex}

This is the chapter that might surprise readers who came for the engineering. Schema design is not primarily a technical exercise. It is where decisions are made about what the domain *is* -- what counts as an entity, what kinds of relationships matter, what level of granularity is useful. These are epistemological decisions, and they determine everything downstream. A poorly designed schema will produce a graph that cannot support the reasoning it was built for, no matter how good the extraction pipeline. A well-designed schema makes extraction easier, validation straightforward, and evolution manageable.

### Schema Design as Intellectual Work\index{schema design}

The temptation is to treat schema design as a matter of picking entity types and relationship names from a list -- a checklist exercise that can be delegated or done quickly. That approach produces schemas that look reasonable on paper and fail in practice. The real work is understanding the domain well enough to know what distinctions matter for the questions the graph will answer.

Consider a medical literature knowledge graph. Should "dosage" be an entity type or a property of a relationship? If it's an entity, the graph can support queries like "what dosages of this drug have been studied?" and "how do recommended dosages vary across indications?" If it's a property, those queries become harder or impossible. The decision depends on what the graph is for. A graph built to support drug repurposing might not need dosage as an entity; a graph built to support clinical decision support might need it badly. There is no universal right answer. The schema must reflect the use case.

The same applies to relationship types. "Inhibits" and "is associated with" are not interchangeable. One supports reasoning about mechanism; the other supports retrieval but not much else. The schema designer must decide how fine-grained the relationship vocabulary should be -- fine enough to support the intended reasoning, coarse enough that extraction can reliably distinguish the types. That balance is domain-specific and use-case-specific. It cannot be looked up in a reference. It has to be thought through.

### Entities: What Gets to Be a Thing

The question of what deserves a node in the graph is foundational. Genes, drugs, diseases, symptoms, procedures, proteins, pathways, patient populations, study designs -- which of these are entities and which are properties of entities? The answer is neither obvious nor universal. It depends on the questions the graph is meant to answer.

A useful heuristic: an entity is something that can be referred to across multiple sources and that can participate in relationships as a subject or object. "Breast cancer" is an entity because it can be the subject of "is treated by" and the object of "targets." "50 mg" is typically a property -- it describes a dosage, but it does not itself have relationships to other things in the same way. The boundary is not always sharp. "Cohort of postmenopausal women" might be an entity if the graph needs to reason about study populations; it might be a property of a study if the graph only needs to retrieve studies by population criteria.

The medical literature example makes specific choices: Disease, Drug, Gene, Protein, Symptom, Procedure, Publication, and a few others. Evidence is an entity -- not just a property of a relationship, but a node with its own identity, because provenance needs to be queryable and traversable. The reasoning behind each choice is worth examining. Genes and proteins are both entities because the literature distinguishes them and the relationships differ -- a drug might target a protein but regulate a gene. Symptoms are entities because they connect to diseases in ways that matter for differential diagnosis. The schema reflects the structure of the domain as it appears in the sources.

### Relationships: Meaning and Direction\index{relationship direction}

The difference between "co-occurs with," "inhibits," "causes," and "is associated with" is enormous. Collapsing them into a single "related to" type produces a graph that can support retrieval but not reasoning. The graph can answer "what is connected to this drug?" but not "what does this drug inhibit?" or "what causes this symptom?" The relationship type carries the meaning. Lose the type, and you lose the ability to reason from it.

The tradeoff is between semantic precision and extraction recall. Relationship types that are too generic -- "associated with" -- are easy to extract and never wrong, but they are almost never useful. Relationship types that are too narrow -- "allosterically inhibits" versus "competitively inhibits" -- may be impossible for an extraction model to distinguish reliably. The right level is where the types are meaningfully distinct, expressible in natural language to the model, and actually present in the sources. That level varies by domain. It is discovered through iteration, not specified in advance.

Direction matters as well. "Drug A treats Disease B" and "Disease B is treated by Drug A" are the same fact, but in a directed graph they are different edges. Consistency across extraction runs and across sources requires that direction be part of the type definition -- not a convention but a constraint. The schema should specify, for each relationship type, what the subject and object types are and which way the relationship points. That discipline prevents the subtle errors that accumulate when direction is left implicit.

### Hierarchy and Inheritance\index{entity hierarchy}\index{inheritance (schema)}

When should entity types form a hierarchy, and when is a flat list better? A hierarchy allows "Protein" to be a subtype of "Gene product," which allows queries over all gene products to include proteins. It also adds complexity: the extractor must decide whether a mention is a protein or a gene product, and the schema must define the inheritance rules. For some domains, that complexity pays off. For others, a flat list of types is simpler and sufficient.

The temptation to over-ontologize is real. Elaborate taxonomies look impressive and suggest rigor. They also make extraction harder -- the model must choose among many similar types -- and they can make the graph harder to query if the hierarchy is deep and the inheritance semantics are unclear. The principle: add hierarchy only when it supports reasoning that a flat schema cannot. If the main use case is "find all entities of type X," and X is a leaf in the hierarchy, the hierarchy may not be earning its keep.

### Provenance as a First-Class Schema Concern

Chapter 3 argued that provenance is essential -- that every claim in a knowledge graph needs to be traceable to its source, with confidence and evidence type. In schema design, that argument becomes concrete. How is provenance represented? Is it a property on each edge? A separate entity type? A linked structure of evidence nodes?

The choice affects everything downstream. If provenance is a property, it is easy to add but hard to query across sources. If it is an entity type, it becomes traversable: "show me all evidence for this relationship" becomes a graph query. The medical literature example uses evidence as an entity -- each piece of evidence is a node with its own identity, linked to the relationship it supports. That design makes it possible to aggregate evidence across sources, to filter by confidence, and to detect when two sources conflict.

The fields that are often regretted later, when they were not included from the start: source document, section, passage offset, extraction method, confidence score, evidence type (e.g., RCT vs. case report). Adding them after the fact requires backfilling or accepting that older extractions lack them. Designing them in from the beginning avoids that debt.

### Designing for Extraction

Schema choices affect how easy or hard extraction is. Some relationship types are natural to express in language -- "treats," "causes," "inhibits" -- and extraction models handle them well. Others are awkward -- "has mechanism" or "exerts effect via" -- and the model may struggle to recognize them consistently. Entity types that are genuinely ambiguous even to a human reader -- is "oxidative stress" a process or a condition? -- will produce inconsistent extraction no matter how good the prompt.

The feedback loop between schema design and extraction quality is tight. A schema that is easy to extract from will produce better results. A schema that is hard to extract from will produce noise, and the natural response is to simplify the schema -- which may sacrifice the reasoning capability the graph was built for. The alternative is to iterate on both together: adjust the schema when extraction consistently fails on a type, and adjust the extraction prompt when the schema is right but the model is not. Finalizing the schema before extraction begins is often a mistake. The schema and the extraction prompt should co-evolve.

### Designing for Evolution\index{schema evolution}

The schema will change. New entity types will be needed that were not anticipated. Relationship types will turn out to be too coarse or too fine. Distinctions that seemed unimportant will matter more than expected. The question is how to design so that evolution is manageable rather than catastrophic.

Versioning\index{schema versioning} helps. When the schema changes, the extraction output format changes, and downstream consumers need to know which version they are looking at. A manifest or metadata that records the schema version with each bundle or each graph snapshot makes it possible to migrate incrementally and to reason about compatibility.

Migration is the hard part. Adding a new entity type is usually straightforward. Splitting an existing type, or changing the semantics of a relationship, can require backfilling or re-extraction. The argument for keeping the schema as simple as possible for as long as possible is practical: every entity type and relationship type is a commitment. Add only what is clearly needed. Defer the rest until the need is demonstrated.

A single source of truth for domain specifics pays off here. In the medlit reference implementation, this is `domain_spec.py`\index{domain\_spec.py}: entity types, predicates, prompt instructions, and vocabulary guidance all defined in one place. The extraction prompt, validation logic, and deduplication rules all import from it. A change in one place propagates everywhere; there is no second copy to forget. Splitting these across YAML configs, Python code, and prompt templates invites drift: an entity type added in one file is forgotten in the prompt, or a predicate constraint tightened in the schema is not reflected in the dedup stage, or an entity type added to the schema but forgotten in the extraction prompt produces silent gaps. One module, one edit, no drift. Readers building their own systems will find that maintaining a single domain specification module -- whether in code, config, or a schema language -- reduces the class of errors that come from inconsistent copies of the same information.

# Part III: Building It

## Chapter 9: Diagnostic Tools

`\chaptermark{Diagnostic Tools}`{=latex}

The single most valuable diagnostic tool is a good visualization of the graph. Force-directed layout -- where nodes and edges are treated like masses and springs floating in a 2-D space -- makes structural problems legible before they surface in logs. A well-designed graph explorer does more than render nodes and edges; it gives you the controls to interrogate what you've built and diagnose what's in it.

### Force-Directed Visualization\index{graph explorer}\index{D3.js}

The medlit reference implementation uses the D3.js\index{D3.js} force layout. Nodes are colored by entity type, edges carry relationship labels, and clicking a node opens a detail panel. At a glance you can see whether the graph has the expected topology: well-connected disease and drug nodes, distinct clusters by domain, bridges between subfields. Zoom, pan, and reset complete the interface.

![](GraphVisualization.png)

**Entity type legend and color coding.** Nodes colored by entity type -- disease, drug, gene, protein, symptom, procedure -- make the graph interpretable at a glance. You can see whether a subgraph is dominated by one type, whether the expected mix is present, and whether any node is misclassified. A gene colored as a disease, or a drug colored as a symptom, is an extraction error that becomes visible immediately.

**Relationship labels on edges.** The edges should show their predicate types: "treats," "inhibits," "causes," "associated with." That visibility is diagnostic. You can spot relationships that are too generic ("associated with" everywhere suggests the extraction prompt is not distinguishing types) or predicates that are wrong for the domain.

**Clicking a node** opens its full metadata: canonical ID, entity type, synonyms, source papers, confidence scores. The canonical ID should link directly to the authority source -- `MeSH:D000072716` to the MeSH Browser, `HGNC:4556` to the HGNC gene page -- turning the detail panel into a live bridge between your graph and the sources it draws from. Provisional entities with `prov:` IDs display as plain text.

**Live statistics.** Node count, edge count -- these numbers give an immediate sense of density. Unexpectedly low counts can indicate extraction gaps or resolution failures; unexpectedly high counts can indicate over-merging or spurious extraction.

### What to Look For\index{deduplication!visual diagnosis}

Force-directed layout reliably surfaces several classes of problem:

**Duplicate nodes** appear as pairs or clusters with near-identical labels that should have resolved to one entity. A disease called "T2DM" and another called "Type 2 diabetes" sitting as separate nodes means your synonym cache or authority lookup did not merge them. The visual makes this obvious; scanning `entities.jsonl` for it would not.

**High-degree hubs** that shouldn't exist often indicate an under-specified entity type. If one "process" node connects to fifty drugs and thirty genes, it may be absorbing mentions that should have resolved to several distinct entities.

**Disconnected components** -- islands of nodes with no edges to the rest of the graph -- suggest extraction gaps. Either the relevant relationships were not extracted, or the entities in that cluster failed identity resolution and are sitting as orphaned provisionals.

**Predicate distribution anomalies.** If the great majority of edges carry "associated with" rather than more specific predicates, the extraction prompt is probably not steering the model toward the predicate vocabulary you defined.

### Visualization as Pipeline Signal

The visualization is not just a display layer -- it is a diagnostic instrument that surfaces pipeline failures before they appear in logs. Unexpectedly long evidence spans, malformed relationship metadata, and identity resolution failures all produce visible anomalies: a sprawling hub where a tight cluster should be, a node with no edges that should be central, or a pair of nodes that should be one.

The feedback loop is tight during development: run a small extraction batch, load it into the visualization, identify what looks wrong, adjust the prompt or schema, repeat. This is faster than unit-testing every failure mode in advance. The visualization makes "is this working?" a question you can answer by looking.

![](MetadataView.png)

## Chapter 10: Design Priorities

`\chaptermark{Design Priorities}`{=latex}

This chapter examines the design decisions that matter most before you start building — specifically around provenance, which is the one you're most likely to underinvest in and most painful to retrofit. The examples are drawn from my own project, a knowledge graph to capture the contents of medical papers. I call this project "kgraph" in its domain-agnostic form, and "medlit" is the extension of the knowledge graph into the domain of medical literature.

These notes should be regarded not as a recipe or specification that you must follow, but rather as a checklist of things worth considering. The approach suggested here might meet your needs, it might not. Thinking about them will help you reason through the details of your own design.

### Provenance

Provenance is not equally important in every domain. Be honest with yourself about how much provenance infrastructure your domain actually requires before you build it.

In medicine, the difference between "this drug inhibits this enzyme, from a single case report" and "this drug inhibits this enzyme, replicated across forty randomized controlled trials" is the difference between a hypothesis and a clinical fact. A clinician making a treatment decision needs to know which. A researcher generating hypotheses might care less about the evidence grade and more about the structural pattern. But for any application where the quality of the claim matters -- clinical decision support, regulatory submission, litigation -- provenance is not optional. You need to know where each relationship came from, what kind of study supported it, and how confident the extraction was.

In other domains, the bar is lower. A knowledge graph of theatrical productions -- which plays were performed where, when, by whom -- might be perfectly useful without tracing every edge to a specific source. If the graph says "Hamlet was performed at the Globe in 1601," you might care that it's correct, but you probably don't need a provenance record that distinguishes "extracted from a primary source" versus "extracted from a secondary source" versus "inferred from context." The graph is useful even if you can't trace every edge. Building elaborate provenance infrastructure for a domain that doesn't need it is over-engineering.

The honest question: what will your users do with the graph? If they will make high-stakes decisions based on it, provenance matters. If they will use it for exploration, discovery, or casual reference, a lighter touch may suffice. Get that right before you invest in schema design and pipeline complexity.

When provenance does matter, it matters at an architectural level, not as an add-on. You can't retrofit provenance into a schema that didn't anticipate it without re-ingesting your corpus. The relationship model, the bundle structure, and the extraction prompts all need to capture provenance from the start. Think about it carefully before you build.

When it matters, it matters a lot. A relationship with provenance -- specific source document, section or passage, extraction method, confidence score, study design if applicable -- is evidence. Without provenance, a relationship in your graph is an assertion of unknown quality. You can't verify it. You can't weight it against conflicting claims. You can't explain to a user why the graph says what it says. You're left with "the graph says drug A treats disease B" and no way to assess whether that's a well-replicated finding or a single speculative mention.

Provenance is also what lets you audit extraction quality. When a relationship looks wrong, you need to trace it back: which document, which passage, what did the extractor see? That trace is how you find prompt bugs, schema ambiguities, and source documents that are genuinely ambiguous. Without it, you're debugging in the dark.

It's also how you debug pipeline regressions. If extraction quality drops after a prompt change, provenance lets you compare: what did the old pipeline produce for this document versus the new one? Which relationships disappeared, which appeared, which changed? Provenance turns "something got worse" into "here's exactly what changed and where."

And it's how you answer the question every serious user will eventually ask: "Why does the graph say this?" A graph that can't answer that question is a black box. A graph that can produce, for any relationship, the list of sources that support it, with enough detail to verify, is a tool you can trust.

### Confidence as a Signal, Not a Guarantee\index{confidence score}

LLMs can be prompted to produce confidence scores alongside their extractions. "How confident are you that this relationship holds, on a scale of 1 to 5?" The model will give you a number. That number is useful. It correlates with extraction quality: relationships the model is confident about tend to be more reliable than ones it's uncertain about. You can use it to filter, rank, or weight results. It's worth capturing.

It is not a calibrated probability. A model that says "90% confident" does not mean that 90% of such extractions will be correct. The model has no access to ground truth; it's producing a subjective assessment of its own certainty, which is a different thing. The scores are ordinal -- higher usually means more reliable -- but the mapping from score to actual accuracy is unknown and varies by domain, relationship type, and prompt.

The honest framing: confidence is one input to trust, not trust itself. A high-confidence extraction from a single case report is still weak evidence. A low-confidence extraction replicated across twenty randomized trials might be strong evidence. Confidence tells you something about the extraction process. Provenance tells you something about the underlying evidence. You need both, and you need to combine them with domain judgment rather than treating either as a sufficient statistic.

### Multi-Source Relationships

When multiple independent sources assert the same relationship, that's meaningful signal. "Drug A inhibits enzyme B" from one paper is a datum. "Drug A inhibits enzyme B" from five papers, each with different authors, methods, and populations, is a finding. The replication across sources is evidence that the relationship is robust, not an artifact of one study's design or one extraction's error.

Designing your data model to aggregate evidence across sources -- rather than storing one relationship record per source -- is worth the extra complexity if your corpus is large enough that the same relationship will appear many times. Instead of five edges from document A, B, C, D, and E, you have one edge with a provenance list of five sources. That aggregation enables queries like "how many sources support this relationship?" and "what's the evidence grade for this claim?" It also keeps the graph from exploding in size: the number of unique relationships in a domain is much smaller than the number of relationship mentions across documents.

The aggregation logic needs to handle nuance. Two papers from the same author group might not be independent; you might want to weight them differently than two papers from unrelated labs. A paper that retracts a finding should reduce the evidence count, not leave a stale relationship in place. A paper that asserts the opposite -- "drug A does not inhibit enzyme B" -- creates a conflict that your model should represent rather than silently merging. These are design choices that depend on your domain and how you plan to use the graph.

### Provenance at Query Time

The point of capturing provenance is being able to use it. A graph server that can answer "what's the evidence for this relationship?" rather than just "does this relationship exist?" is a qualitatively different tool. The first supports verification, weighting, and explanation. The second supports only retrieval.

Whether you need that capability depends on your domain and your users. A researcher exploring a graph for hypothesis generation might be satisfied with "drug A is connected to disease B" and not need to drill into sources. A clinician considering a treatment decision needs the evidence. A regulatory submission requires traceability. Design for the most demanding use case you anticipate.

If you do need provenance at query time, design for it from the start. The query interface should support "give me this relationship and its provenance" as a first-class operation. The API response should include source documents, passages, confidence, and whatever else your schema captures. Retrofitting this into a schema that stored relationships without provenance, or into a server that never exposed it, is painful. You'd need to re-ingest to capture what wasn't captured, and you'd need to extend the API to return what wasn't designed to be returned. Get it right early.

## Chapter 11: The Identity Server

`\chaptermark{The Identity Server}`{=latex}

The identity server\index{identity server} is the component responsible for entity identity across the knowledge graph: resolving a mention to a canonical ID, tracking provisional entities until they can be confirmed, detecting synonyms, and merging duplicates. Its full architecture -- domain plugin contract, authority lookup chain, synonym cache, promotion policy, Docker deployment -- is covered in the companion volume *The Identity Server: Canonical Identity for Knowledge Graphs*. This chapter covers only what the ingestion pipeline needs to know about calling it.

### Identity Is Load-Bearing\index{entity resolution}\index{canonical entity}

Canonical entities with canonical IDs are the design decision that most separates a useful knowledge graph from a sophisticated extraction exercise. Without identity resolution, you have a collection of mentions that look like a graph but don't support cross-document reasoning. With it, "Drug A treats Disease B" means the same thing whether it came from a 2010 review article or a 2024 clinical trial, because both assertions resolve to the same nodes.

### The Pipeline's View

The ingestion pipeline calls the identity server as a black box. After the LLM extraction pass produces raw mentions, the ingest stage calls `resolve(mention, entity_type)` for each one and receives back a stable ID -- canonical if an authority matched, provisional otherwise. Provisional IDs are valid graph nodes: relationships referencing them are valid edges and evidence accumulates against them through any later promotion or merge. The pipeline does not handle provisional entities specially.

Papers, authors, and citations from document metadata enter with their canonical ID already known (a PMC ID, an ORCID) and bypass the lookup chain entirely. The citation graph this produces -- `CITES(Paper, Paper)` edges derived directly from reference lists, confidence 1.0 -- is a built-in corpus expansion mechanism: frequently cited papers not yet ingested become natural candidates for the next ingest run.

## Chapter 12: The Ingestion Pipeline

`\chaptermark{The Ingestion Pipeline}`{=latex}

### The Framework's Five Abstractions

The `kgraph` framework defines five pluggable interfaces, each implemented per domain. Every ingestion pipeline -- regardless of domain -- is built from these five pieces:

1. **DocumentParserInterface** -- converts raw bytes (XML, PDF, plain text) into a structured document with section boundaries and metadata.
2. **EntityExtractorInterface** -- takes a document and returns entity mentions: text spans with type classifications, before any identity resolution.
3. **EntityResolverInterface** -- maps mentions to canonical or provisional entities, calling the identity server and updating the synonym cache.
4. **RelationshipExtractorInterface** -- takes a document and the resolved entity set from Pass 1, and returns typed relationships between them.
5. **Bundle export** -- merges per-document results, aggregates evidence across sources, and writes the kgbundle format that the query layer loads.

Domain code implements these interfaces; the framework orchestrates them. The medlit and sherlock examples each provide their own implementations. Medlit uses an LLM for both entity and relationship extraction, a JATS/PMC XML parser, and authority lookup against UMLS, HGNC, and RxNorm. Sherlock uses a simpler text parser and a lightweight LLM extractor with no external authority lookup. Same interfaces, different implementations, same output format.

### Why Two Passes

The temptation is to do extraction end-to-end in one shot: send the document to the model, get back entities and relationships, done. That approach fails at scale for reasons that are worth stating explicitly. A single monolithic pass has a single point of failure -- if anything goes wrong, you restart from scratch. It produces output that is hard to debug, because you can't inspect intermediate states. And it conflates concerns that are better handled separately: entity extraction, identity resolution, relationship extraction, and assembly are different problems with different failure modes and different recovery strategies.

The two-pass architecture addresses this. Pass 1 (entity extraction and resolution) produces a stable, deduplicated entity vocabulary before Pass 2 runs. Pass 2 (relationship extraction) refers to canonical entity IDs rather than raw text spans, which improves consistency and enables cross-document linking. Each pass has a well-defined input and output. Failures are recoverable: if Pass 1 fails on document 47, you fix the issue and rerun from document 47. Intermediate artifacts are inspectable. The per-document bundle becomes the natural unit of work: each document produces a bundle that can be validated, cached, and merged independently. None of this is medlit-specific. It's good pipeline design for any extraction problem at non-trivial scale.

The medlit batch pipeline exposes these passes as four concrete stages, each a Python script with a well-defined artifact at its output:

1. **Vocabulary** (`fetch_vocab`): optional LLM pass over all papers to build a shared vocabulary of canonical entity names and their aliases. Output: `vocab.json` and a seeded synonym cache.
2. **Extract** (`extract`): LLM entity and relationship extraction for each paper, using the vocabulary as context. Output: per-paper `paper_*.json` artifact files in the `extracted/` directory.
3. **Ingest** (`ingest`): identity-server-based deduplication and canonical ID assignment across all extracted bundles. Output: `entities.json`, `relationships.json`, and an ID map in `merged/`.
4. **Build bundle** (`build_bundle`): assembles the kgbundle -- the loadable artifact for the query layer. Fetches titles for cited papers from NCBI `esummary`. Output: `entities.jsonl`, `relationships.jsonl`, and supporting files in `bundle/`.

That ordering matters. You need a consistent entity vocabulary before extraction can use it. You need resolved entity IDs before you can aggregate relationships across documents. And you need the aggregated merged output before you can build the final bundle. Other orderings are possible, but the principle holds: separate concerns, make each pass debuggable, design for partial failure and restart.

### Parsing: Getting to Text

Whatever your source format, you need to get to structured text before you can extract anything. The model reads text; it doesn't read PDF layout or XML tags. JATS XML\index{JATS XML} -- the format used by PubMed Central -- is medlit's case: a structured representation of journal articles with metadata, abstract, and body sections. Yours might be PDFs, HTML, EPUB, proprietary formats, or plain text that's already clean. The parser's job is to produce a document representation that preserves structure the extractor can use: section boundaries, paragraph boundaries, and the actual text content.

Two decisions matter regardless of format. First, how do you identify section boundaries? In scientific papers, the distinction between Methods, Results, and Discussion carries semantic weight -- a claim in Results is different from a claim in Discussion. In legal documents, sections and subsections matter for citation. The parser should expose this structure so downstream passes can use it. Second, how do you chunk for extraction? Documents are often too long to send to the model in one call. Chunk too small and you lose context -- the referent of "it" or "the compound" may be in the previous chunk. Chunk too large and you exceed model context limits, dilute the signal, or hit token budgets that make the run expensive. Overlapping chunks\index{overlapping chunks} can help: each sentence appears in at least one chunk, so no sentence is orphaned at a boundary. Sentence boundaries are a practical constraint worth respecting -- splitting mid-sentence produces fragments that are harder for the model to interpret correctly.

### Extraction: The LLM Pass

This is where your schema meets the text. The extraction prompt is not a generic "extract entities and relationships" request. It is a binding of your entity types and relationship types to natural language, written so the model understands exactly what to look for.

**What every extraction prompt needs.** At minimum: the closed entity-type list (definitions, prompt guidance, and classification rules for edge cases); the predicate list with domain and range guidance, explicitly steering the model toward specific predicates over generic ones like `ASSOCIATED_WITH`; corpus vocabulary as preferred names for the entities seen in the batch (injected to suppress surface variation before deduplication); and domain-specific instructions for classification edge cases and output format. The vocabulary section is optional but materially reduces deduplication noise in any field where the same concept has many names.

**The closed-world constraint.** Every relationship subject and object must be the ID of an entity extracted in the same response. The model cannot assert a relationship involving a participant it didn't also classify and type. This is enforced in the prompt and validated downstream. It prevents the model from emitting relationships that reference entities not in the extracted set -- a form of hallucination that is otherwise difficult to detect and expensive to repair.

**Staging tradeoffs.** One combined prompt -- entities and relationships together -- is simpler, often sufficient, and lower latency. Splitting into two sequential calls (entities first, then relationships over the resolved entity set) reduces hallucination surface for complex documents: the model sees a clean entity list before constructing relationships, rather than reasoning about both simultaneously. The cost is latency and complexity. Ancillary metadata (study design, population characteristics, author affiliations) can be pulled in separate lightweight calls without affecting the main extraction. Most pipelines start with a single combined call and add staged passes only when inspection reveals that splitting would help.

**Required output contract.** Per entity: a local ID (stable within the response), entity type, surface name, synonyms, and any authority ID hints the model can infer. Per relationship: subject ID, predicate, object ID, evidence span ID, confidence, and linguistic trust (`asserted` / `suggested` / `speculative`). Per evidence span: passage text, section name, and paragraph index. The linguistic trust field is what allows downstream consumers to weight hedged claims differently from direct assertions. It is worth requiring it from the start rather than retrofitting -- provenance is painful to add after a pipeline is in production.

The prompt is the place where domain expertise gets translated into extraction behavior. A clinician reviewing a well-written prompt should be able to assess whether it captures the domain correctly. Schema changes -- adding an entity type, splitting a predicate into two more specific ones -- require editing the prompt, not retraining a model. Iteration over the prompt is the design method: run extraction on a sample, inspect the output, adjust, repeat. Appendix A shows an abstracted version of the medlit extraction prompt, illustrating how entity types, predicates, linguistic trust, and the closed-world constraint slot into a template.

### Vocabulary: Building a Shared Terminology\index{vocabulary pass}

Before extraction, medlit runs a dedicated vocabulary pass over all the papers in the batch. The idea: before you try to resolve "BRCA1," "breast cancer gene 1," and "BRCA1 protein" to the same entity, you establish a shared vocabulary of entity names and their variants. A vocabulary pass asks the LLM a narrower, cheaper question than full extraction -- "given the text of this paper, list the distinct named entities you see and their common aliases" -- and aggregates the answers across all papers into a canonical name list.

The output of the vocabulary pass feeds directly into extraction. When the extraction prompt runs for each paper, the shared vocabulary is injected as context: "these are the preferred names for entities seen across the corpus; use them." This keeps extraction consistent across workers and across time. Without it, two papers that both mention GPX4 might extract it as "GPX4," "glutathione peroxidase 4," and "phospholipid hydroperoxide glutathione peroxidase" in three different bundles, and identity resolution must sort them out later. With the vocabulary priming the extraction prompt, the model tends to use a consistent preferred form, reducing the deduplication burden downstream.

Not every domain needs a vocabulary pass. If your corpus uses consistent terminology, extraction may produce sufficiently normalized output without it. But medicine, law, and chemistry -- any field where the same concept has many names and many names map to the same concept -- will see a measurable reduction in deduplication noise. Think of it as schema binding at the lexical level: you're telling the model what things are called before asking it to extract relationships among them.

### Deduplication

The same entity extracted from many documents will appear under slightly different names. "Aspirin," "acetylsalicylic acid," "ASA," and "2-acetoxybenzoic acid" are one drug. "Type 2 diabetes," "T2DM," "diabetes mellitus type 2," and "adult-onset diabetes" are one disease. The deduplication stage groups mentions, resolves them to canonical forms, and handles the ambiguous cases. This is where the gap between "a list of extracted facts" and "a coherent graph" starts to close.

The details vary by domain. In medicine, authority lookup -- MeSH, RxNorm, HGNC, and the rest -- does much of the work: many apparent synonyms resolve to the same canonical ID automatically. What remains after authority lookup is the residue: novel entities, institution-specific abbreviations, terms that aren't in any vocabulary yet. For those, you need other signals. Semantic similarity can help: mentions whose meanings are close -- as measured by comparing their numeric representations -- may be the same entity. So can co-occurrence: if "compound X" and "imatinib" appear in the same document and the context suggests they're the same, that's evidence. The hard cases are the ambiguous ones -- "ACE" could be angiotensin-converting enzyme or the gene, "CRF" could be corticotropin-releasing factor or chronic renal failure. Resolving those may require context, domain heuristics, or human review. The universal part: you need a deduplication strategy, and it should run before or alongside relationship extraction so that relationships reference resolved entities, not raw strings.

### Assembly

Once you have per-document extractions -- entities resolved, relationships extracted -- you need to merge them into a coherent whole. Assembly is not just concatenation. When multiple documents assert the same relationship, that's meaningful signal. "Drug A treats Disease B" from one paper is weaker than "Drug A treats Disease B" from five independent papers. The assembly stage should aggregate evidence across sources: one relationship record with a provenance list, not five duplicate edges. That aggregation is what makes the graph useful for reasoning -- you can weight relationships by how many sources support them, filter by evidence type, and detect when sources conflict.

The structure of the final bundle is worth thinking about carefully before you start. What does a "document" in your graph look like? Is it a node with metadata and outgoing edges to the relationships it supports? Are relationships first-class with document references, or are documents first-class with relationship references? The choice affects query patterns, provenance traversal, and how you handle updates when you re-ingest a document with corrections. Changing the bundle structure later, once you have data and downstream consumers, is expensive. Get it right early.

### Progress Tracking and Resumability\index{resumability}

Large ingestion runs fail partway through. A run over 100,000 documents will hit rate limits, network timeouts, model outages, or your own mistakes. If the pipeline has no notion of progress, you restart from zero every time. That's acceptable for a research prototype. It's not acceptable for something you run regularly.

Design for restartability\index{restartability} from the beginning. Each document should have a processing status: not started, in progress, completed, failed. The pipeline should record which documents have been fully processed and which haven't. On restart, it should skip completed documents and resume from the first incomplete one. Checkpointing\index{checkpointing} within a document -- if a single document requires multiple LLM calls, record which chunks have been processed -- can help for very long documents, though the document is usually the right granularity. The progress store should be persistent and survive process restarts. This isn't glamorous work. It's the difference between a pipeline you can run once as a demo and a pipeline you can run every week as part of your workflow.

### Design Principles

The concepts above translate directly into four implementation commitments.

**Dedup-on-write.** Identity resolution and synonym detection happen incrementally as each entity is written; there is no global deduplication pass over the corpus. Papers can be ingested concurrently.

**Per-paper atomicity.** Each paper moves through stages independently. A failure at any stage leaves the paper at its last committed status; the next available worker picks it up and retries. No paper's failure affects any other.

**Durable checkpoints.** Raw fetched text and raw LLM extraction output are stored durably before any graph writes. A schema change, extraction bug, or infrastructure failure can be recovered from without re-fetching or re-paying LLM costs.

**Shared pipeline code.** The MCP tool and the batch runner call the same stage functions. There is no separate implementation for interactive versus batch use.

### Work Queue, Artifact Files, and Reference Implementation

The medlit implementation uses Postgres as a work queue (via `SKIP LOCKED` for distributed job claiming), per-paper artifact files for durability and retraction support, and a shared set of pipeline functions used by both the batch CLI and the MCP tool. The full SQL schema, shell invocations, Python snippets, and extraction output JSON format are in Appendix A.

# Part IV: What It Makes Possible

## Chapter 13: What Your Graph Can Do

`\chaptermark{What Your Graph Can Do}`{=latex}

The value of the graph is in what grounded reasoning becomes possible, not in the serving layer. The graph doesn't tell the reasoning system what to conclude -- it offers evidence and lets the reasoning happen.

### The Server Is Not the Point

This chapter is about what becomes possible once your graph exists, not about how to build a particular serving layer. You might expose your graph through a REST API, an MCP server, a force-directed visualization, or no server at all -- just load the bundle into memory and run Python scripts against it. The infrastructure choices are yours. What this chapter is really about is the capability space: what can a well-constructed knowledge graph actually do for someone?

That distinction matters because it's easy to conflate "I have a graph" with "I have a graph server." The graph is the data structure and the relationships it encodes. The serving layer is one way to expose it. The capabilities we're about to describe -- direct querying, visualization, grounding LLMs, hypothesis generation -- are capabilities of the graph. The serving layer is a delivery mechanism. Choose one that fits your users and your deployment constraints; don't let the choice obscure what the graph itself enables.

### Direct Querying

The basics: entity lookup, relationship queries, graph neighborhood traversal. These are useful and often sufficient for many applications. The interesting design question isn't which API style (REST, GraphQL, something else) but what the right query primitives are for your domain. What questions will your users actually ask?

A biomedical researcher might ask: "What drugs are known to treat this condition?" "What genes are associated with this disease?" "What's the evidence for this drug-gene interaction?" A legal researcher might ask: "What cases cite this statute?" "What statutes does this case interpret?" The primitives that support these questions -- get entity by ID, get relationships of type X from entity Y, get N-hop neighborhood, filter by provenance -- are similar across domains. The *semantics* of what counts as a good answer differ. A drug-disease "treats" relationship in medicine has different evidentiary standards than a case-statute "cites" relationship in law. Your query interface should expose primitives that map cleanly to your domain's question types, not force users to translate their questions into a generic graph query language.

At minimum, you need: entity lookup (by name or canonical ID), relationship enumeration (what connects to this entity, and how), and some form of traversal (neighbors, N-hop expansion, path finding). Provenance-aware queries -- "give me this relationship and its sources" -- belong in the primitive set if your domain cares about evidence, which most serious domains do. Everything else is optimization.

### Graph Visualization

Chapter 9 recommended graph visualization as a diagnostic tool for pipeline development. What might visualization do for an end user exploring the graph?

A browsable, zoomable view of entities and relationships would let users navigate structure that would be tedious to reconstruct from query output. "Show me everything connected to this drug" produces a list; a force-directed layout\index{force-directed layout} produces a picture where clusters, bridges, and outliers are visible at a glance. For exploration and discovery -- "what's in this neighborhood?" "what connects these two things?" -- visualization often beats tabular output. The implementation cost is modest if you already have the query primitives; for users who think spatially about their domain, it may be the most natural interface you offer.

### Grounding LLM Inference

The pattern that changes what a language model can do: instead of asking a model to reason from its training data, give it structured, typed, provenance-tracked claims from your graph and ask it to reason from those. The difference in reliability is substantial. A model hallucinating over raw text and a model reasoning over a curated graph with explicit provenance are doing qualitatively different things, even if they look similar from the outside. This is the integration that makes a knowledge graph more than a database.

The mechanics are straightforward. A user asks a question. Your system retrieves relevant subgraphs -- entities and relationships that match the question's scope -- and injects them into the model's context. The model reasons over that context and produces an answer. The answer is grounded in the retrieved graph, not in the model's training. You can cite the sources. You can trace the reasoning path. When the graph is wrong, you fix the graph; you don't retrain the model.

The retrieval step matters. "Relevant" means different things for different questions. A question about a specific drug might need that drug's neighborhood, its indications, its interactions, and the evidence for each. A question about a disease might need the disease's subtypes, associated genes, known treatments, and the studies that support those links. Designing the retrieval logic -- what subgraph to fetch for what question -- is where domain knowledge enters. A generic "fetch entities mentioned in the question" often works; a retrieval strategy tuned to your schema and your users' question patterns works better. The graph gives you something to retrieve. The retrieval strategy determines how well the model uses it.

### MCP as the Integration Point\index{Model Context Protocol (MCP)}

The Model Context Protocol is worth understanding as an architectural pattern, not just as a specific technology. The idea is that a knowledge graph should be a first-class context source for LLM-based systems -- something that agents, assistants, and reasoning pipelines can query as naturally as a human researcher would reach for a reference database. Whether you use MCP specifically or some other integration approach, the principle is sound: your graph is most powerful when it's actively grounding inference, not sitting passively waiting to be queried by humans.

MCP defines a standard way for AI systems to discover and call tools. A knowledge graph exposed as an MCP server offers tools like "find entities matching this query," "get the neighborhood of this entity," "retrieve relationships of type X." An LLM-powered assistant with access to that server can answer domain questions by querying the graph, synthesizing the results, and citing the sources. The user gets an answer grounded in your curated knowledge rather than in the model's training distribution. The integration is loose: the model doesn't need to know your schema in advance; it discovers the available tools and uses them. That looseness is a feature. Because the contract is machine-readable, the reasoning layer can adapt to schema changes without code changes on the consumer side. Your graph can evolve without breaking every consumer.

MCP represents a qualitative shift in how the graph participates in inference. The specific thing MCP provides that REST and GraphQL don't is *discoverability*: tools are self-describing, typed, and enumerable at runtime. An agent can query the server to learn what tools exist and what they do, without being pre-programmed for your specific schema. That makes the graph a first-class active participant in agentic reasoning rather than a passive endpoint that some human wired up in advance.

If you decide not to use MCP, the graph still needs to be queryable by whatever system is doing the reasoning. REST, GraphQL, or a custom API all work, albeit not discoverable in the same way. The architectural point is that the graph should be *available* to the reasoning layer, not a separate system that humans query manually. Passive retrieval -- human runs query, copies result, pastes into chat -- is a fallback. Active grounding -- the reasoning system queries the graph as part of generating its answer -- is the target.

### BFS Queries\index{breadth-first search (BFS)}

The medlit implementation uses a JSON-based breadth-first search query language designed for LLM friendliness and context-window efficiency. The key design insight is that topology and presentation are orthogonal: BFS from seed nodes determines *which* nodes and edges are in the subgraph, while node and edge filters control only how much metadata each item carries in the response. Non-matching items appear as stubs rather than being omitted, so the LLM always sees an accurate picture of the graph's shape.

The full query format, response format, field reference, worked examples, and LLM prompt template are in the companion volume *BFS-QL: Graph Queries for Language Models*.

### Hypothesis Generation

The capability that arguably justifies building the graph in the first place, and the one that most directly prefigures the Robot Scientist in Chapter 14. Graph traversal as a discovery tool: not "what do we know about X" but "what's adjacent to X that hasn't been studied," "what entities are structurally similar to X in the graph," "what relationships exist between X and Y that no single paper asserts but that follow from combining multiple sources." These are queries that are impossible over raw text and natural over a well-constructed graph.

Consider a concrete example. Drug A treats disease D. Gene G is associated with disease D. Drug B modulates gene G. No single paper may state that drug B is worth testing for disease D. The inference follows from combining three relationships that exist in the graph. A researcher who had read all the relevant papers might make that connection; the graph makes it queryable. "What drugs modulate genes associated with this disease?" is a traversal. The results are candidate hypotheses: drug-disease pairs that the graph implies but that may not have been studied together. Some will be known, some will be nonsense, some will be novel and worth investigating. The graph doesn't decide which are which. It surfaces candidates that a human or a downstream system can filter and prioritize.

Structural similarity is another pattern. Two entities are structurally similar if their neighborhoods in the graph look alike -- similar relationship types, similar connected entity types, similar topology. If drug X is structurally similar to drug Y, and drug Y treats condition Z, then drug X might be worth testing for Z. The graph encodes the structure; the similarity query exploits it. Again, the result is a candidate set, not a conclusion. The value is in narrowing the space of possibilities to something a researcher can evaluate.

### Returning to the Dream

The fantasy at the heart of Chapter 2 -- a machine that doesn't just retrieve facts but reasons over them -- was never wrong. It was blocked at the extraction end: getting knowledge in from natural language prose was expensive enough that the vision kept stalling before the reasoning could demonstrate its value. That bottleneck is gone. The engineering in Part III -- extraction pipelines, schema design, identity resolution, bundle export -- is what the vision always needed and couldn't have.

A system built along these lines is not yet the full Robot Scientist of the next chapter -- it does not design and execute experiments in a lab. The gap is narrower than it looks. The architecture is the same: represent the domain explicitly, generate candidates from structure, ground the reasoning in that representation. The substrate has changed from formal logic and lab robotics to graphs and language models. The need for that explicit layer has not.

## Chapter 14: The Augmented Researcher

`\chaptermark{The Augmented Researcher}`{=latex}

### What Machines Would See That We Can't

Consider confirmation bias\index{confirmation bias}. A researcher with a hypothesis tends to notice evidence that supports it and to underweight evidence that doesn't. This isn't a character flaw; it's how attention works. When you're reading papers one at a time, your prior beliefs shape what you notice, what you remember, and what you connect. A graph doesn't have prior beliefs. It encodes what the literature asserts, and a traversal query doesn't care whether the result confirms or contradicts your favorite theory. The graph surfaces connections that a human reader, biased toward coherence with existing beliefs, might have skimmed past. That doesn't make the graph right and the human wrong. It makes them different. The graph offers a view that isn't filtered through a single researcher's expectations.

Prestige bias\index{prestige bias} works similarly. A finding from a famous lab or a high-impact journal gets more attention than the same finding from an unknown group or a niche venue. Citation networks\index{citation network} amplify this: papers that are already well-cited get cited more, in a feedback loop that the Matthew effect\index{Matthew effect} describes. A knowledge graph built from a broad corpus can include relationships from papers that nobody cites. The graph doesn't know which papers are prestigious. It knows which relationships were extracted. A query over the graph can expose a connection that appeared in an obscure regional journal twenty years ago and was never picked up by the mainstream literature. Again, that doesn't make the obscure paper right. It makes it *visible* in a way that citation-based discovery systematically hides it.

Recency bias\index{recency bias} is the flip side. Newer work gets more attention than older work, partly because it's easier to find and partly because the field has collectively decided that recent results matter more. But important findings sometimes sit in the literature for decades before someone connects them to a new context. A graph that spans the full temporal range of a corpus can surface those connections. "What did we know about X in 1990?" is a query that citation networks handle poorly -- they tend to show you what's cited now, which skews recent -- but a graph can answer it directly.

The point is not that machines are unbiased. Extraction has its own biases: it favors what the model was trained on, what the schema captures, what the prompts elicit. The point is that the biases are *different*. A human reading the literature and a graph traversing the same literature will expose different patterns. The augmented researcher has access to both views.

### The Combinatorial Argument\index{combinatorial discovery}

A graph with N entities and relationship types R has on the order of N² × R possible pairwise connections. Most of those don't exist; the graph is sparse. But the space of *potential* connections -- pairs of entities that could be related, that might be worth investigating -- is enormous. A human researcher can survey a tiny fraction of it. A graph can enumerate it.

The combinatorial argument is that important discoveries often live at the intersection of things that were known separately but never connected. Drug A was studied for condition X. Pathway B was studied in context Y. Nobody looked at A and B together because the relevant papers were in different subfields, published in different decades, or written in different languages. The connection was always possible in principle; it just required someone to look. A graph that spans both subfields can expose "A modulates B" as a candidate relationship -- either one that exists in the literature but wasn't connected, or one that the graph implies from combining multiple sources. The researcher's job becomes evaluating candidates rather than generating them from scratch. The graph does the combinatorial explosion; the human does the judgment.

Structural analogies\index{structural similarity} across disciplines extend this. A relationship pattern that holds in one domain might hold in another. "Compound X inhibits enzyme Y" in biochemistry suggests "inhibitor of Y" as a search strategy in drug discovery. "Gene G is associated with disease D" in genetics suggests "genes in the same pathway as G" as candidates for D. The graph encodes structure; structural similarity queries exploit it. A researcher who knows one domain well can use the graph to find analogous patterns in domains they know less well. The graph doesn't replace domain expertise. It extends the reach of that expertise across a larger structure than any one person could hold in their head.

### Linguistic and Geographic Blind Spots\index{linguistic bias}\index{geographic bias}

The scientific literature is not evenly distributed. A disproportionate share of what gets read, cited, and built upon is published in English, from institutions in North America and Europe, in journals that Western researchers routinely check. That's not a conspiracy; it's the cumulative effect of where funding flows, where training happens, and how citation networks form. The result is that a researcher following the standard literature is systematically missing work from other languages, other regions, and other publication venues.

Citation networks encode and amplify this. If you discover papers by following citations, you stay within the citation graph. Papers that nobody in your network cites are invisible to you. They might as well not exist. A knowledge graph built from a genuinely broad corpus -- including non-English sources, regional journals, preprints, and gray literature -- can expose relationships that the citation network never connects. The graph doesn't care that a paper was published in Portuguese or in a journal with an impact factor of 0.5. It cares that the extraction found a relationship. A query over that graph can return results that would never appear in a citation-based search.

This isn't a panacea. Extraction quality varies by language and by how well the source matches the model's training distribution. Building a graph that truly spans the global literature requires deliberate effort: multilingual extraction\index{multilingual extraction}, diverse source selection, and care that the pipeline doesn't silently drop or degrade non-standard inputs. But the capability is there. A well-constructed KG with broad sourcing can surface what citation networks systematically miss. For domains where important work happens outside the mainstream -- rare diseases,\index{rare disease} regional health issues, indigenous knowledge, applied research in developing countries -- that capability matters.

### The Robot Scientist\index{robot scientist}\index{Adam (robot scientist)}\index{Eve (robot scientist)}

In 2009, a team at Aberystwyth University published results from a system they called Adam.\index{Adam (robot scientist)} Adam was a robotic scientist that reasoned from a knowledge graph of yeast biology, formulated hypotheses about the function of specific genes, designed experiments to test those hypotheses, ran the experiments using a robotic lab, and updated its beliefs from the results. The loop was fully autonomous. Adam identified, from the graph, genes with unknown function; inferred, from structural and pathway relationships, what those functions might be; and confirmed several of its predictions experimentally. It was the scientific method, formalized and automated. No human was in the loop between hypothesis formation and experimental confirmation.

Eve\index{Eve (robot scientist)} extended the pattern to drug discovery. The same loop -- reason from the graph, form hypotheses about drug-target interactions, test them -- was applied to the problem of identifying compounds that might be effective against specific pathogens. Eve was not looking for candidates in the way a drug discovery pipeline looks for candidates. It was reasoning over a structured knowledge representation, traversing relationships between compounds, targets, and biological processes, and identifying implications of those relationships that hadn't been tested.

What Adam and Eve demonstrated was that autonomous scientific reasoning is achievable, given a rich enough knowledge representation. The bottleneck wasn't the reasoning -- the inference, the experimental loop, the belief updating. The bottleneck was getting the knowledge in. Adam's knowledge graph was narrow: yeast biology, curated by domain experts, sufficient for inference within that domain. Eve's graph was broader but still hand-constructed. Building the knowledge representation required a team of domain experts working by hand for months. That meant the approach was confined to domains where someone had already done that work. Everywhere else, the graph didn't exist, and neither did the possibility of automating the reasoning over it.

That bottleneck is gone. The machinery in Part III -- extraction from literature, identity resolution, provenance tracking, hypothesis generation as graph traversal -- is the machinery that lets an Adam-like system scale beyond a single hand-curated domain. A graph spanning drug discovery, disease biology, and chemical space, built from the literature rather than manually encoded, could generate hypotheses connecting compounds, targets, and indications across literatures that no single human could synthesize. The representation was always the limiting factor. The tools to build the representation now exist.

The honest answer about where we are: close enough to see the path, not close enough to declare victory. We have extraction that works at scale. We have identity resolution. We have provenance that supports evidence-weighted reasoning. What we don't yet have is the full autonomous loop -- automated experiment design, robotic execution, belief updating from results -- deployed across arbitrary domains. The wet-lab part remains a different kind of engineering problem. But the representation was always the bottleneck. Once the graph exists, the rest is engineering. And what that engineering might enable -- systems that expose what the literature already implies but hasn't yet connected, in domains where the literature is too scattered for any individual researcher to see the full picture -- is reason enough to take this seriously.

## Chapter 15: Consequences

`\chaptermark{Consequences}`{=latex}

### Democratization and Its Limits

Building and maintaining a serious knowledge graph still requires significant resources. You need a corpus, which may be behind paywalls\index{paywalls}. You need compute for extraction, which costs money. You need domain expertise to design the schema and validate the output. The result is that the first generation of domain-spanning knowledge graphs will likely be built by those who can afford to build them -- pharmaceutical companies, large universities, government agencies, well-funded startups. The question of who gets access then becomes a question of licensing, openness, and governance.

The promise the technology holds out is real nonetheless. A researcher at a small institution, or in a developing country, with access to a comprehensive KG over their domain would have the same structural view of the literature as a researcher at a well-funded lab. The graph doesn't care who queries it. The capability to synthesize across millions of papers, to expose connections that citation networks hide, to ground an LLM in curated knowledge -- that capability could be democratized. The technology enables it; policy and incentive will decide whether it happens.

### Compressed Discovery Timelines\index{drug discovery}

In drug discovery, the bottleneck is often synthesis -- not of molecules, but of knowledge. A promising target emerges from basic research. The relevant literature spans decades, multiple disciplines, and hundreds of papers. Someone has to read it, extract the key relationships, and figure out what's known, what's contested, and what's missing. That synthesis can take months. A functioning extraction pipeline and a well-constructed graph can compress it to days. The same is true in rare disease research, where the literature is scattered across case reports, small studies, and patient advocacy publications. And in materials science, where the space of possible compounds is vast and the literature connecting structure to properties is fragmented. In each of these domains, the bottleneck is not the underlying science; it's the human capacity to hold and connect what's already been published. A KG that does that synthesis automatically changes the pace of work. The researcher's time shifts from "what do we know?" to "what should we do next?" That shift is consequential.

### The Rare Disease Problem\index{rare disease}

Rare diseases are underserved not because nobody cares but because no single community is large enough to see the full picture. A disease that affects one in fifty thousand people might have a few hundred papers published about it, scattered across decades and subdisciplines. No single clinician sees enough cases to develop deep expertise. No single researcher has the bandwidth to synthesize the full literature. The patient community is small and often fragmented. The result is that knowledge about rare diseases exists -- it's in the literature -- but it's never assembled in a form that any one person or group can use. Patients and their doctors are left to piece it together from whatever they can find.

A knowledge graph built from the full rare-disease literature could serve as a coordination mechanism. It wouldn't replace clinical expertise or patient advocacy. It would give both something to work with: a structured view of what's known, what's been tried, what's connected to what. A clinician facing an unfamiliar rare diagnosis could query the graph for similar cases, related genes, and treatment attempts. A patient group could use it to identify research gaps and prioritize what to fund. The graph doesn't solve the problem of small communities. It gives small communities access to the same structural synthesis that large communities can achieve through sheer numbers. That's a different kind of equalizer.

### Credit, Priority, and Provenance\index{credit (scientific)}\index{scientific priority}

When a machine surfaces a connection -- a drug-disease relationship that no single paper states but that the graph implies from combining multiple sources -- who gets credit? The authors of the papers that contributed the underlying facts? The builders of the graph? The user who ran the query? The question matters for scientific priority, intellectual property, and the sociology of research. Scientists are rewarded for discovery. If the discovery is made by a system, the reward structure gets complicated.

Provenance tracking, which the book has treated as a technical concern throughout, turns out to have significant ethical implications. How you record where a fact came from determines who can be credited. A relationship with full provenance -- source document, passage, extraction method -- makes it possible to trace the contribution back to the original authors. A relationship stored without provenance makes that impossible. The technical decision about schema design is also a decision about how credit will flow. The same is true for conflicts: when two sources assert contradictory relationships, provenance lets you represent the conflict rather than silently merging. That representation matters for how disputes get resolved and how the community understands what's known versus what's contested. The builder of the graph is making choices that affect the sociology of the domain, whether or not they intend to.

### Who Owns the Graph\index{open science}\index{graph ownership}

Open versus proprietary is not a new tension in science. GenBank\index{GenBank}, the repository of genetic sequences, was built as a public resource; the decision to make it open and freely accessible shaped how molecular biology developed. Clinical trial data, by contrast, has often been held proprietary by sponsors; the fight for access has been long and only partially won. The question of who owns a comprehensive knowledge graph over a significant scientific domain will have similar consequences.

If a single entity -- a company, a government, a consortium -- controls the graph, that entity controls who can query it, what they can do with the results, and how the graph evolves. The incentives may align with the scientific commons, or they may not. A company that built a drug-discovery KG might restrict access to protect competitive advantage. A government might restrict access for national security reasons. An open consortium might make the graph freely available but lack the resources to maintain it. The historical analogies are instructive: GenBank succeeded because the community agreed that sequence data should be a commons; clinical trial data remains contested because the incentives are mixed. A knowledge graph over a domain like medicine or materials science will face the same tensions. What it would mean for a single entity to control it -- the power to shape what gets synthesized, what gets surfaced, what gets updated -- is worth thinking about before it happens.

### Capability Is Not Bounded by Intent\index{capability vs. intent}\index{architecture of expertise}

Consider what it means to build a system that encodes the architecture of expertise for a domain. You built a graph for drug discovery; a user runs a traversal that surfaces a drug-pathway combination that could be repurposed for something harmful. You built a graph for medical literature; a query connects the dots in a way that reveals something about a person's health that they didn't intend to share. You built a graph for materials science; the same structural similarity query that finds promising battery compounds could find promising explosives. None of these are edge cases or failures. They follow directly from the system working as designed.

The graph encodes structure; structure supports inference; inference doesn't respect the boundaries of what you had in mind. A reasoning system with access to rich, typed, provenance-tracked knowledge will expose connections its builders didn't anticipate -- because the value of the system is precisely that it can traverse the graph more exhaustively than any individual human would. That traversal doesn't stop at the edges of your intended use case. Capability is not neatly bounded by intent.

That doesn't mean you shouldn't build. It means you should build with your eyes open. The inferences the system can expose are a feature when they advance science and a risk when they don't. The difference is often context, use case, and the choices you make about access, provenance, and what gets logged. Those choices deserve to be taken seriously.

### Dual Use at Graph Scale\index{dual use}

The drug interaction that saves lives and the synthesis route that enables harm are both pattern-matching problems over structured knowledge. A graph that encodes "compound X inhibits enzyme Y" and "reaction A produces compound X" can answer "what inhibits Y?" for a clinician looking for treatments and for someone looking for precursors. The same query interface serves both. The graph doesn't know the difference. Dual use is not a bug; it's inherent to how knowledge works. Facts don't come with moral valence. The same fact can support healing or harm depending on who uses it and how.

What does responsible construction and deployment look like? There's no clean answer, but there are practices that help. Access control\index{access control}: who can query the graph, and for what? Some graphs should be broadly available; others may need to be restricted to credentialed researchers or vetted use cases. Provenance and transparency: when the system surfaces a connection, can the user trace it to sources? That traceability supports verification and accountability. Logging and monitoring: if the graph is used for something harmful, can you detect it? Auditing: who reviews how the system is used? These are operational questions, not just technical ones. They don't eliminate dual use. They make it harder to misuse the system without leaving a trace, and they create channels for accountability when misuse occurs. The right response to dual use isn't to not build. It's to build with these questions in mind.

### Bias at Scale\index{bias (knowledge graph)}

A knowledge graph encodes the biases of its sources. If the biomedical literature over-represents male subjects, Western populations, and certain research paradigms, the graph encodes that. A query over the graph will expose relationships that reflect those biases. The graph doesn't add bias; it preserves and amplifies what's in the literature. At scale, that amplification has a subtle effect: the graph starts to look like systematic knowledge. The user sees a dense network of connections and may assume it represents the full picture. It doesn't. It represents what got published, in what proportions, with what emphases. The appearance of comprehensiveness can be misleading.

Mitigation strategies exist. Diverse sourcing: build the graph from a corpus that includes underrepresented populations, regions, and publication venues. Provenance transparency: make it visible where each relationship came from, so users can assess coverage and gaps. Explicit uncertainty representation: don't present the graph as ground truth; represent confidence, conflict, and the limits of the corpus. These strategies help. They have limits. You can't source what doesn't exist; if the literature on a topic is thin or skewed, the graph will be too. Provenance helps users notice gaps; it doesn't fill them. Uncertainty representation requires schema support and user literacy. The honest conclusion: bias at scale is a structural feature of any system built from human-generated sources. You can mitigate it; you can't eliminate it. Build with that in mind.

### The Epistemic Responsibility of the Builder\index{epistemic responsibility}

What do you owe to the users of the system you build? At minimum, you owe them honesty about what the system is and isn't. It's a synthesis of the literature, not a representation of ground truth. It has gaps, biases, and limits. Users who don't understand that may over-trust it. You also owe them the infrastructure for verification: provenance, so they can trace claims to sources; confidence, so they can weight what they find; and documentation, so they know what the schema captures and what it doesn't.

Beyond that, the builder's choices about provenance, transparency, access, and schema design are ethical choices, not just technical ones. Deciding what to extract, how to represent it, who gets to query it, and what gets logged -- these decisions shape how the system will be used and what consequences it will have. That doesn't mean every builder must solve every ethical problem before shipping. It means the builder is a stakeholder, with some power to shape outcomes. The right response isn't paralysis. It's to take the responsibility seriously, to build with the foreseeable consequences in mind, and to create the conditions for accountability when things go wrong.

### Open Problems

The approach in this book works. It also has limits. An honest assessment of what doesn't yet solve well:

**Very long document contexts.** Scientific papers can be tens of thousands of words. The relationships that matter may span sections written pages apart. Chunking helps but doesn't fully solve the problem: a relationship that spans a chunk boundary may be missed, and the model's context within any chunk is always less than the full document. Longer context windows in future models will help. So will multi-pass strategies that explicitly handle cross-chunk dependencies. The problem is tractable; it's not solved.

**Multi-hop reasoning during extraction.**\index{multi-hop reasoning} Some relationships require integrating information across multiple sentences, paragraphs, or documents. "Drug A was tested in combination with B; the combination showed activity against C" implies a relationship between the combination and C that depends on understanding both clauses. Current extraction is largely single-pass over local context. Richer reasoning during extraction -- the ability to hold intermediate conclusions and combine them -- would improve recall on complex relationships. This is an active research direction.

**Real-time updating.** The pipeline in this book is batch-oriented: you ingest a corpus, build a graph, serve it. When new papers appear, you re-run the pipeline. That works for many use cases. It doesn't work for domains where freshness matters -- breaking news, emerging outbreaks, rapidly evolving fields. Incremental update\index{incremental update}, where new documents are processed and merged without full re-ingestion, is a different design. It's buildable; it adds complexity.

**Schema evolution without re-extraction.**\index{schema evolution!without re-extraction} When you add a new entity type or relationship type, the natural approach is to update the schema and re-extract. That's expensive at scale. Schema evolution that can incorporate new types without re-processing the entire corpus -- perhaps by running a targeted extraction pass over documents likely to contain the new type -- is an open problem. Most projects today bite the bullet and re-extract when the schema changes significantly.

None of these are fundamental blockers. They're places where the current approach is good but not great, and where progress would expand the range of problems the technology can address.

### Where the Field Is Going

The specific reasoning substrate will change. LLMs today, something else in ten years -- perhaps more efficient models, perhaps hybrid systems that combine neural and symbolic reasoning, perhaps something we haven't imagined. The need for this grounding layer will not change. Whatever comes after LLMs will still need explicit, domain-specific, human-curated knowledge structure to reason reliably in specialized domains. The book is not documenting a technology moment; it is identifying a permanent architectural requirement that the current moment has finally made practical to address.

Retrieval-augmented generation\index{retrieval-augmented generation!as convergence point} is a point of convergence. The idea that language models should be grounded in retrieved context rather than relying solely on training is now mainstream. Knowledge graphs are one form that retrieved context can take -- structured, typed, provenance-tracked. The RAG paradigm and the KG approach are complementary. As RAG matures, the value of structured retrieval -- graphs over document chunks -- becomes clearer. The convergence is already happening.

Structured world models\index{structured world models} in foundation models\index{foundation models} are another direction. Some researchers are exploring whether large models can learn internal representations that are more graph-like, with explicit entities and relationships. If that succeeds, the boundary between "retrieve from external graph" and "reason from internal structure" may blur. Even then, the argument for explicit, inspectable, provenance-tracked graphs remains: internal representations are opaque; external graphs are auditable. For domains where you need to trace a claim to a source, an external graph is the right architecture. The substrate may evolve. The need for that layer will not.

What the field needs that isn't purely technical is harder to forecast but worth naming. Shared schemas for common domains would reduce duplicated effort and make graphs interoperable across research groups. Open corpora with permissive licensing would let extraction pipelines be benchmarked and compared. Community norms around provenance -- what it means to assert a relationship, how confidence should be calibrated, how retractions should propagate through downstream graphs -- are still being established. The engineering described in this book is relatively mature compared to the social infrastructure around it. Both are necessary.


# Appendix A: Reference Implementation Notes

`\chaptermark{Reference Implementation}`{=latex}

This appendix documents implementation details of the medlit reference project: the ingestion pipeline's work queue, artifact files, parallelism, and shared code. These details are specific to one implementation and will evolve; the principles behind them are in Chapters 11 and 12.

### Ingestion Pipeline: Work Queue

A Postgres table coordinates all work:

```sql
CREATE TABLE ingest_jobs (
    pmcid          TEXT PRIMARY KEY,
    status         TEXT NOT NULL DEFAULT 'pending',
                   -- pending → fetching → fetched
                   --        → extracting → extracted
                   --        → ingesting → done | failed
    raw_text       TEXT,
    raw_extraction JSONB,
    error          TEXT,
    attempts       INT DEFAULT 0,
    updated_at     TIMESTAMPTZ DEFAULT now()
);
```

Workers claim jobs with:

```sql
SELECT * FROM ingest_jobs
WHERE status = 'pending'
FOR UPDATE SKIP LOCKED
LIMIT 1;
```

`SKIP LOCKED` provides a distributed work queue with no additional infrastructure: no races, crash-safe, and naturally load-balanced across any number of workers or server instances. A crashed worker releases its lock when its connection drops and the job is retried by the next available worker. The `attempts` counter enables dead-lettering after N failures, leaving the job at `status='failed'` with the error recorded.

Progress is trivially observable:

```sql
SELECT status, count(*) FROM ingest_jobs GROUP BY status;
```

### Paper Artifact Files

After `extract_stage` stores `raw_extraction` in Postgres, it also writes a per-paper artifact file using atomic write-then-rename:

```python
tmp = artifact_dir / f".tmp_{pmcid}_{os.getpid()}.json"
tmp.write_text(json.dumps({
    "pmcid": pmcid,
    "raw_text": raw_text,
    "raw_extraction": raw_extraction,
}, indent=2))
tmp.rename(artifact_dir / f"paper_{pmcid}.json")
```

Including both `raw_text` and `raw_extraction` makes each file a self-contained record of everything that happened for that paper.

**These files serve three purposes:**

**Recovery.** If Postgres is lost, the artifact directory is sufficient to repopulate the graph. For extraction-side schema changes (new entity types, revised prompts), reset to `status='fetched'` and re-run from `raw_text`. For ingest-side changes only, reset to `status='extracted'` and re-run from `raw_extraction`. In both cases the identity server runs fresh and rebuilds all merges correctly.

**Auditability.** A human-readable record of what was fetched and what the LLM extracted, independent of any subsequent graph operations.

**Retraction support.** When a paper is retracted, its artifact file provides an exact record of every claim it contributed to the graph. Provenance-aware graph queries can then down-weight or exclude retracted sources. The artifact is the supporting record for that process; a `retracted` flag on `ingest_jobs` is the mechanism.

The artifact directory can be a local volume, NFS mount, or S3-compatible store.

**Repopulation from artifacts:**

```bash
python -m medlit.scripts.ingest \
    --from-artifacts ./artifacts/ --ingest-workers 16
```

Reads `paper_*.json` from the directory, inserts each into `ingest_jobs` with the appropriate status and fields populated from the file (`INSERT ... ON CONFLICT DO NOTHING` skips papers already in the table), then lets the normal worker pool handle the rest.

### Parallelism

Different stages have different bottlenecks and should have independently tunable worker counts:

| Stage   | Bottleneck                       |
|---------|----------------------------------|
| Fetch   | PMC API rate limits              |
| Extract | LLM token budget / cost          |
| Ingest  | Postgres / identity server locks |

The batch runner accepts separate concurrency limits per stage. Running multiple instances of the batch runner across machines is safe; all instances share the same `ingest_jobs` table and coordinate via `SKIP LOCKED`.

### Batch Ingestion

The batch pipeline is driven by a shell script that sequences the four stages in order:

```bash
# Run all four stages over a named list of papers
./run-ingest-new.sh --list ferroptosis      # two-paper test set
./run-ingest-new.sh --list smorgasbord     # 39-paper corpus
```

Each stage is a Python module invoked with `uv run python -m`:

```bash
# Stage 1: vocabulary
uv run python -m examples.medlit.scripts.fetch_vocab \
    --input-dir pmc_xmls --output-dir vocab --papers PMC12345.xml,...

# Stage 2: extraction
uv run python -m examples.medlit.scripts.extract \
    --input-dir pmc_xmls --output-dir extracted \
    --vocab-file vocab/vocab.json --papers PMC12345.xml,...

# Stage 3: ingest (identity-server deduplication)
uv run python -m examples.medlit.scripts.ingest \
    --bundle-dir extracted --output-dir merged --use-identity-server

# Stage 4: build bundle
uv run python -m examples.medlit.scripts.build_bundle \
    --merged-dir merged --bundles-dir extracted \
    --output-dir bundle --pmc-xmls-dir pmc_xmls
```

Stages 1 and 2 are embarrassingly parallel at the paper level and can be run with multiple workers. Stage 3 parallelizes authority lookups (MeSH, UniProt, HGNC) within a single run using `asyncio.gather` with a semaphore, so HTTP calls to authority APIs happen concurrently rather than sequentially. Stage 4 is fast and single-threaded -- its main network cost is the batched NCBI `esummary` call for cited-paper titles, which takes only a handful of requests regardless of corpus size.

### MCP Tool

The MCP tool is a convenience for a user who wants to pull in one or a few papers during a query session and have them available immediately. It is not intended for bulk operations.

The tool calls the same underlying pipeline stages as the batch CLI -- fetch, extract, ingest, build bundle -- but runs them synchronously in a background thread so the MCP server stays responsive. If the paper has already been ingested, it returns immediately with a status message. For large lists of papers, use the batch CLI instead; the MCP tool is optimized for single-paper interactive use.

```python
@mcp.tool()
async def ingest_paper(pmcid: str) -> dict:
    """
    Fetch, extract, and ingest a single PMC paper into the knowledge graph.
    Runs the full pipeline (fetch → extract → ingest → build_bundle) and
    makes the paper available for querying on return.
    """
    # Check if already ingested
    existing = check_ingest_status(pmcid)
    if existing == "done":
        return {"status": "already_ingested", "pmcid": pmcid}

    # Run all pipeline stages via the same function used by the batch worker
    await asyncio.get_event_loop().run_in_executor(
        None, _run_pass2_pass3_load, workspace, bundles_dir, merged_dir, output_dir
    )
    return {"status": "ingested", "pmcid": pmcid}
```

The `_run_pass2_pass3_load` function is the shared implementation used by both the MCP tool and the background ingest worker. It runs `ingest`, `build_bundle`, and `load_bundle_incremental` in sequence, so that after it returns the paper is live in the graph without a server restart.

### Extraction Output Format

The artifact file captures what the LLM decided, before the identity server assigns any entity IDs. Mentions and evidence strings include their location in the source document so that any claim can be verified against the original text.

`raw_text` is stored as the original PMC XML rather than stripped plain text. PMC XML has explicit section labels (`<sec>`, `<title>`, `<p>`) that make section and paragraph extraction reliable, and preserving the structure means location references remain valid if the artifact is re-ingested later.

Most paper metadata and cited references are available as structured fields in the PMC XML and are parsed directly by the fetch stage rather than extracted by the LLM. This makes them reliable and cheap — no prompt engineering required. Each cited PMC ID is also a candidate for further ingestion, making the reference list a natural source for corpus expansion.

```json
{
  "pmcid": "PMC12345",
  "extracted_at": "2026-03-17T14:23:00Z",
  "model": "claude-sonnet-xxx",
  "metadata": {
    "title": "Serum cortisol as a diagnostic marker for hypercortisolism",
    "authors": [
      { "name": "Jane A. Smith",  "institution": "Massachusetts General Hospital" },
      { "name": "Robert T. Chen", "institution": "Harvard Medical School" }
    ],
    "publication_date": "2024-09-15",
    "journal": {
      "name": "Journal of Clinical Endocrinology & Metabolism",
      "issn": "0021-972X",
      "volume": "109",
      "issue": "4",
      "pages": "1123-1131"
    }
  },
  "references": [
    {
      "pmcid": "PMC98765",
      "doi": "10.1210/clinem/dgad001",
      "authors": ["Johnson B", "Lee K"],
      "title": "Urinary free cortisol in Cushing syndrome diagnosis",
      "journal": "Endocrine Reviews",
      "year": "2023"
    }
  ],
  "entities": [
    {
      "mention": "cortisol",
      "type": "Biomarker",
      "locations": [
        { "section": "Abstract", "paragraph": 1, "sentence": 2 },
        { "section": "Results",  "paragraph": 2, "sentence": 1 },
        { "section": "Results",  "paragraph": 4, "sentence": 3 }
      ],
      "attributes": {
        "value": "elevated",
        "specimen": "serum"
      }
    }
  ],
  "relationships": [
    {
      "subject_mention": "cortisol",
      "predicate": "indicates",
      "object_mention": "hypercortisolism",
      "evidence": "Serum cortisol levels were elevated in all patients diagnosed with hypercortisolism.",
      "evidence_locations": [
        { "section": "Results", "paragraph": 2, "sentence": 1 }
      ]
    }
  ]
}
```

Key properties:

- **Mentions, not IDs.** The artifact records what the LLM said. Entity IDs are assigned by `identity_server.resolve()` during ingest and are not present here.
- **All locations for each entity.** The same entity may be mentioned many times across a paper. Recording all locations supports `usage_count` computation and provides the full evidentiary basis for the entity.
- **Evidence strings with location.** The verbatim text supporting each relationship, with its position in the document. `evidence_locations` is a list to handle cases where the supporting evidence spans multiple sentences or where the antecedent of a pronoun appears in a prior sentence.
- **Model and timestamp.** Records exactly what produced this output, which is essential when comparing extractions before and after a prompt or model change.
- **No graph state.** Nothing about merges, status, or canonical IDs. That is all rebuilt fresh by the identity server on each ingest.

### Shared Pipeline Code

The four pipeline stages share their core logic across both the batch CLI and the MCP/server path. The batch CLI calls stage scripts directly; the MCP tool and background ingest worker call `_run_pass2_pass3_load`, which sequences the ingest, build_bundle, and load_bundle_incremental steps using the same underlying functions:

```python
def _run_pass2_pass3_load(
    workspace_root: Path,
    bundles_dir: Path,
    merged_dir: Path,
    output_dir: Path,
) -> None:
    """Run ingest, build_bundle, and load_bundle_incremental. Raises on failure."""
    run_ingest(bundle_dir=bundles_dir, output_dir=merged_dir, ...)
    run_build_bundle(merged_dir, bundles_dir, output_dir)
    load_storage.load_bundle_incremental(manifest, str(output_dir))
```

`run_ingest` is the identity-server deduplication stage. `run_build_bundle` assembles the kgbundle including NCBI title fetching. `load_bundle_incremental` pushes the new bundle into the live graph storage without a restart.

The vocabulary and extraction stages are not in this shared path -- they are CLI-only for batch runs, since interactive single-paper ingestion via the MCP tool skips the vocabulary pass (the vocabulary built from the existing corpus is already embedded in the seeded synonym cache). For the MCP use case, the paper is extracted with the current vocabulary as context, then ingested, and the bundle is rebuilt and reloaded.

### Extraction Prompt Template

The extraction prompt is a Jinja2 template with three injection points and a small number of structural rules that apply regardless of domain. What follows is an abstracted version that shows the structure; the full medlit domain instructions serve as a worked example.

```
You are a knowledge extraction expert. Extract entities
and relationships from the given text and return a single
JSON object with this structure (use exact keys):

- "entities": array of {
    "id"        (string, unique within this response),
    "class"     (entity type from the list below),
    "name"      (canonical surface form),
    "synonyms"  (array of alternate names)
  }

- "evidence_entities": array of {
    "id"     (format: paper_id:section:para_idx:method),
    "class": "Evidence",
    "text"   (verbatim passage from the source)
  }

- "relationships": array of {
    "subject"          (id from entities array),
    "predicate"        (from predicate list below),
    "object"           (id from entities array),
    "evidence_ids"     (array of evidence entity ids),
    "confidence"       (0.0–1.0),
    "linguistic_trust" ("asserted"|"suggested"|"speculative")
  }

CRITICAL: "subject" and "object" must be the "id" of an
entry in the "entities" array. If an entity appears in a
relationship but is not yet in the entities array, add it
first. Never use a free-form name as subject or object.

Return ONLY valid JSON. No markdown, no commentary.

{{ domain_instructions }}

Entity types: {{ entity_types }}
Predicates:   {{ predicates }}
{{ vocab_section }}
```

The three injection points:

- `{{ entity_types }}` -- rendered from the domain spec; one line per type with label, description, and any classification guidance. In medlit this is the full list (Disease, Gene, Drug, Protein, ...) with concise definitions and edge-case rules (e.g. "if both Hormone and Protein, classify as Hormone").

- `{{ predicates }}` -- rendered from the domain spec; one line per predicate with description and domain/range guidance. Listing domain and range steers the model toward specific predicates rather than generic fallbacks like `ASSOCIATED_WITH`.

- `{{ vocab_section }}` -- injected when a vocabulary pass has been run; lists preferred names for entities seen across the current batch. When present, the model uses consistent surface forms, reducing deduplication noise downstream. When absent (single-paper MCP use), the section is empty and the model names entities as it sees fit.

The `domain_instructions` block is where domain-specific classification rules and output conventions live. In medlit:

```
This domain covers peer-reviewed medical literature.
Prefer established terminology over colloquial.
When in doubt about entity type, prefer the more specific.
Connect Author and Institution to the graph via
relationships; do not leave them as standalone entities.

#### Entity type classification
Classify at the most specific functional role. If an
entity is both a hormone and a protein, classify as
Hormone. Enzymes should be Enzyme, not Protein.
Extract pathological processes (hyperplasia, hypertrophy,
atrophy, etc.) as Symptom entities.

#### Predicates
Use the predicate list from the config. For SAME_AS,
use "resolution": null and "note" in the output.
When text describes a hormone "causing" a pathological
change "of" an anatomical structure (e.g. "ACTH
determines hyperplasia of the adrenal cortex"), extract:
(1) AGENT CAUSES SYMPTOM
(2) SYMPTOM LOCATED_IN ANATOMICAL_STRUCTURE

#### Linguistic trust
For each relationship, classify linguistic trust:
asserted (direct statement), suggested (soft language),
speculative (hedged).

#### Evidence format
Evidence id format:
  {paper_id}:{section}:{paragraph_idx}:llm
Use ==CURRENT_PAPER== as paper_id when PMC ID is unknown.
```

The domain instructions block is the place for rules that are domain-specific: what to do about entities that span multiple types, which predicates to prefer for common patterns in the literature, how to handle missing identifiers. Keep it short and declarative. Rules the model must actually follow during extraction belong here; background on why those rules exist does not.
