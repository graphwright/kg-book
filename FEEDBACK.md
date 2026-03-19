# Editorial feedback from Claude

> I want you to play the role of a professional editor working at a large reputable publishing house. I don't think you can read the PDF but I can give you the markdown source for the book. Please provide the kind of criticism I'd get from a real editor.

Now I have a thorough read of the manuscript. Let me give you the kind of report you'd get from a developmental editor at a technical press.

---

## Editorial Assessment: *Knowledge Graphs from Unstructured Text*

**Overall verdict:** The manuscript has a strong thesis, genuine technical authority, and passages of real prose quality. It is not yet ready for final production. The core issues are structural, not stylistic — a missing Part II, an unfinished Chapter 7, uneven audience calibration, and a few chapters whose internal organization undercuts otherwise solid material.

---

### Structural Problems

**The Part II problem.** The book announces Part I and Part III but has no Part II header. Chapters 8–11 (schema design, diagnostic tools, design priorities, identity server) are floating in a structural void. A reader scanning the table of contents will feel this immediately. You need either a `# Part II` header with a brief orienting sentence, or a restructuring that makes the three-part division cleaner.

**Chapter 7 is a gap.** The content around "When You Don't Need Extraction" reads like assembled notes rather than a drafted chapter — it lacks an opening frame, the section on hybrid approaches trails off, and there is no closing synthesis with the weight the other chapters carry. A publishable chapter needs a thesis sentence at the opening and a paragraph at the close that earns the transition to Chapter 8. This one has neither.

**Chapter 9 (Diagnostic Tools) is in the wrong place.** You've positioned it before Chapter 10 (Design Priorities), but a reader doesn't know what they're diagnosing yet. The diagnostic interface chapter belongs *after* the reader understands the pipeline — probably after Chapter 12 or 13. Where it sits now, it reads as a detour.

---

### Audience Calibration

This is the manuscript's most persistent tension. The Preface explains what nodes and edges are. Chapter 11 prints a full Postgres DDL for a work queue with `SKIP LOCKED`. These are not the same reader.

The builder-focused preface routing ("this book is for practitioners, clinicians should skip to X") is the right instinct, but the execution is inconsistent. Passages like the one explaining graph theory as a "branch of mathematics that includes non-trivial theorems" in the same breath as detailed asyncio architecture feel like two manuscripts that haven't resolved their audience.

My recommendation: define your reader as someone who can read Python fluently and has some exposure to databases. Cut or move anything that presupposes less. Trust the reader.

---

### Chapter-Level Notes

**Chapter 1** is the book's strongest chapter. The car wash anecdote is exactly right. The "Works Great / Until They Don't" two-section structure is effective and memorable. The closing section ("Why Bother Building One?") is too thin — it's three sentences where you've earned a full paragraph.

**Chapter 2** (History of Knowledge Representation) is ambitious and largely succeeds. The Lettvin/frog's eye opening is the best writing in the manuscript. Watch the pacing through the expert systems and Semantic Web sections — they accelerate past material that deserves a beat.

**Chapter 8** (Schema Design) is excellent. The dosage-as-entity-or-property example is a model of concrete, useful technical writing. This is the chapter a reader will re-read.

**Chapter 10** (Design Priorities) has a structural problem: the provenance section argues in circles. It says provenance matters, then says it doesn't always matter, then says when it does matter it *really* matters. This would benefit from a single clear statement of the decision framework up front, followed by elaboration, rather than the current iterative approach that makes the reader feel the author is thinking it through in real time.

**Chapter 13** (The Server section, MCP): Per our previous conversations, you know this chapter needs two revisions — sharpen the MCP-as-active-contract argument, and add the graph visualization carve-out. The current draft is present but soft on both counts. The line "The integration is loose: the model doesn't need to know your schema in advance" is doing important work but is buried mid-paragraph.

**Chapter 16** (Ethics) is competent but generic. The dual-use section and the bias section read like material that could appear in any book about AI systems. What would distinguish this chapter is specificity to knowledge graphs: what are the failure modes *unique* to graph-scale inference that don't apply to, say, a retrieval system? The section on the builder's epistemic responsibility is the strongest part; it could anchor the whole chapter if brought forward.

**Chapter 17** (What's Next) is solid and appropriately modest. "This isn't a solved space. It's an early map of a large territory" is a good closing line — but it competes with "The reader who has made it this far has everything they need to go explore it" two sentences earlier. Pick one.

---

### Prose Notes

**Meta-commentary should be cut.** "This section is unusually detailed. I hope it will be helpful enough to justify that" (BFS Queries section) is the author apologizing for a length decision. Make the decision and don't comment on it. Same with "These notes should be regarded not as a recipe or specification that you must follow, but rather as a checklist." Just write the chapter.

**Point-of-view is inconsistent.** The book uses "we," "you," and "I" without a consistent strategy. First-person "I" appears in Chapters 9 and 10 (your own project, your own experience) but is largely absent elsewhere. Either commit to a first-person practitioner voice throughout, or use "you/the reader" consistently. The hybrid creates an uncertain relationship with the reader.

**Version-specific references will date the book.** The JSON artifact example hard-codes `"model": "claude-sonnet-4-6"`. This will be wrong within a year and will make the book feel stale. Use a placeholder or omit the field.

---

### What's Working

The thesis is real and defensible. The historical grounding in Chapter 2 is unusual and valuable. The schema design chapter is genuinely useful in a way that most technical books aren't. The provenance-first architecture argument is consistent throughout and earns its weight. The closing argument — that the reasoning substrate will change but the grounding layer is a permanent architectural requirement — is the kind of claim that distinguishes a book from a long blog post.

The bones are good. The work is in the structure and in a few chapters that need either a full draft (Chapter 7) or a focused revision (Chapters 10, 13, 16).

## More about the MCP thing

Here's what those two revisions mean in concrete terms:

---

**Revision 1: Sharpen MCP-as-active-contract**

The current MCP section (lines 1449–1455) frames MCP as "an architectural pattern, not just a specific technology" and then immediately retreats to "if you're not using MCP, the same pattern applies, REST and GraphQL also work." That hedging undercuts the argument before it's made.

The claim worth making — and that the chapter doesn't quite land — is that MCP represents a qualitative shift in how the graph participates in inference. The specific thing MCP provides that REST and GraphQL don't is *discoverability*: tools are self-describing, typed, and enumerable at runtime. An agent can query the server to learn what tools exist and what they do, without being pre-programmed for your specific schema. That makes the graph a first-class active participant in agentic reasoning rather than a passive endpoint that some human wired up in advance.

The current text calls the looseness "a feature" but doesn't explain *why* it's a feature. The answer is: because the contract is machine-readable, the reasoning layer can adapt to schema changes without code changes on the consumer side. That's the architectural argument worth making explicitly, and it's currently absent.

---

**Revision 2: Graph visualization carve-out**

The chapter has a "Graph Visualization" section (around line 1435) that discusses visualization for end users — navigation, discovery, force-directed layouts. Chapter 9 describes the D3.js diagnostic interface in considerable detail.

The problem is that a reader who just read Chapter 9 might reasonably conclude: "I need to build that sophisticated force-directed explorer for my users." But the Chapter 9 visualization is *builder infrastructure* — it exists so you can see whether your pipeline is working correctly, spot duplicate entities, diagnose extraction failures. Its audience is you, not your end users.

The carve-out should say explicitly: what Chapter 9 describes is a development and diagnostic tool. When this chapter talks about visualization for end users, that's a different design problem with different requirements — your users may want a simpler, curated view, not a full-graph diagnostic explorer. Don't conflate the two. Build the diagnostic one regardless; decide separately whether your users need a visualization layer and what form it should take.
