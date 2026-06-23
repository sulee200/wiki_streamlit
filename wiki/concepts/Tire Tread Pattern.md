---
title: Tire Tread Pattern
node_type: concept
concept_type: design_parameter
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Tire Tread Pattern

## Concept Type

design_parameter

## Definition

The geometric arrangement of blocks, grooves, voids, lugs, and sipes in the tire footprint that governs how the tire interacts mechanically with snow.

## Key Claims

- Tread pattern controls shear stress distribution in snow and affects snow traction.
- Differences among blank, blocked, and siped tread patterns reveal separate contributions from void shear and edge plowing.
- Practical tread pattern effects can be studied using [[FEA of Tire Traction on Snow]].

## Design Implications

Pattern design should target useful snow shear in voids, sufficient lateral edge length, and controlled void deformation. Pattern changes should be evaluated for both snow traction and competing ice/contact-area requirements.

## Related Concepts

- [[Snow Traction]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: The source states that snow traction coefficient depends on pattern design.
- [[Shear Force of Snow in Void]]
  - relation: causes
  - confidence: EXTRACTED
  - rationale: The source says snow shear stress is produced by complex interaction between tread pattern and snow.
- [[Plowing Force]]
  - relation: causes
  - confidence: EXTRACTED
  - rationale: The source attributes plowing force to block and sipe edges in the tread.
- [[FEA of Tire Traction on Snow]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source uses simulation to compare practical tread patterns and their shear stress distributions.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 3-5 and 9-13.
