---
title: Lateral Groove Width
node_type: concept
concept_type: design_parameter
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Lateral Groove Width

## Concept Type

design_parameter

## Definition

The width of grooves running laterally across the tread pattern.

## Key Claims

- The source reports that average tractive force on snow increased with lateral groove width in both prediction and experiment.
- Shear stress in the FEA results is mainly generated at lateral grooves.

## Design Implications

Increasing lateral groove width can improve snow traction by improving snow interaction in the contact patch, but it must be balanced against contact area, block support, and ice traction.

## Related Concepts

- [[Snow Traction]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: The source states that average tractive force on snow increased with lateral groove width.
- [[Tire Tread Pattern]]
  - relation: part_of
  - confidence: EXTRACTED
  - rationale: Lateral grooves are tread pattern features.
- [[FEA of Tire Traction on Snow]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source compares predicted and experimental traction for narrow and wide lateral grooves.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 11-12.
