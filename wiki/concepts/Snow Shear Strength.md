---
title: Snow Shear Strength
node_type: concept
concept_type: material_property
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Snow Shear Strength

## Concept Type

material_property

## Definition

The maximum shear stress snow can sustain before rupture, modeled as density-dependent in the analytical model and represented with yield criteria in FEA.

## Key Claims

- Snow in a tread void can support shear only while tire-induced shear stress stays below snow shear strength.
- Shear strength increases with snow density.
- In FEA, snow elastoplasticity is represented with a Mohr-Coulomb yield model.

## Design Implications

Snow traction benefits from compaction that raises shear strength, but only until void area reduction or rupture limits the usable force.

## Related Concepts

- [[Shear Force of Snow in Void]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: The source calculates maximum void shear force from snow shear strength.
- [[Snow Density]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source states that snow shear strength is a function of density.
- [[FEA of Tire Traction on Snow]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The FEA section validates a yield model through shear-box behavior.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 3, 6-7, and 9-10.
