---
title: Slip Ratio
node_type: concept
concept_type: performance_metric
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Slip Ratio

## Concept Type

performance_metric

## Definition

A tire operating condition describing the relative slip between the tire and road. In the source, it determines which snow traction force components contribute.

## Key Claims

- Snow traction coefficient reaches a maximum at slip ratios around 20-30% in the cited data.
- [[Shear Force of Snow in Void]] contributes at small slip ratio but not at large slip ratio.
- [[Plowing Force]] affects traction across slip ratios.

## Design Implications

Snow tire evaluation should examine the operating slip range. Designs that improve traction by preserving void-shear force may matter most near moderate slip, while edge and friction contributions remain important at high slip.

## Related Concepts

- [[Snow Traction]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source plots snow traction coefficient as a function of slip ratio.
- [[Shear Force of Snow in Void]]
  - relation: negatively_affects
  - confidence: EXTRACTED
  - rationale: The source states that at large slip ratio the shear force in snow voids makes no contribution because snow fractures.
- [[Plowing Force]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source states that the difference between siped and solid blocks is due to plowing force across slip ratios.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 4-5.
