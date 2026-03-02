---
title: Knowledge Graphs from Unstructured Text
author: Will Ware
rights: © 2026 Will Ware, MIT License
language: en-US
description: "A practitioner's guide to building knowledge graphs from unstructured text using LLMs."
cover-image: CoverImage.png
...

# Preface

This is a book written in the age of Large Language Models, but the central thesis of this book is about machine reasoning in general, now and in the future. Knowledge graphs predate LLMs and will outlast them, because they capture something essential to how humans understand and reason about complex fields in an explicit, structured form that can be shared and curated. A machine cannot reason reliably about such fields without knowledge encoded in some form of graph. The software projects described here are demonstrations of this thesis, not the subject of it. LLMs are enablers for the creation of knowledge graphs, which were much discussed in the past but only practical at scale now.

![](ExampleGraph.png)

This is a picture of a simple knowledge graph. Bubbles and arrows (we can call them "nodes" and "edges" or "vertices" and "edges") both have labels representing metadata. Graph theory is a branch of mathematics that includes non-trivial theorems and results.

The gist of this book (beyond providing a lot of how-to information) is that a knowledge graph in some form is

- a necessity, not just a convenience, for reliable machine reasoning
- an explicit representation of how human experts understand difficult topics

---

# Part I: The Landscape

## Chapter 1: Why Do We Want Knowledge Graphs?

### Large Language Models Work Great

We ask them questions about the capitals of countries, or about a chemical formula, or how long to bake something in the oven, and usually we get an answer that is articulate, confident, intelligent-sounding, and correct. We can go to Wikipedia or Google and confirm that, yes, that is the right answer. It's a feel-good moment. The fluency is real. The models have internalized an enormous amount of surface pattern from human text, and for a large class of questions that pattern is enough.

### Until They Don't

Correctness was never a primary design priority for LLMs. They are neural networks trained on large corpora. They try to predict the next bit of text, following statistical patterns derived from the training set. As long as our questions stay well within the training set, we can expect answers that are correct most of the time.

When we stray outside the training set contents, the LLM has no mechanism or structure to guage correctness and no way to correct an answer. We get answers that are articulate, confident, intelligent-sounding, and wrong. My brother told an LLM:

> I live near a carwash and the weather is warm and sunny. I want to get my car washed. Should I walk or drive there?

and of course he was told that on a nice day like this, he could use the exercise, so he should walk to the carwash.

The LLM only "knows" what's in the training set, only the statistical patterns of the text it was trained on. It doesn't know that he'll need his car in order to get it washed. The dangerous part is that the wrong answer was delivered with the same tone and confidence as a right one would have been. There is no internal signal that says "I'm extrapolating here" or "I'm not sure." The machine has no way to distinguish a retrieval from memory from a plausible guess. This is **hallucination** -- the model producing confident, fluent, false output because it is doing what it was designed to do (generate statistically plausible text) in a situation where the right answer is not well represented in its training. Hallucination is not a bug to be patched; it is a predictable consequence of how LLMs work.

### The Scale of the Problem

For casual use, hallucination might be acceptable. For anything that matters -- medical advice, legal research, scientific synthesis, technical decisions -- we need more than fluency. We need answers that are grounded in something checkable, that can be traced to a source, that can be updated when the world changes, and that reflect the structure of the domain rather than the statistics of the training corpus. That is a different kind of system.

### Retrieval-Augmented Generation or "RAG"

We can artificially extend the scope of the training set by adding content to the prompt for the parts the LLM is likely to get wrong. My brother might have created a prompt describing car wash operations and mentioning that the car must be physically present for the operations to work. With the prompt extended in this way, eventually the LLM would stop making that kind of mistake. That would have been a laborious manual process of tinkering and re-wording, and seeing what worked best. This approach would not scale to large bodies of knowledge.

In practice, RAG usually means retrieving relevant passages from a document store and stuffing them into the prompt. That helps: the model can reason over the retrieved text instead of relying solely on training. But retrieved passages are still just text. The model has to parse them, resolve references, and combine information across snippets on the fly. There is no explicit representation of *what* entities are in play or *how* they are related. The structure of the domain stays implicit in the prose, and the model is left to infer it every time. For narrow, one-off questions that can be answered from a few paragraphs, this often works. For complex reasoning that depends on many entities and relationships, or for questions you didn't know to ask in advance, passage retrieval hits its limits.

### Graph RAG

The LLM is given a knowledge graph to consult. Instead of raw passages, it gets entities and typed relationships: this drug *treats* this condition, this gene *encodes* this protein, this study *reports* this finding. The graph answers "what is connected to what" and "what kind of connection is it" in a form the model can traverse and cite. The entities and the links between them provide facts, context, names, dates, and meaningful connections. You knew you were asking an egg question for your omelette but you didn't realize in advance that you might also want to know how to tell if an egg has gone bad; the graph can surface that connection because the structure is explicit.

A knowledge graph built from your domain gives the model something to reason *from* rather than something to paraphrase. Claims can be traced to sources. Gaps and conflicts in the graph are visible. When the underlying evidence changes, you update the graph instead of retraining the model. The graph is a shared, inspectable representation of what the system is allowed to "know" in that domain.

### Why Bother Building One?

Knowledge graphs provide a unique return on investment. They are simple data structures, easy to understand, not too difficult to build with the tools we have now, and easy for an LLM to query. They reflect the shape of human knowledge with surprising accuracy when the extraction is done well. The rest of this book is about when you want one, how to design it, and how to build it from the unstructured text where most of that knowledge still lives.

## Chapter 2: A Brief History of Knowledge Representation

### The Idea That Wouldn't Die

Opens with the observation that humans have been trying to make machines that *know things* -- not just store data -- for as long as there have been computers. Sets up the through-line of the chapter: repeated attempts, repeated partial successes, repeated stalls at the same bottleneck.

### What the Frog's Eye Tells Us

In 1959, a paper appeared in the *Proceedings of the IRE* with an unusually vivid title: "What the Frog's Eye Tells the Frog's Brain." Its authors were Jerome Lettvin, Humberto Maturana, Warren McCulloch, and Walter Pitts, and its central finding was startling enough that it still rewards a careful reading sixty-five years later.

The experiment was straightforward in concept. Lettvin and his colleagues placed electrodes in the optic nerve of a frog and observed which retinal ganglion cells fired in response to which visual stimuli. What they found was that the frog's retina doesn't send the brain a raw image. It sends the brain *processed features* -- small dark moving objects (bugs), large dark approaching shapes (predators), sharp edges, sudden dimming. By the time the signal reaches the frog's brain, the eye has already done substantial interpretation. The retina is not a camera. It's a feature extraction pipeline.

The implications reached beyond frog vision. If perception in even a simple vertebrate is not passive reception of raw data but active, structured, selective extraction of semantically meaningful features, then the prevailing model of how biological intelligence works -- sense first, interpret later -- was badly wrong. Meaning isn't added to perception after the fact. It's built into the extraction process itself. Intelligence, biological or artificial, doesn't work by accumulating raw data and reasoning over it afterward. It works by extracting structured signals and reasoning over *those*.

This turns out to be a claim about cognition in general, not just about frogs. The AI researchers who would spend the following decades trying to build systems that *know things* -- rather than merely store and retrieve them -- were, whether they realized it or not, trying to do in software what the frog's retina was already doing in wetware.

### Semantic Networks and the Frame Problem

The graph as a mathematical object is ancient. Euler's 1736 solution to the Königsberg bridge problem -- can you cross each of the city's seven bridges exactly once? -- is usually cited as the birth of graph theory, and the centuries of results that followed established it as a mature branch of mathematics long before anyone thought to use it for knowledge representation. Euclid's *Elements*, two thousand years earlier, had definitions, propositions, and logical dependencies between them that you could draw as a directed acyclic graph -- but Euclid wasn't making a claim about knowledge representation, he was doing geometry. The data structure, in some form, has always been available. The question was whether anyone would recognize it as the right structure for something other than bridges and triangles.

The answer, in the context of AI, arrived in 1966 with Ross Quillian's doctoral dissertation on semantic memory. Quillian was trying to represent the meanings of words -- not as dictionary definitions but as structured networks of relationships. The word "plant," in Quillian's model, wasn't defined by a string of text; it was a node connected by labeled links to other nodes representing its properties, its categories, its relationships to other concepts. This was recognizably a knowledge graph in embryonic form, and it established the semantic network as a tool for AI research.

Minsky's contribution, in his 1974 paper "A Framework for Representing Knowledge," was different in kind. He wasn't just proposing a data structure -- he was making a cognitive claim. The claim was that when humans encounter a situation, they don't process it from scratch. They retrieve a pre-existing structure -- a frame -- that represents a stereotypical version of that kind of situation, with slots for the details that vary. A "restaurant" frame has slots for host, menu, food, check, tip. When you walk into a restaurant you don't reason from first principles about what's happening -- you instantiate the frame and fill in the slots from what you observe. The frame carries default values for unfilled slots, which is how you know to expect a menu before one appears.

What made Minsky's paper feel vague to readers who wanted a specification -- and it did feel vague, the reaction was common and not a failure of reading -- was that he deliberately left open how frames were organized, how the right frame gets retrieved, how conflicts between frames get resolved, how new frames get created. These are hard problems and he largely left them open. He was sketching a research agenda, not specifying a system. In retrospect this was the right choice: premature formalization of a half-understood idea produces a wrong formalism that is harder to correct than a productive sketch. Minsky was doing what good theorists do at the frontier -- pointing confidently at something real without pretending to have fully characterized it.

The frame problem -- related to but distinct from Minsky's frames -- is the AI challenge of representing what *doesn't* change when something happens. If you move a block from one table to another, the block's color doesn't change. This seems obvious; it's extraordinarily difficult to formalize in a way that scales. Every action in a world has a vast number of things it doesn't affect, and a reasoning system that has to explicitly represent all of them is overwhelmed before it begins. The frame problem was one of the first demonstrations that human common sense, which handles this effortlessly, is hiding enormous computational complexity.

What frames and semantic networks got right -- what makes them the direct ancestors of the knowledge graph -- is the claim that the relationships *are* the knowledge. Not an index of facts with relationships as an afterthought, but a structure in which meaning is constituted by connection. A node in isolation is just a label. A node embedded in a graph of typed relationships to other nodes is a concept, with implications, with context, with a place in a web of meaning. This is not just a useful engineering observation. It is, as Minsky was arguing, a description of how intelligence works -- how a mind, human or artificial, can know what it knows in a way that supports inference rather than mere retrieval.

The knowledge graph as built today is in many ways the realization of what Minsky was gesturing at: a rigorous, computable, queryable structure where entities have typed relationships, where context shapes interpretation, where the graph itself carries meaning rather than merely pointing at it. The difference is that Minsky was working at the level of cognitive theory, and we are building infrastructure. The informality that frustrated impatient readers in 1974 has become, fifty years later, a schema definition language and a pipeline.

### Meaning is Relational

Douglas Hofstadter's argument in *Gödel, Escher, Bach* is directly relevant here, and the connection is tighter than it might first appear.

Hofstadter's central concern is how meaning arises in formal systems -- how symbols, which are just patterns, come to *refer* to things in the world. His answer, developed through the interweaving of Gödel's incompleteness theorems, Escher's self-referential drawings, and Bach's fugues, is that meaning isn't a property of individual symbols but of *symbol systems* -- of the relationships and transformations between symbols. A symbol means something because of its position in a web of other symbols and the rules that connect them. Isolate the symbol from that web and the meaning evaporates.

This is precisely the claim that frames and semantic networks were making, and that knowledge graphs embody. A node in a knowledge graph isn't meaningful in isolation -- "BRCA1" as a string of characters means nothing. It means something because of its typed relationships to other nodes: it *encodes* a protein, it *is associated with* breast cancer risk, it *interacts with* other genes, it *has synonym* "breast cancer type 1 susceptibility protein." The meaning is in the web, not in the label.

Hofstadter goes further in a way that connects to Chapter 5's argument. He distinguishes between what he calls *active symbols* and passive ones. A passive symbol is just a token that gets manipulated by external rules -- the symbols in a formal logical system, for instance. An active symbol is one that participates in its own interpretation, that has something like internal structure that fires in response to the right context. His argument is that genuine intelligence requires active symbols -- that what brains do, and what any sufficiently sophisticated reasoning system must do, is maintain a network of active symbols that mutually constrain and activate each other.

The knowledge graph, in this framing, is an attempt to make active symbols computationally tractable. Not just a passive lookup table but a structure where the typed relationships do real work -- where querying "what treats this disease" is not a string match but a traversal of a semantic network that carries the meaning of "treats" as a typed predicate with defined subject and object constraints. The graph doesn't just store the claim; it participates in the reasoning.

There's a passage in GEB where Hofstadter discusses the difference between the *map* and the *territory* -- between a representation and the thing it represents -- and argues that sufficiently rich representations develop a kind of isomorphism with their subject that amounts to genuine understanding. The representation isn't just *about* the territory; it captures enough of the territory's structure that reasoning over the representation produces true results about the territory. This is, almost word for word, the argument your Chapter 5 is making about knowledge graphs and grounded inference.

The connection you could draw in the book is something like: Hofstadter gave us the theoretical vocabulary for why symbol systems need to be relational rather than atomic, why meaning is constituted by connection rather than inherent in labels, and why a sufficiently structured representation can support genuine inference rather than mere retrieval. Minsky gave us the cognitive architecture -- frames as the natural unit of structured knowledge. The knowledge graph is what you get when you take both of those arguments seriously and ask: what does this look like as buildable infrastructure?

That lineage -- Quillian's semantic networks, Minsky's frames, Hofstadter's theory of meaning, arriving at the knowledge graph as a practical construction -- is the intellectual through-line of Chapter 2, and it's a stronger story for having all three in it.

### The Logic Wars

Expert systems, Prolog, description logics. Why they worked beautifully in narrow domains and collapsed under the weight of the real world. The brittleness problem.

### The Semantic Web and the RDF Era

Berners-Lee's grand vision. Why the vision was sound but the adoption economics were broken. Linked Data as a partial redemption.

### The Industrial Knowledge Graph

In May 2012, Google announced what it called its Knowledge Graph with a phrase that became a kind of slogan for the field: the goal was to understand "things, not strings." Instead of matching keywords to documents, Google wanted its search engine to understand that "Leonardo da Vinci" was an entity -- a person, with a birthdate, a nationality, a set of works -- and that queries about him were queries about that entity, not just about a sequence of characters. The knowledge panel that appears to the right of search results when you search for a person, place, or organization is the visible surface of this system.

The Knowledge Graph didn't emerge from nowhere. Its initial corpus was built primarily from Freebase, a structured knowledge base that a company called Metaweb had been developing since 2007 and that Google acquired in 2010. Freebase was itself a descendant of the collaborative, community-edited spirit of Wikipedia, but where Wikipedia stored knowledge as prose, Freebase stored it as structured facts: typed entities connected by typed relationships, contributed and edited by users. By the time Google folded it into the Knowledge Graph, Freebase contained roughly 44 million topics and 2.4 billion facts. Google supplemented this with Wikipedia, the CIA World Factbook, and other structured sources. The graph grew rapidly -- tripling in size within seven months of launch, reaching 570 million entities and 18 billion facts by the end of 2012, and eventually growing to hundreds of billions of facts on billions of entities.

What Google demonstrated at scale was that a knowledge graph was extraordinarily useful for a specific class of questions: factual queries about well-known entities. Who directed this film? When was this person born? What is the capital of this country? For these queries -- where the answer is a fact about a named entity that exists in the structured corpus -- the knowledge panel delivers an answer directly, without the user needing to click through to a source. This was genuinely transformative for search, and it established the knowledge graph as production infrastructure rather than academic exercise.

But it also revealed, somewhat quietly, what the approach could *not* do. The Google Knowledge Graph was built almost entirely from structured sources -- curated databases, collaborative encyclopedias, government factbooks. It was very good at facts that someone had already explicitly encoded. It had almost no ability to extract knowledge from the unstructured text that makes up the vast majority of what humans have written. Google's own internal research project, Knowledge Vault, attempted to address this -- automatically harvesting facts from across the web -- but it remained a research effort rather than a production system, and the problem of reliably extracting structured knowledge from free text remained essentially unsolved.

Freebase itself was shut down in 2016, its data migrated to Wikidata, the open collaborative knowledge base that now serves as one of the primary structured sources for the Knowledge Graph. The arc is instructive: even Google, with essentially unlimited engineering resources, found it easier to rely on human-curated structured data than to solve the extraction problem at the quality level required for production use. The extraction bottleneck wasn't a failure of ambition. It was a genuine hard problem that the tools of the time couldn't crack.

**The Extraction Bottleneck** -- Every era of knowledge representation described in this chapter ran into the same wall, approached from a different direction. The semantic networks of the 1960s and 70s had to be hand-built by knowledge engineers -- a process so labor-intensive that the resulting systems covered narrow domains at best. The expert systems of the 80s required domain experts to spend months encoding their knowledge as rules, and still couldn't capture the tacit understanding that experts applied effortlessly. The Semantic Web vision of the 90s and 2000s imagined a world where structured data would be published everywhere -- but the incentive for any individual publisher to do the hard work of structuring their content for others' benefit was never quite strong enough. And Google's Knowledge Graph, for all its scale, was built from the structured sources that already existed: databases, encyclopedias, factbooks. It was excellent at encoding what had already been made explicit. It had no way to reach the knowledge that hadn't.

The uncomfortable arithmetic is this: the vast majority of what humanity knows is written down in natural language -- in papers, books, reports, articles, case studies, clinical notes, legal opinions, engineering specifications, and a million other forms of text. This is where the knowledge lives. Not in databases. Not in ontologies. In sentences. And sentences, it turns out, are extraordinarily difficult to machine-read at the level required to extract structured, typed, confident knowledge from them.

The bottleneck persisted, decade after decade, as the tools improved incrementally but the fundamental economics of the problem remained the same. The knowledge was in the text. Getting it out reliably, at scale, across domains, remained out of reach.

Until, around 2022 and 2023, it suddenly wasn't. The rest of this book is about what changed, and what you can do with it.

---

## Chapter 3: The Dream

*Read this chapter with the awareness that the dream is grounded in the thesis: structured knowledge representation is the cognitive substrate for reasoning.*

### The Computer That Knows

Science fiction of the 1960s gave us a recurring dream: the computer you could simply ask. Not a database to query with the right syntax, not a search engine that returns links -- a machine that understood your question, knew the relevant facts, and told you the answer. HAL 9000, Multivac, the ship's computer that the captain addresses in plain English. The specifics varied but the fantasy was consistent: a machine that *knows things* the way a very well-read person knows things, and can reason from that knowledge rather than merely retrieve it. What would it actually take to build that?

### The Robot Scientist

Ross King's Adam and Eve systems. What they actually did: autonomous hypothesis generation, experimental design, execution, and belief updating. The yeast gene function discoveries. Why this is the most important existence proof in the field, and why it didn't make bigger waves. Adam and Eve did not just use a knowledge graph as a database; they used it as the substrate for autonomous reasoning. Make that connection explicit.

### The Cross-Disciplinary Machine

The argument that the most important insights may live *between* disciplines. A graph spanning medicine, chemistry, ecology, and materials science can see structural analogies invisible to any specialist. Historical breakthroughs that were essentially cross-domain pattern matches made by unusually well-read humans -- and the argument that a sufficiently rich KG does this systematically.

### The Machine That Knew Too Much

HAL 9000 as the dark mirror of the dream. Not a cautionary tale about AI turning evil -- something more philosophically interesting: a cautionary tale about underestimating what genuine language comprehension *implies*. The crew thought they understood the boundaries of HAL's capabilities and were wrong. A system that understands speech well enough to transcribe it understands speech well enough to read lips through a porthole. HAL as Shakespearean villain: always the smartest person in the room, always two moves ahead, always exploiting the gap between what others *think* they know and what is actually true. The lesson isn't fear -- it's epistemic humility about the capabilities you're creating. Plants a thematic tension that pays off in Part IV: the same capability that finds the unexpected drug interaction that saves lives is the capability that surfaces the unexpected inference you didn't intend to enable.

### The Gap Is the Book

Closing beat: the dream is coherent, the destination is visible. The missing piece is reliable extraction of structured, connected, provenance-tracked knowledge from unstructured text at scale.

---

## Chapter 4: What Is a Knowledge Graph, Really?

### Cutting Through the Buzzword Fog

A working definition that will hold for the rest of the book.

> A knowledge graph is a directed graph in which:
> 
> - **Nodes represent entities** -- discrete, identifiable things: people, places, substances, concepts, events. Not properties, not values, not free-floating text. Things that can be named, referenced, and recognized across sources -- and that's the critical word: *recognized*. When two papers mention the same gene, the same drug, the same disease, a knowledge graph can know they're talking about the same thing. That's what makes cross-source reasoning possible at all. Without it, you're not combining knowledge from multiple sources -- you're just accumulating text.
> - **Edges represent typed relationships** -- not generic connections but semantically defined predicates with a direction and a meaning. An edge labeled "inhibits" between a drug and an enzyme is a different kind of claim from one labeled "co-occurs with," and the distinction is not cosmetic.
> - **Every entity has a canonical identity** -- a stable identifier that persists across documents, authors, and time. The same gene is the same node whether a paper calls it by its official symbol, a common alias, or a misspelling. Resolving that multiplicity to a single identity is not bookkeeping; it's what makes the graph useful.
> - **Every relationship carries provenance** -- a traceable record of where the claim came from, by what method it was established, and with what confidence. A relationship without provenance is an assertion of unknown quality. A relationship with provenance is evidence.
> 
> These four properties together are what distinguish a knowledge graph from a labeled graph, a property graph, a document store, or a well-structured relational database. Any of the four can be relaxed for pragmatic reasons -- and sometimes they should be -- but relaxing them has costs that are worth understanding before you do it.

### Nodes, Edges, and What They Mean

Entities, relationships, and the critical point that a relationship isn't just a link. What distinguishes a KG from a property graph, a relational database, or a document store.

### The Semantics Matter

An edge without a type is nearly useless. Knowing that a drug and a disease are *connected* tells you almost nothing; knowing that the drug *treats* the disease, or *causes* it, or *is contraindicated in* patients with it, tells you something actionable. The meaning of the edge is the knowledge. The edge itself is just the plumbing.

Software engineers will recognize this intuition from type systems. An untyped variable that could hold anything is harder to reason about than one whose type tells you what operations are valid on it and what guarantees it carries. The same principle applies to edges in a knowledge graph: a typed relationship isn't just a label, it's a contract. It tells you what the subject and object are allowed to be, what direction the relationship runs, and what it means to assert it. A graph with well-typed edges is one that can catch its own errors -- an "inhibits" edge between two diseases, for instance, is probably a mistake, and a schema that defines valid subject and object types for each predicate will surface that mistake rather than silently incorporate it.

This seems obvious stated plainly, but it has consequences that are easy to underestimate during schema design. The temptation -- especially early, when you're trying to get extraction working at all -- is to start with a small number of generic relationship types and plan to refine them later. "Associated with" is the classic offender: it's easy to extract, it's never wrong, and it's almost never useful. A graph full of "associated with" edges is a graph that can support retrieval but not reasoning.

The flip side is also real: relationship types that are too narrow make extraction impractical. If your schema requires the model to distinguish between "directly inhibits," "allosterically inhibits," and "competitively inhibits," you've created a precision that the extraction step probably can't reliably deliver, and you'll spend more time correcting misclassifications than you'll gain from the distinction. The right level of semantic granularity is the one where the types are meaningfully distinct, expressible in natural language to an extraction model, and actually supported by what your sources say.

There's a third consideration that doesn't get enough attention: direction. "Drug A treats Disease B" and "Disease B is treated by Drug A" are the same fact, but in a directed graph they're different edges. Getting direction consistent across extraction runs and across sources is a detail that causes real headaches if it's not settled early. Treating direction as part of the type definition -- not just a convention but a constraint -- keeps the graph coherent as it grows.

### Provenance and the Epistemics of a Fact

Every edge in a knowledge graph is a claim. And claims, unlike data, have an epistemological status: they come from somewhere, they were established by some method, they are more or less certain, and they may conflict with other claims made by other sources. Provenance is the machinery that tracks all of this.

At minimum, provenance answers: *where did this relationship come from?* -- which source document, which section, which passage. But a well-designed provenance system goes further. It records *how* the relationship was established -- was it extracted by an LLM, identified by a named entity recognizer, asserted by a human curator? It records *confidence* -- not as a precise probability but as an ordinal signal about how much weight to give the claim. And in domains where it matters, it records the *epistemic type* of the evidence -- a randomized controlled trial is a different kind of claim from a case report, which is a different kind of claim from a computational prediction.

This last point deserves emphasis. In medicine, the Evidence and Conclusion Ontology (ECO) exists precisely because "there is evidence for this relationship" is not a single thing -- it's a spectrum from "one lab observed this once under unusual conditions" to "this has been replicated across fifty independent studies in multiple populations." A knowledge graph that conflates these is not just imprecise -- it's dangerous. A knowledge graph that preserves the distinction gives downstream reasoning systems something to work with.

The practical consequence is that provenance shouldn't be an afterthought bolted onto a graph that was designed without it. It should be a first-class schema concern from the start. In kgraph, this meant treating evidence as its own entity type -- not just a property of a relationship, but a node in the graph with its own identity, its own source, and its own relationship to the claim it supports. That design decision turns out to have large downstream implications: it makes provenance queryable, traversable, and aggregable across sources in ways that a simple confidence score attached to an edge cannot be.

A graph without provenance is a collection of claims with no way to evaluate them -- no way to ask "how well-supported is this?", no way to debug "why does the graph believe this?", no way to detect when two sources are in conflict rather than in agreement. Provenance is what separates a knowledge structure from a very large list of sentences that someone decided to believe.

### Identity: The Hard Problem

Canonical identity as a first-class concern, not an implementation detail. Identity is hard and consequential, being introduced at the level of abstraction appropriate for a chapter that's defining what a knowledge graph is. It's non-trivial, and treating it as an afterthought is a mistake. A graph where "BRCA1," "breast cancer gene 1," and "BRCA1 protein" are three separate nodes isn't a knowledge graph -- it's an index.

### What a KG Is Good For

Querying, traversal, hypothesis generation, LLM grounding.

### Build vs. Buy

Why someone would build their own rather than use Wikidata, SPOKE, ROBOKOP, or a commercial offering. The cases where existing graphs are sufficient, and the cases -- novel domains, proprietary corpora, custom schemas, provenance requirements -- where they aren't. An honest accounting rather than a sales pitch for the approach in this book.

### What a KG Is Not Good For

Honest accounting: KGs reflect the quality and coverage of their sources. They require maintenance. They can encode bias at scale.

---

## Chapter 5: Representation Is Reasoning

### From fluency to grounded reasoning

Chapter 1 established that LLMs are fluent but not grounded -- they have no way to gauge correctness or signal uncertainty, and they fail unpredictably when we leave the training distribution. The consequence that matters here: a system reasoning from statistical patterns fails in ways that are opaque, while a system reasoning from explicit, structured knowledge about the domain fails in ways that are traceable, correctable, and bounded by what's in the representation. That distinction is what the rest of this chapter is about.

### Experts already have a knowledge graph in their heads

Here is the argument for knowledge graphs, stated plainly: genuine reasoning about a complex domain requires a representation that makes the structure of that domain explicit, inspectable, and correctable. Not as an engineering convenience. As an epistemological necessity.

But there's a version of this argument that undersells itself, and it's worth avoiding. The weak version says: machines need explicit knowledge representations because they can't do what humans do implicitly. The strong version -- the one worth making -- says: humans need explicit knowledge representations too, for exactly the same reasons, and the best human expertise already has them, just not written down in a form that machines can use.

Think about what it means to be genuinely expert in a complex domain. A working cardiologist doesn't hold the relevant knowledge as a pile of facts. She holds it as a structured web of relationships -- this drug potentiates that pathway, this symptom cluster suggests this differential, this interaction is dangerous in patients with this history. The knowledge is relational. It has direction. It has confidence levels, implicitly -- she trusts the large randomized trials more than the case reports, the established mechanisms more than the preliminary findings. She has, in effect, a knowledge graph in her head, built over years of training and practice. What she doesn't have is an artifact that a machine can query.

The knowledge graph is not a substitute for that expertise. It's an attempt to make its structure explicit -- to take the relational model that the expert has built and put it in a form that can be shared, extended, corrected, and reasoned over by systems that didn't spend fifteen years in medical training. The central argument shifts from "machines need this" to something more interesting: machines and humans are doing the same thing, and now we can make the shared structure visible.

This reframing has a consequence that matters for how you think about the future of the field. The objection that large language models are getting better fast -- that the case for explicit knowledge representation is really just a case for not-yet-good-enough LLMs, and will dissolve as the models improve -- misses the point. A more capable language model reasons better over its training distribution. It does not, by virtue of being larger or better trained, acquire the specific, curated, provenance-tracked model of *this* domain as *this* community of experts currently understands it. That model is constructed through human judgment, domain expertise, and deliberate curation. No amount of training data substitutes for it, because training data reflects the past and the general, while a curated knowledge graph reflects the present and the specific. The cardiologist's knowledge graph, if it existed and were kept current, would contain things that aren't in any published paper yet -- the pattern she noticed last month, the contraindication that her department started flagging based on three recent cases, the consensus that has shifted but hasn't been formally written up. Training data is always behind the frontier of expert knowledge. A living graph doesn't have to be.

### Grounded representation as the fix

Chapter 1 argued that hallucination is baked in, not a bug. The fix is to give the model something to reason *from* -- explicit, structured, checkable claims. A knowledge graph does that: the model is shown edges, sources, and confidence, not asked to retrieve from statistical memory. That's a different cognitive task, and it produces different results.

### What you gain when the model is not a black box

A knowledge graph is a model of a domain, not the domain itself. This distinction sounds pedantic until you think about what it implies.

The implicit "model" inside a neural network is also a model of a domain -- or rather, of many domains simultaneously, encoded in weights that are not directly interpretable. It cannot be inspected. You cannot ask the model to show you its representation of the relationship between a drug and its target protein. You cannot correct it when that representation is wrong. You cannot extend it with new knowledge without retraining. You cannot audit it for bias or gaps. The model is a black box with a surface -- you can probe the surface, but the interior is not accessible.

An explicit representation -- a knowledge graph -- is a different kind of thing. It can be inspected. Every entity can be examined, every relationship can be queried, every provenance record can be traced back to its source. When it's wrong, it can be corrected. When the domain changes, it can be updated. When you want to know why the system believes something, you can follow the chain of evidence. Auditability is not just a nice property -- in any domain where the reasoning matters, it is a requirement. A physician using an AI system to inform a treatment decision needs to be able to ask "why" and get an answer that makes sense. A lawyer relying on an AI-assisted analysis needs to be able to trace the claim to its source. An explicit representation makes this possible. An implicit one doesn't.

The history of knowledge representation in AI is, in one reading, a long argument about this distinction. The expert systems of the 1980s had it right in principle: they reasoned over explicit representations, their inferences were in principle auditable, and when they were wrong you could usually figure out why. What they got wrong was the economics: building and maintaining those representations required armies of knowledge engineers working with domain experts, and it didn't scale. The logic-based systems were brittle because the representations were brittle -- incomplete, inconsistent, and expensive to update. The statistical revolution of the 1990s and 2000s threw out the explicit representation in favor of learned, implicit ones, and gained enormous practical capability at the cost of auditability. The current moment is the first time in the history of the field that it has been practically possible to build explicit, structured, domain-specific representations at scale without armies of knowledge engineers -- because the extraction step, the part that was always the bottleneck, can now be done by a language model with a well-designed prompt.

The argument comes full circle. Representation matters. Explicit representation matters more than implicit representation in any domain where the reasoning has to be auditable. Extraction is what makes explicit representation tractable at scale. Language models provide the extraction. The rest of this book is the engineering.

---

## Chapter 6: The Extraction Problem

### Text is subtler (and humans are smarter) than you would think

Consider this sentence, from a real paper in the cancer literature:

> Patients treated with the combination showed significantly reduced tumor burden compared to controls, though the effect was attenuated in those with prior platinum exposure.

Read it once and you already know, if you have any background in the domain, roughly what it's saying. There's a treatment -- a combination of something, referenced earlier in the paper -- that works against tumor growth. The evidence is significant, which means it cleared a statistical threshold. But the effect is weaker -- attenuated -- in patients who have previously received platinum-based chemotherapy. This is a clinically important qualification: prior platinum exposure is a common history in many cancer populations, so "works, but less well if you've had platinum" is a materially different clinical claim from "works".

Fifty words. A finding, a population, a comparison structure, a statistical hedge, a subgroup qualification, and an implicit clinical contraindication. A human reader with domain knowledge unpacks all of this in roughly the time it takes to read it once.

Now ask what it would take for a machine to do the same.

The finding itself is not stated as a simple subject-verb-object. "Patients treated with the combination" is the subject, but the combination is not named here -- its identity requires reading earlier in the paper, which requires co-reference resolution across sentence boundaries. "Showed significantly reduced tumor burden" is the claim, but "significantly reduced" is a statistical characterization, not a raw observation, and "tumor burden" is a clinical measurement that needs to be recognized as such and linked to its standard definition. "Compared to controls" establishes the comparison structure -- this isn't an absolute claim, it's a relative one, and losing that distinction changes the meaning. "Though the effect was attenuated" introduces hedging -- not a negation, but a qualification. And "prior platinum exposure" names a variable that modulates the effect, which means the machine needs to understand not just that platinum is a drug, but that prior exposure to it is a patient characteristic that interacts with treatment response.

This is not an unusually complex sentence for the biomedical literature. It's representative. And the extraction problem is the problem of reading sentences like this, millions of them, across thousands of papers, and producing structured, typed, provenance-tracked knowledge from them reliably enough to be useful.

### NLP was magnificent but still insufficient to the task

It is worth being honest about what the field of natural language processing actually achieved before large language models arrived, because the temptation to either overstate or dismiss that progress is real.

Named entity recognition -- NER -- had become genuinely practical by the mid-2010s. Systems trained on annotated biomedical corpora could identify genes, diseases, drugs, and chemicals in text with accuracy that was useful for downstream applications. The BioBERT family of models, pre-trained on PubMed abstracts and fine-tuned for specific tasks, set benchmarks that were hard to dismiss. Co-reference resolution -- the problem of knowing that "the compound" in one sentence refers to "imatinib" in the previous one -- made real progress, though it remained brittle on the long-range dependencies that appear routinely in scientific prose. Relation extraction -- identifying that two named entities stand in a specific relationship -- worked well in narrow domains with sufficient training data and carefully defined relationship types.

These weren't failures. They were genuine scientific and engineering progress, and the systems built on them were in production at pharmaceutical companies, biomedical literature services, and research institutions. The field knew what it was doing.

The brittleness showed up at the edges, and the edges were everywhere.

Domain adaptation was the first wall. A relation extraction system trained on biomedical literature needed to be substantially retrained to work on legal documents. The vocabulary was different, the sentence structures were different, the implicit conventions about how claims were stated were different. This wasn't a matter of fine-tuning a few parameters -- it was, in practice, a research project. You needed new training data, which meant new annotation, which meant hiring domain experts and building annotation pipelines and managing annotator disagreement. The cycle time from "we want to build a KG in this new domain" to "we have a working extraction pipeline" was measured in months, and the result was never quite as good as you hoped.

The annotation treadmill was the second wall, and it interacted badly with the first. Supervised extraction requires labeled data. Labeled data requires human judgment. Human judgment is expensive, inconsistent, and always slightly out of date. Domain experts disagree about edge cases -- and in complex domains, there are a lot of edge cases. Schemas evolve as understanding improves, which means last year's annotations are partially wrong for this year's schema. The pipeline you trained for the schema you had in January doesn't quite fit the schema you have in June. You annotate more data. You retrain. The schema changes again. The treadmill is always moving.

There was also something more fundamental. Classical NLP worked by learning statistical proxies for semantic relationships -- patterns of words, grammatical structures, co-occurrence statistics that correlated with the relationships you cared about. This worked well when the patterns were consistent and the training data was representative. It worked poorly on hedged language, because "did not inhibit" and "inhibits" have very similar statistical fingerprints but opposite meanings. It worked poorly on implicit relationships -- the kind where the text doesn't state the relationship directly but a knowledgeable reader infers it. It worked poorly on domain jargon that appeared rarely enough in training data to be statistically invisible. And it worked poorly, structurally, on anything that required integrating information across multiple sentences or multiple documents to establish a single relationship, because most classical architectures had no mechanism for that kind of extended context.

The honest summary: classical NLP built extractors that worked well on the easy cases, degraded gracefully on the medium cases, and failed in ways that were hard to characterize on the hard cases. For many applications, "works well on the easy cases" was sufficient. For building a knowledge graph from a large, diverse scientific literature, it wasn't.

### The economics and risk management of LLMs for extraction

The shift that large language models bring is not, primarily, a capability shift. It's an economic one, and the economic shift is what makes the capability shift matter.

The marginal cost of a new extraction task, with classical NLP, was a research project: weeks or months of work, annotated training data, iterative refinement against a domain-specific benchmark, deployment engineering, and ongoing maintenance as the schema evolved. For organizations with the resources to do this, it was feasible. For everyone else, it wasn't. Knowledge graph construction from unstructured text was, in practice, a capability available only to well-resourced actors in high-value domains.

The marginal cost of a new extraction task with a large language model is a prompt. Not a simple prompt -- a good extraction prompt takes thought, domain knowledge, and iterative refinement, and we'll spend a chapter on how to write one. But the cycle from "I want to extract this kind of relationship" to "I have a working extractor" is measured in hours, not months. Schema changes don't require retraining. A domain expert who can't write code can participate meaningfully in defining what the extraction should look for. The feedback loop between schema design and extraction quality -- always important, usually expensive to close -- becomes something you can iterate through in an afternoon.

This is a phase transition, not an incremental improvement. When the cost of a capability drops by two orders of magnitude, the set of people who can use it changes qualitatively, not just quantitatively. Knowledge graph construction from unstructured text is no longer a capability for organizations with research teams and annotation budgets. It's a capability for anyone with a corpus, a clear schema, and the patience to iterate on prompts.

What LLMs bring to the specific challenges of extraction is also worth being concrete about. Hedging and negation -- the bane of classical systems -- are handled naturally by a model that has learned from an enormous amount of human language, most of which contains hedging and negation. Implicit relationships -- the ones a knowledgeable reader infers rather than reads directly -- are within reach of a model with enough domain knowledge in its training distribution. Cross-sentence dependencies, which defeated most classical architectures, are handled by the attention mechanisms that are foundational to the transformer architecture. Domain jargon is less of a problem when the model has been trained on a corpus large enough to have seen most of it.

None of this is magic, and it's worth being precise about what it isn't.

Hallucination (Chapter 1) takes a specific form in extraction: the model can invent entity names that don't appear in the source, fabricate relationships the text doesn't assert, and misattribute provenance. Validation is not optional.

Context window limits matter for scientific literature, where a paper is often tens of thousands of words and the relationships that matter may span sections written pages apart. The chunking strategies in Chapter 10 are a response to this reality. They work, but they introduce their own complications: a relationship that spans a chunk boundary may be missed, and the context available to the model for any given extraction is always less than the full paper.

Cost at serious scale is real. Extracting a comprehensive knowledge graph from a large corpus -- hundreds of thousands of papers -- requires a large number of API calls, and API calls are not free. The economics are better than classical NLP at the research prototype scale and require more careful management at production scale.

And non-determinism -- the fact that the same prompt, run twice against the same text, may produce slightly different output -- has implications for reproducibility that any serious pipeline needs to address. Caching extraction results is not just an efficiency measure; it's a reproducibility measure.

This chapter ends honestly because the rest of the book is the engineering response to these limitations. LLMs are the best tool we have ever had for the extraction problem. That's a strong claim and the evidence for it is in the following chapters. But "best we've ever had" and "good enough to use without careful engineering" are not the same thing, and conflating them leads to pipelines that work in demos and break on real corpora.

---

# Part II: LLMs Change the Equation

## Chapter 7: Why LLMs Make This Practical Now

### The Economics Argument First

Before capability, cost. The reason classical NLP pipelines didn't democratize KG construction wasn't purely technical -- it was that adapting them to a new domain required a research project. LLMs shift the marginal cost of a new extraction task from months to hours. That's not an improvement in degree, it's a change in what's possible for whom.

### What LLMs Actually Are (For Our Purposes)

Brief forward reference to Chapter 1: when a model extracts, it's not magic or understanding in the human sense, but it's sufficient for the task. Here, focus on what matters for extraction -- the prompt as schema binding, what the model can handle that classical systems couldn't, and what remains limiting.

### The Prompt as Schema Binding

The key insight that makes LLM-based extraction different: you can describe your schema in natural language and the model will attempt to extract against it. This sounds obvious but its implications are large. Schema changes don't require retraining. Ambiguous cases can be handled with instructions rather than labeled examples. A domain expert who can't write code can participate in schema design in a meaningful way.

### Handling What Classical Systems Couldn't

Hedging and negation ("did not inhibit"), implicit relationships ("patients receiving drug X showed improvement" implies a treatment relationship), cross-sentence dependencies, domain jargon without explicit definition. Concrete examples from the medlit domain of sentences that would have broken a classical pipeline and how a prompted LLM handles them.

### The Remaining Limitations, Honestly

Don't rehash Chapter 1 or the detailed treatment in Chapter 6. List the limitations (hallucination in extraction, context window, cost, non-determinism) and point forward: the rest of the book is the engineering response.

### Why This Moment

A brief look at what changed between 2020 and now: model capability, API accessibility, cost curves, the ecosystem of tooling. The argument that we're in a window where this is newly practical but not yet crowded -- which is when it's worth building.

---

## Chapter 8: The Free KG Cases

### When You Don't Need Extraction

Some knowledge graphs aren't extracted -- they're generated, measured, or curated from sources that are already structured. Understanding these cases sharpens the argument for extraction by showing what the hard problem actually is. Perhaps you're getting data from some lab equipment or pulling it from a database table, and it already has a clear structure when you get it. Then all you need is to map the existing structure to your graph format, perhaps nothing more than a short shell script.

### Lab Instruments and Measured Data

Genomics as the canonical example: sequencers produce structured data almost by definition, and graphs like STRING or BioGRID are populated from experimental measurements rather than text mining. What these graphs look like, what they're good for, and what they miss -- because the experiment that wasn't done, or wasn't published as structured data, isn't in the graph.

### Generated and Synthetic Graphs

Knowledge graphs constructed from databases, ontologies, or formal specifications. The Gene Ontology, drug interaction databases, legal code graphs. High precision, limited to what was explicitly encoded. The boundary between a knowledge graph and a very well-structured database starts to blur here, which is instructive.

### Curated Graphs at Scale

Wikidata, Freebase before it, DBpedia. Human curation at scale: what it achieves, what it costs, and why it doesn't generalize to domains where the relevant knowledge lives in the literature rather than in encyclopedia articles.

### What These Cases Teach Us

The common thread: structured sources give you high-precision graphs over the knowledge that was *already structured*. The extraction problem is precisely the problem of accessing the knowledge that *wasn't* -- which, in most interesting domains, is the majority of what's known. The free KG cases set a quality benchmark worth aiming for and illustrate the shape of the gap.

### Hybrid Approaches

Most real KGs combine extraction with structured sources: link your extracted entities to Wikidata, anchor your drug names to a curated drug database, use the Gene Ontology as a backbone for your biomedical graph. The extraction problem doesn't go away but it's better constrained. This is actually what the medlit example does, and it sets up the authority lookup discussion in Part III.

---

## Chapter 9: Designing Your Schema

### Schema Design as Intellectual Work

This is the chapter that might surprise readers who came for the engineering. Schema design is where you make decisions about what your domain *is* -- what counts as an entity, what kinds of relationships matter, what level of granularity is useful. These are not technical decisions, they're epistemological ones, and they determine everything downstream.

### Entities: What Gets to Be a Thing

The question of what deserves a node in your graph. Genes, drugs, diseases, dosages, patient populations -- which of these are entities and which are properties of entities? The answer is neither obvious nor universal; it depends on the questions you want the graph to answer. A worked example of the medlit entity type decisions and the reasoning behind them.

### Relationships: Meaning and Direction

The difference between "co-occurs with," "inhibits," "causes," and "is associated with" is enormous, and collapsing them produces a graph that can't support real reasoning. How to define relationship types precisely enough to be useful without making them so narrow that extraction becomes impractical. The tradeoff between semantic precision and extraction recall.

### Hierarchy and Inheritance

When entity types should form a hierarchy and when flat is better. The temptation to over-ontologize -- building elaborate taxonomies that look impressive and make extraction harder without improving the graph's usefulness.

### Provenance as a First-Class Schema Concern

Revisiting the provenance argument from Chapter 4, now in a design context. How you represent where a fact came from isn't an afterthought -- it should be part of the schema from the start. The fields you'll regret not having later.

### Designing for Extraction

Schema choices that make LLM extraction easier versus harder. Relationship types that are hard to express in natural language. Entity types that are genuinely ambiguous even to a human reader. The feedback loop between schema design and extraction quality, and the argument for iterating on both together rather than finalizing the schema before you start extracting.

### Designing for Evolution

Your schema will change. New entity types you didn't anticipate, relationship types that turn out to be too coarse, distinctions that turn out to matter more than you thought. How to design in a way that doesn't make schema evolution catastrophic. Versioning, migration, and the argument for keeping the schema as simple as possible for as long as possible.

---

# Part III: Building It

The next three chapters examine issues that arose while working on my own software implementation of a knowledge graph system. The level of detail goes into the realm of engineering decisions. For non-engineers, the material here may feel a bit dense.

If you don't have to make engineering decisions yourself, you may wish to skim these chapters, or perhaps skip them entirely, and pick up again at chapter 13, "What Your Graph Can Do". Even if you skim, the chapter introductions sketch the main tradeoffs — which is enough to have an informed conversation with an engineer or a consultant about what you're building.

## Chapter 10: The Ingestion Pipeline

### The Pipeline as a Pattern, Not a Recipe

> Opens with an honest framing: the medlit pipeline is a worked example, not a template to copy. It reflects decisions made for a specific domain, a specific source format, and a specific set of tradeoffs. The value of studying it is understanding *why* each stage exists and what problem it solves -- which lets you decide, for your domain, whether you need that stage, a simpler version of it, or something different entirely. Use it as a **checklist of things to consider, not a specification to implement**.

### Why Multiple Passes at All

The case for staging extraction rather than doing it end-to-end in one shot. Each pass has a well-defined input and output. Failures are recoverable. Intermediate artifacts are inspectable and debuggable. The per-document bundle as the natural unit of work between passes. None of this is medlit-specific -- it's good pipeline design for any extraction problem at non-trivial scale.

### Parsing: Getting to Text

Whatever your source format, you need to get to structured text before you can extract anything. JATS XML (the PMC format) is medlit's case; yours might be PDFs, HTML, EPUB, proprietary formats, or plain text that's already clean. The decisions that matter regardless of format: how do you identify section boundaries, and how do you chunk for extraction? Too small and you lose context; too large and you exceed model limits or dilute signal. Sentence boundaries as a practical constraint worth respecting.

### Extraction: The LLM Pass

What gets sent to the model and what comes back. The extraction prompt as the place where your schema meets the text. A good extraction prompt binds your entity types and relationship types in natural language, handles hedging and negation explicitly, and instructs the model to capture provenance alongside content. The tradeoff between prompt specificity (higher precision) and prompt flexibility (higher recall). Iteration over the prompt is the design method -- there's no shortcut.

### A Note on Vocabulary

The medlit pipeline has an explicit vocabulary pass that runs alongside or after extraction. Not every domain needs this, but the underlying idea -- that your extraction will be more consistent if you first establish a shared vocabulary of entity names and their variants -- is worth understanding. If your domain has heavy terminology (medicine, law, chemistry), something like this will pay off. If your domain is more casual, you may not need it.

### Deduplication

The same entity extracted from many documents under slightly different names. Grouping mentions, resolving to canonical forms, handling the ambiguous cases. Embedding similarity as a signal. This stage is where the gap between "a list of extracted facts" and "a coherent graph" starts to close. The details will vary by domain, but the problem is universal.

### Assembly

Merging per-document extractions into a coherent whole. Relationship merging across documents -- multiple sources asserting the same relationship is meaningful signal that should strengthen confidence, not just create duplicates. What the final bundle looks like and why its structure is worth thinking about carefully before you start, because changing it later is expensive.

### Progress Tracking and Resumability

Large ingestion runs fail partway through. Design for restartability from the beginning. This isn't glamorous but it's the difference between a research prototype and something you can actually run.

---

## Chapter 11: Identity and Canonicalization

### Identity Is Load-Bearing

Canonical entities with canonical IDs are the design decision that most separates a useful knowledge graph from a sophisticated extraction exercise. They enable reasoning with apples-to-apples comparisons that span diverse sources. Everything else in the pipeline is in service of this. This chapter is about collapsing that multiplicity into something a reasoning system can actually use.

### The Scale of the Problem

A concrete illustration from medlit: a single gene across a corpus of thousands of papers might appear as its official symbol, common aliases, protein product names, misspellings, and context-dependent abbreviations. Multiply that across every entity type in every document, and identity resolution isn't a detail -- it's the central challenge.

### Canonical IDs as Primary Keys

The design decision to treat canonical IDs as the primary key rather than derived metadata. This sounds like an implementation detail but it has deep consequences. It forces the question "what is this entity, really?" at ingestion time rather than at query time. It makes the graph interoperable with external systems that use the same ID schemes. And it makes entity resolution a first-class concern rather than something you bolt on later.

### Authority Lookup: The Domain-Specific Part

In medicine there are established ontological authorities: UMLS for diseases and symptoms, HGNC for genes, RxNorm for drugs, UniProt for proteins. Your domain may have equivalents (legal citation systems, chemical databases, geographic identifiers, library catalog systems), or it may not. If it doesn't, you'll need to decide how to assign canonical IDs -- whether that's minting your own, using an open identifier scheme, or accepting that your graph is self-contained rather than interoperable. All of these are legitimate choices; what matters is making the choice deliberately.

### The Lookup Chain

When an entity arrives from extraction with a name but no ID: exact match, then fuzzy match, then embedding-based reranking. Knowing when to accept a match and when to leave an entity provisional is a tuning problem specific to your domain and your tolerance for false merges versus missed merges. False merges (collapsing two distinct entities into one) are generally worse than missed merges (leaving duplicates in the graph), but the right threshold depends on what you're doing with the graph.

### Provisional Entities and Promotion

Not everything gets resolved immediately, and that's fine. Provisional entities live in the graph until enough evidence accumulates, a better lookup succeeds, or a human reviewer makes a call. The promotion mechanism -- the thresholds that govern when a provisional entity earns canonical status -- is worth designing for your domain rather than borrowing wholesale from medlit, whose thresholds reflect LLM extraction characteristics in a medical context.

### The Synonym Cache

Whatever your lookup strategy, cache aggressively. Repeated lookups for the same term across a large corpus are expensive in API calls, latency, and money. A persistent synonym cache is not optional at any serious scale.

---

## Chapter 12: Provenance and Trust

*General argument: provenance is domain-dependent but when it matters it matters architecturally, not as an add-on. Evidence, not instruction.*

### Domain-Dependent Honesty

Provenance is not equally important in every domain. In medicine, the difference between "this drug inhibits this enzyme, from a single case report" and "this drug inhibits this enzyme, replicated across forty randomized controlled trials" is the difference between a hypothesis and a clinical fact. In theater arts, you may not care nearly as much where a relationship came from -- the graph is useful even if you can't trace every edge to a source. Be honest with yourself about how much provenance infrastructure your domain actually requires before you build it.

### What Provenance Buys You

When it matters, it matters a lot. A relationship with provenance -- specific source, section, extraction method, confidence, study design -- is evidence. Without provenance, a relationship in your graph is an assertion of unknown quality that you can neither verify nor weight. Provenance is also what lets you audit extraction quality, debug pipeline regressions, and answer the question "why does the graph say this?"

### Confidence as a Signal, Not a Guarantee

LLM confidence scores are useful ordinal signals, not calibrated probabilities. They tell you something about relative reliability across relationships, and they're worth tracking, but don't mistake them for ground truth. The honest framing: confidence is one input to trust, not trust itself.

### Multi-Source Relationships

When multiple independent sources assert the same relationship, that's meaningful signal. Designing your data model to aggregate evidence across sources -- rather than storing one relationship record per source -- is worth the extra complexity if your corpus is large enough that the same relationship will appear many times.

### Provenance at Query Time

The point of capturing provenance is being able to use it. A graph server that can answer "what's the evidence for this relationship" rather than just "does this relationship exist" is a qualitatively different tool. Whether you need that capability depends on your domain and your users. If you do need it, design for it from the start -- retrofitting provenance tracking into a schema that didn't anticipate it is painful.

---

# Part IV: What It Makes Possible

## Chapter 13: What Your Graph Can Do

*General argument: the value of the graph is in what grounded reasoning becomes possible, not in the serving layer. Evidence, not instruction.*

### The Server Is Not the Point

This chapter is about what becomes possible once your graph exists, not about how to build a particular server. The medlit project has a serving layer -- kgserver -- with REST, GraphQL, MCP, and persistent storage backends. You might build something like it, or you might expose your graph through a completely different interface, or you might not serve it externally at all. The infrastructure choices are yours. What this chapter is really about is the capability space: what can a well-constructed knowledge graph actually do for someone?

### Direct Querying

The basics: entity lookup, relationship queries, graph neighborhood traversal. These are useful and often sufficient for many applications. The interesting design question isn't which API style (REST, GraphQL, something else) but what the right query primitives are for your domain. What questions will your users actually ask?

### Graph Visualization

Of all the features in a graph serving layer, visualization has proven to have outsized value relative to its implementation cost. Seeing the graph -- as a browsable, zoomable network of entities and relationships -- does something for understanding that no amount of query output achieves. It surfaces structure that was invisible in the source documents, and it's the fastest way to catch extraction errors, spot unexpected patterns, and build intuition about your domain. If you build nothing else on top of your graph, build this.

### Grounding LLM Inference

The pattern that changes what a language model can do: instead of asking a model to reason from its training data, give it structured, typed, provenance-tracked claims from your graph and ask it to reason from those. The difference in reliability is substantial. A model hallucinating over raw text and a model reasoning over a curated graph with explicit provenance are doing qualitatively different things, even if they look similar from the outside. This is the integration that makes a knowledge graph more than a database.

### MCP as the Integration Point

The Model Context Protocol is worth understanding as an architectural pattern, not just as a specific technology. The idea is that a knowledge graph should be a first-class context source for LLM-based systems -- something that agents, assistants, and reasoning pipelines can query as naturally as a human researcher would reach for a reference database. Whether you use MCP specifically or some other integration approach, the principle is sound: your graph is most powerful when it's actively grounding inference, not sitting passively waiting to be queried by humans.

### Hypothesis Generation

The capability that arguably justifies building the graph in the first place, and the one that most clearly connects back to Chapter 3's Robot Scientist. Graph traversal as a discovery tool: not "what do we know about X" but "what's adjacent to X that hasn't been studied," "what entities are structurally similar to X in the graph," "what relationships exist between X and Y that no single paper asserts but that follow from combining multiple sources." These are queries that are impossible over raw text and natural over a well-constructed graph.

### Should Hypothesis Generation Be Baked In?

A question worth sitting with rather than answering too quickly. There's an argument that hypothesis generation is generic enough -- graph traversal, structural similarity, gap detection -- that it belongs in the framework rather than in domain-specific code. There's a counterargument that what counts as an interesting hypothesis is deeply domain-specific, and that baking it in prematurely produces a mechanism that nobody actually wants. The honest answer is probably that the *primitives* (traversal, similarity, subgraph queries) belong in the framework, and the *interpretation* of what makes a result interesting belongs in domain code or in the prompts given to whatever LLM is reasoning over the results.

### Returning to the Dream

A brief callback to Part I. Chapter 3 described the vision; Chapter 5 argued that representation is the prerequisite for principled reasoning; the rest of Part III has been the engineering. A functioning knowledge graph with a serving layer and LLM integration is not the Robot Scientist -- but it's the closest thing currently buildable. The gap between what you've just learned to construct and what Adam and Eve demonstrated is narrower than it looks.

---

## Chapter 14: The Augmented Researcher

### What Machines Would See That We Can't

Cognitive biases revisited with teeth: confirmation bias, prestige bias, recency bias, the Matthew effect in citation. A human reads thousands of papers in a career; a system reads millions. Now that the reader has seen how a KG is actually built, these arguments land differently -- this isn't speculation, it's an extrapolation of the system they've just learned to construct.

### The Combinatorial Argument

The scale of possible connections across a large graph versus what any individual researcher could survey. Structural analogies across disciplines. Formalizing the intuition that important results are already in the literature, unconnected, waiting.

### Linguistic and Geographic Blind Spots

What Western researchers actually engage with versus the full body of published science. A well-constructed KG with genuinely broad sourcing surfaces what citation networks systematically miss.

### The Robot Scientist, Revisited

Coming back to Adam and Eve now that the reader understands the extraction and graph construction machinery. What it would actually take to build something like this today. How close we are.

---

## Chapter 15: Who Benefits, Who Decides

### Democratization and Its Limits

A well-resourced KG as a potential equalizer for smaller institutions and developing-world researchers -- and the countervailing reality that building and maintaining one still requires significant resources. Who actually ends up with access.

### Compressed Discovery Timelines

Drug discovery, rare disease research, materials science. Concrete domains where the bottleneck is synthesis across a large literature and where a functioning extraction pipeline would meaningfully change the pace of work.

### The Rare Disease Problem

Research communities too small to synthesize their own literature. The structural argument that rare diseases are underserved not because nobody cares but because no single community is large enough to see the full picture. A KG as a coordination mechanism.

### Credit, Priority, and Provenance

When a machine surfaces a connection, who gets credit? Provenance tracking -- which the book has treated as a technical concern throughout -- turns out to have significant implications for scientific priority, intellectual property, and the sociology of research. The technical decision about how to record where a fact came from is also an ethical decision.

### Who Owns the Graph

Open versus proprietary. The tension between the scientific commons and commercial incentives. Historical analogies: who owned GenBank, who owns clinical trial data. What it would mean for a single entity to control a comprehensive KG over a significant scientific domain.

---

## Chapter 16: The Inference You Didn't Intend

*If the knowledge graph captures something essential to human expert understanding -- the deep structure of how a domain is organized -- then a system that reasons over it has access to the **architecture of expertise**, not just facts. The epistemic responsibility argument in this chapter should reflect that.*

### Returning to HAL

The lip-reading observation from Chapter 3, now with full context. A system capable enough to do what this book describes is capable enough to surface inferences its builders didn't anticipate and didn't design for. This isn't a flaw -- it's the point. But it deserves to be taken seriously.

### Dual Use at Graph Scale

The drug interaction that saves lives and the synthesis route that enables harm are both pattern-matching problems over structured knowledge. The same query interface serves both. What responsible construction and deployment actually looks like.

### Bias at Scale

A KG encodes the biases of its sources. If the literature over-represents certain populations, geographies, or research paradigms, the graph encodes that. At scale, these biases get laundered into the appearance of systematic knowledge. The mitigation strategies -- diverse sourcing, provenance transparency, explicit uncertainty representation -- and their limits.

### The Epistemic Responsibility of the Builder

What you owe to users of the system you build. Not a counsel of paralysis -- the right response to dual use isn't to not build -- but an argument that the builder's choices about provenance, transparency, access, and schema design are ethical choices, not just technical ones.

---

## Chapter 17: What's Next

### Open Problems

Honest assessment of what the approach in this book doesn't yet solve well: very long document contexts, multi-hop reasoning during extraction, real-time updating, schema evolution without re-extraction.

### Where the Field Is Going

Make explicit: the specific reasoning substrate will change -- LLMs today, something else in ten years -- but **the need for this grounding layer will not**. Whatever comes after LLMs will still need explicit, domain-specific, human-curated knowledge structure to reason reliably in specialized domains. The book is not documenting a technology moment; it is identifying a permanent architectural requirement that the current moment has finally made practical to address. Retrieval-augmented generation as a point of convergence with KG approaches. Structured world models in foundation models. The argument for why explicit, inspectable, provenance-tracked graphs remain valuable even as the substrate evolves.

### What I'd Do Differently

Personal reflection. The design decisions that turned out well, the ones that didn't, the things that seemed important early and faded, the things that seemed like implementation details and turned out to matter enormously.

### An Invitation

Closing beat: **the tools will change, the models will change, the need for this layer will not.** The reader who understands that is positioned to work on something durable. The tools are here, the need is real, the problems are interesting. This isn't a solved space -- it's an early map of a large territory. The reader who has made it this far has everything they need to go explore it.
