# Snow Tire Knowledge Base Agent — Schema & Workflow Instructions

This repository contains a concept-centric knowledge base for snow tire mechanics.

The primary objective is not document summarization, but extraction of:

* key physical concepts
* causal relationships between concepts
* evidence supporting those relationships
* design implications for snow tire performance

The knowledge base will ultimately support an agent capable of reasoning about:

* snow traction mechanisms
* tire design trade-offs
* potential design modifications to improve snow performance

---

## Concept Extraction Principles

Prefer fewer high-quality concepts over many fragmented concepts.

A concept should represent a meaningful:

* design parameter
* material property
* force
* phenomenon
* performance metric
* analysis method
* model

Avoid creating concepts that are merely:

* section titles
* synonyms
* examples
* temporary descriptions
* overly specific phrases

Merge concepts whenever they describe the same underlying mechanism.

Prioritize concepts that contribute directly to understanding or improving snow tire performance.

---

## Allowed Relation Types

Graph relationships MUST use only:

* positively_affects
* negatively_affects
* consists_of
* part_of
* utilizes
* causes
* contradicts
* related_to

Definitions:

* positively_affects: improvement or increase in source tends to improve target
* negatively_affects: increase in source tends to degrade target
* consists_of: source contains target as a component
* part_of: source is a component of target
* utilizes: source uses or relies on target
* causes: source directly produces target
* contradicts: source conflicts with target
* related_to: meaningful relationship exists but does not fit another category

---

## Allowed Confidence Levels

Confidence describes the reliability of a graph relationship (edge), not the validity of a concept node.

Every graph relationship must have one confidence label:

* EXTRACTED
* INFERRED
* AMBIGUOUS

Definitions:

* EXTRACTED: explicitly stated in the source
* INFERRED: reasonable interpretation based on source evidence
* AMBIGUOUS: relationship is uncertain and requires review

---

## Directory Layout

```text
raw/          # immutable source documents

wiki/
  index.md
  log.md
  overview.md

  sources/
  concepts/
  syntheses/

graph/

tools/
  health.py
  lint.py
  build_graph.py
```

Entity pages are disabled by default.

The primary unit of knowledge is the concept page.

---

## Page Format

Every concept page must use:

```yaml
---
title: Concept Name
node_type: concept
concept_type:
sources: []
last_updated: YYYY-MM-DD
---
```

Use `[[Concept Name]]` wikilinks whenever a concept references another concept.

Graph relationships should be stored in the `Related Concepts` section of concept pages and serve as the primary source for graph generation.

Confidence values describe the reliability of graph relationships (edges), not concept nodes.

---

## How to Use

Describe what you want in plain English:

* "Ingest this file: raw/advanced-tire-mechanics-snow.md"
* "What concepts influence snow traction?"
* "What design parameters positively affect snow traction?"
* "Build the knowledge graph"
* "Suggest tire design modifications based on the current knowledge graph"

Or use shorthand triggers:

* ingest <file>
* query: <question>
* health
* lint
* build graph

```
```

---
## Ingest Workflow

Triggered by: *"ingest <file>"*

**Supported formats:** Markdown (`.md`) is ingested directly. Non-markdown files (`.pdf`, `.docx`, `.pptx`, `.xlsx`, `.html`, `.txt`, `.csv`, `.json`, `.xml`, `.rst`, `.rtf`, `.epub`, `.ipynb`, `.yaml`, `.yml`, `.tsv`, `.wav`, `.mp3`) are auto-converted to markdown via markitdown before ingestion.

### Goal

Build a concept-centric knowledge base focused on snow tire mechanics.

The wiki should capture:

* Core concepts
* Relationships among concepts
* Evidence supporting those relationships
* Design implications for snow tire performance

---

### Steps (in order)

1. Read the source document fully (auto-convert if needed).

2. Read:

   * `wiki/index.md`
   * `wiki/overview.md`

3. Create or update:

   `wiki/sources/<slug>.md`

   using the Source Page Format.

4. Update `wiki/index.md`

   * Add source page entry.
   * Add newly discovered concept pages.

5. Update `wiki/overview.md`

   * Revise overall understanding of snow traction mechanisms.
   * Update high-level concept map if necessary.

6. Identify important concepts.

   Concepts may belong to:

   * design_parameter
   * material_property
   * force
   * phenomenon
   * performance_metric
   * analysis_method
   * model

7. Create or update concept pages.

   Merge information into existing concepts whenever possible.

   Do NOT create duplicate concepts.

8. For each concept page:

   * Update Definition
   * Update Key Claims
   * Update Design Implications
   * Update Related Concepts
   * Update Source Evidence

9. Extract graph relationships.

   Allowed relations:

   * positively_affects
   * negatively_affects
   * consists_of
   * part_of
   * utilizes
   * causes
   * contradicts
   * related_to

   Allowed confidence levels:

   * EXTRACTED
   * INFERRED
   * AMBIGUOUS

10. Every relationship MUST include:

* target concept
* relation type
* confidence
* rationale

11. Flag contradictions with existing wiki content.

12. Append to:

`wiki/log.md`

```
## [YYYY-MM-DD] ingest | <Title>
```

13. Post-ingest validation

* Verify all wikilinks exist.
* Verify every concept appears in `index.md`.
* Verify every relation uses an allowed relation type.
* Verify every relation includes confidence.
* Print a change summary.

---

### Concept Page Requirements

Each concept page MUST follow:

```markdown
---
title: Concept Name
node_type: concept
concept_type:
sources: []
last_updated: YYYY-MM-DD
---

# Concept Name

## Concept Type

## Definition

## Key Claims

## Design Implications

## Related Concepts

Relationships stored in this section represent graph edges.

Each relationship must contain:

- target concept
- relation
- confidence
- rationale

## Source
```

---

### Relationship Format

Inside `## Related Concepts`:

```markdown
- [[Snow Traction]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: Increased contact pressure improves snow compaction and traction generation.
```

Only the allowed relation types may be used.

These relationships are the primary source used by the Graph Workflow when generating `graph/graph.json`.

---

## Query Workflow

Triggered by: *"query: <question>"*

Steps:
1. Read `wiki/index.md` to identify relevant pages
2. Read those pages
3. Synthesize an answer with inline citations as `[[PageName]]` wikilinks
4. Ask the user if they want the answer filed as `wiki/syntheses/<slug>.md`

---

## Lint Workflow

Triggered by: *"lint"*

Check for:
- **Orphan pages** — wiki pages with no inbound `[[links]]` from other pages
- **Broken links** — `[[WikiLinks]]` pointing to pages that don't exist
- **Contradictions** — claims that conflict across pages
- **Stale summaries** — pages not updated after newer sources
- **Sparse pages** — pages with fewer than 2 outbound `[[wikilinks]]` (link density budget)
- **Data gaps** — questions the wiki can't answer; suggest new sources

Graph-aware checks (require `graph.json` from `build graph`):
- **Hub stubs** — god nodes (degree > μ+2σ) with thin content (< 500 chars)
- **Fragile bridges** — community pairs connected by only 1 edge
- **Isolated communities** — clusters with zero external connections

Output a lint report and ask if the user wants it saved to `wiki/lint-report.md`.

---

## Health Workflow

Triggered by: *"health"*

Run: `python tools/health.py` (or `python tools/health.py --json` for machine-readable output)

Fast structural integrity checks — **zero LLM calls**, safe to run every session:
- **Empty / stub files** — pages with no content beyond frontmatter (rate-limit damage)
- **Index sync** — `wiki/index.md` entries vs actual files on disk
- **Log coverage** — source pages missing a corresponding `ingest` entry in `wiki/log.md`

Output a health report. Use `--save` to write to `wiki/health-report.md`.

### Health vs Lint Boundary

| Dimension | `health` | `lint` |
|---|---|---|
| **Scope** | Structural integrity | Content quality |
| **LLM calls** | Zero | Yes (semantic analysis) |
| **Cost** | Free | Tokens |
| **Frequency** | Every session, before other work | Every 10-15 ingests |
| **Checks** | Empty files, index sync, log sync | Orphans, broken links, contradictions, gaps |
| **Tool** | `tools/health.py` | `tools/lint.py` |
| **Run order** | First (pre-flight) | After health passes |

> Run `health` first — linting an empty file wastes tokens.

---
## Graph Workflow

Triggered by: *"build graph"*

### Goal

Build a concept-centric knowledge graph from the wiki.

The graph should:

* Preserve the existing wiki generation workflow.
* Generate `graph/graph.json`.
* Generate `graph/graph.html`.
* Represent concepts and their relationships.
* Support future agent reasoning about snow tire performance and design improvement.

Run:

`python tools/build_graph.py --open`

---

### Graph Extraction Rules

#### Nodes

A node represents one stable wiki concept page.

Preferred source:

* `wiki/concepts/*.md`

Entity pages are disabled by default.

Node IDs must:

* be lowercase
* contain only `[a-z0-9_]`
* be generated from the normalized page title

Examples:

* Snow Traction → `snow_traction`
* Contact Pressure → `contact_pressure`
* Void Ratio → `void_ratio`

Each node should contain:

* title
* concept_type
* source_file
* page path
* preview text
* full markdown content

---

#### Edges

Edges are extracted primarily from the `## Related Concepts` section of concept pages.

Allowed relations:

* positively_affects
* negatively_affects
* consists_of
* part_of
* utilizes
* causes
* contradicts
* related_to

No other relation labels are allowed.

If a relationship does not clearly fit the whitelist, use `related_to`.

---

### Relation Definitions

#### positively_affects

An increase or improvement in the source concept tends to improve the target concept.

#### negatively_affects

An increase in the source concept tends to degrade the target concept.

#### consists_of

The source concept contains the target concept as a component.

#### part_of

The source concept is a component of the target concept.

#### utilizes

A concept, method, or model uses another concept.

#### causes

A direct causal relationship exists.

#### contradicts

The relationship is explicitly contradictory.

Use only when clearly supported by source material.

#### related_to

A meaningful relationship exists but does not fit another category.

---

### Confidence

Allowed confidence labels:

* EXTRACTED
* INFERRED
* AMBIGUOUS

#### EXTRACTED

Relationship is explicitly stated in the source material or wiki page.

#### INFERRED

Relationship is a reasonable interpretation supported by evidence.

#### AMBIGUOUS

Relationship is uncertain and should be reviewed.

---

### Required Edge Metadata

Every edge MUST contain:

* relation
* confidence
* rationale

and should include source evidence whenever available.

Expected format inside `## Related Concepts`:

* `[[Snow Traction]]`

  * relation: positively_affects
  * confidence: EXTRACTED
  * rationale: Higher contact pressure improves snow compaction and increases traction generation.

---

### Graph JSON Schema

Each node should contain:

* id
* label
* node_type
* concept_type
* path
* source_file
* preview
* markdown

Each edge should contain:

* source
* target
* relation
* confidence
* confidence_score
* rationale
* source_file
* weight

---

### HTML Visualization

Generate:

`graph/graph.html`

using a graphify-style vis.js visualization.

Required features:

* zoom and pan
* search box
* relation filter
* confidence filter
* concept-type coloring
* interactive sidebar

#### Node Click

When a node is clicked, display:

* title
* concept_type
* source
* preview
* full wiki page content

#### Edge Click

When an edge is clicked, display:

* source node
* target node
* relation
* confidence
* rationale
* source evidence

---

### Graph Validation

Before saving:

Verify:

* all node IDs are valid
* all edge endpoints exist
* all relations belong to the whitelist
* all confidence values belong to the whitelist
* all concept pages contain a Related Concepts section
* all edges contain rationale

Broken wikilinks should be reported but never auto-created.

---

### Graph Health Report

Triggered by:

* `graph report`

or

* `python tools/build_graph.py --report`

The report should include:

* node count
* edge count
* orphan nodes
* hub nodes
* community count
* invalid relations
* invalid confidence labels
* missing rationale
* broken wikilinks

Save to:

`graph/graph-report.md`

---

### Hard Rules

* Never invent relation types.
* Never invent confidence labels.
* Never auto-create pages from broken links.
* Prefer concept pages over source pages.
* Preserve full wiki page content inside graph nodes.
* The graph must remain compatible with the graph.html visualization.
