# Track 2 -- Technical Docs

1. **Overview** -- What this codebase is and the problem it solves. See *Knowledge Graphs from Unstructured Text* for the conceptual foundation and the argument for why this approach.
2. **Architecture** -- The major components (kgschema, kgraph, kgbundle, kgserver, examples) and how they relate.
3. **Schema Design Guide** -- How to define your domain's entities, relationships, and documents using kgschema.
4. **The Pipeline** -- Each stage in detail: parsing, chunking, extraction, dedup, resolution, bundle building.
5. **Canonical IDs and Entity Resolution** -- How identity works, authority lookups, the synonym cache.
6. **Storage and Export** -- In-memory storage, bundle format, query interface.
7. **Adapting to Your Domain** *(first-class chapter)* -- Step-by-step: define your schema, write your extraction prompts, configure your pipeline, validate your output.
8. **The medlit Example** -- Annotated walkthrough of the reference implementation.
9. **The Sherlock Example** -- A simpler/literary contrast case showing the framework's generality.
10. **Deployment and Operations** -- kgserver, Docker, MCP integration, running at scale.
11. **`kgserver/index.md`** -- The KGserver home page, living at the server's web root. Covers what the server exposes, how to connect to it, and how to query a running graph instance.
12. **Contributing** -- Internals, extension points, testing approach.

