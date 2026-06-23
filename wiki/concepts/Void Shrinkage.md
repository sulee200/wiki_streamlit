---
title: Void Shrinkage
node_type: concept
concept_type: design_parameter
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Void Shrinkage

## Concept Type

design_parameter

## Definition

The change in tread void volume inside the contact footprint relative to void volume outside the footprint, expressed in the source as Vol/Vol0.

## Key Claims

- Void volume shrinks when voids enter the footprint, remains nearly unchanged within the footprint, and recovers after leaving the footprint.
- Shrinkage increases compacted snow density but reduces void shear area.
- [[Shear Force of Snow in Void]] reaches a maximum at an optimum void shrinkage.

## Design Implications

Pattern, construction, and sidewall shape should be tuned to reach the void shrinkage that maximizes snow shear force, rather than simply maximizing void size or compaction.

## Related Concepts

- [[Shear Force of Snow in Void]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source shows void-shear force increasing up to an optimum as shrinkage changes.
- [[Snow Density]]
  - relation: causes
  - confidence: EXTRACTED
  - rationale: The source estimates compacted snow density in the footprint from undisturbed snow density and void shrinkage.
- [[Snow Shear Strength]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: Greater compaction raises snow density, and shear strength increases with density.
- [[Tire Tread Pattern]]
  - relation: related_to
  - confidence: INFERRED
  - rationale: The source notes optimum void shrinkage may be controlled by tire pattern, construction, or sidewall shape.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 6-7.
