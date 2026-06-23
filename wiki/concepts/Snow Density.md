---
title: Snow Density
node_type: concept
concept_type: material_property
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Snow Density

## Concept Type

material_property

## Definition

The density of snow, including undisturbed road-surface density and compacted density inside the tire footprint.

## Key Claims

- Snow density in a void is estimated from measured void shrinkage.
- The source treats shear strength as a function of snow density.
- Fresh and aged snow differ in how force components contribute to traction.

## Design Implications

Snow tire predictions should parameterize snow state. A design that performs well in fresh snow may not have the same force balance in aged or compacted snow.

## Related Concepts

- [[Snow Shear Strength]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: The source states that snow shear strength is a function of snow density.
- [[Shear Force of Snow in Void]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: Higher compacted density can increase shear strength and therefore the void shear force.
- [[Void Shrinkage]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source estimates footprint snow density from void shrinkage.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 5-8.
