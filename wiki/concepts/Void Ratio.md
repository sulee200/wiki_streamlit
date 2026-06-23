---
title: Void Ratio
node_type: concept
concept_type: design_parameter
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Void Ratio

## Concept Type

design_parameter

## Definition

The ratio of void area to the area of the tire footprint.

## Key Claims

- Higher void ratio increases [[Snow Traction]].
- Higher void ratio decreases [[Ice Traction]] because it reduces tire-ice contact area.
- The snow/ice trade-off cannot be solved by changing void ratio alone.

## Design Implications

Void ratio is a primary but limited design lever. It should be co-optimized with edge length, tread pattern, and void deformation behavior rather than treated as a standalone snow-traction maximizer.

## Related Concepts

- [[Snow Traction]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: The source states that tire traction on snow increases when void ratio increases.
- [[Ice Traction]]
  - relation: negatively_affects
  - confidence: EXTRACTED
  - rationale: The source states that tire traction on ice decreases when void ratio increases because contact area is reduced.
- [[Tire Tread Pattern]]
  - relation: related_to
  - confidence: INFERRED
  - rationale: Void ratio is a footprint-level pattern parameter controlled by the arrangement of grooves and blocks.
- [[Void Shrinkage]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source evaluates snow shear in voids through void volume changes inside and outside the footprint.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 1 and 6-7.
