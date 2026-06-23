---
title: Snow Traction
node_type: concept
concept_type: performance_metric
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Snow Traction

## Concept Type

performance_metric

## Definition

Longitudinal tire performance on snow, expressed in the source through tractive or braking force and the snow traction coefficient, which is the ratio of tractive force on snow to normal load.

## Key Claims

- Snow traction depends on [[Tire Tread Pattern]], [[Slip Ratio]], snow material properties, and contact-patch force mechanisms.
- At moderate slip, traction can increase because shear deformation grows, but at high slip the [[Shear Force of Snow in Void]] disappears after snow fracture.
- Practical snow traction is difficult to optimize because improvements for snow can conflict with [[Ice Traction]].

## Design Implications

Design should balance void capacity, edge length, contact area, and snow compaction. Maximizing a single parameter such as [[Void Ratio]] can improve snow performance while harming ice performance.

## Related Concepts

- [[Analytical Model of Tire Traction on Snow]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source models snow traction using an analytical force decomposition.
- [[Void Ratio]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source states that increasing void ratio increases tire traction on snow.
- [[Slip Ratio]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source shows snow traction coefficient varying with slip ratio and peaking around moderate slip.
- [[Tire Tread Pattern]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source states that snow traction depends on pattern design and compares blank, blocked, and siped patterns.
- [[Ice Traction]]
  - relation: contradicts
  - confidence: EXTRACTED
  - rationale: The source describes an incompatibility dilemma where changes that improve snow traction can reduce ice traction.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 1 and 5.
