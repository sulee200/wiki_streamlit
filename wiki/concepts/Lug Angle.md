---
title: Lug Angle
node_type: concept
concept_type: design_parameter
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Lug Angle

## Concept Type

design_parameter

## Definition

The angle of tread lugs measured from the lateral direction.

## Key Claims

- The source compares 0 degree, 30 degree, and -30 degree lug angles.
- FEA captures the same general tendency as experiments for traction and braking comparisons, but some braking ranking differs.

## Design Implications

Lug angle is a meaningful pattern variable for snow traction and braking, but it should be validated experimentally because model predictions may diverge for braking-dominant conditions.

## Related Concepts

- [[Snow Traction]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source compares tractive force and braking force on snow for different lug angles.
- [[Tire Tread Pattern]]
  - relation: part_of
  - confidence: EXTRACTED
  - rationale: Lug angle is a geometric property of the tread pattern.
- [[FEA of Tire Traction on Snow]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source validates lug-angle predictions against experiments.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 12-13.
