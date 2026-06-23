---
title: Edge Effect
node_type: concept
concept_type: phenomenon
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Edge Effect

## Concept Type

phenomenon

## Definition

The snow-traction effect produced when block and sipe edges dig into snow, corresponding to [[Plowing Force]] in the analytical model.

## Key Claims

- Edge effect is associated with the plowing force at tread block and sipe edges.
- It can be roughly estimated from the edge length of the tread pattern.

## Design Implications

Edge length and edge orientation should be treated as explicit snow-traction design variables, especially for traction at high slip where void-shear force is no longer active.

## Related Concepts

- [[Plowing Force]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source identifies plowing force at block and sipe edges as edge effect.
- [[Tire Tread Pattern]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The effect depends on tread block and sipe edges.
- [[Snow Traction]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: The edge effect contributes to the analytical traction force.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 4 and 7.
