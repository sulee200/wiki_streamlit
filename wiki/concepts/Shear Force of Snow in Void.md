---
title: Shear Force of Snow in Void
node_type: concept
concept_type: force
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Shear Force of Snow in Void

## Concept Type

force

## Definition

The traction-supporting force generated when snow packed into tread voids is compressed by vertical load and resists shear up to the snow's shear strength.

## Key Claims

- Snow packed into a void can sustain shear because compression increases its shear strength.
- This force is important at small [[Slip Ratio]] but disappears at large slip ratio after snow fracture.
- It depends on [[Snow Shear Strength]], [[Snow Density]], void area, and [[Void Shrinkage]].

## Design Implications

Tread design should create voids that compact snow enough to increase strength without shrinking the shear area so much that total shear force falls.

## Related Concepts

- [[Snow Traction]]
  - relation: positively_affects
  - confidence: EXTRACTED
  - rationale: The source includes this force as a positive term in small-slip snow traction.
- [[Slip Ratio]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source states that this force becomes small under high slip because snow fractures.
- [[Snow Shear Strength]]
  - relation: utilizes
  - confidence: EXTRACTED
  - rationale: The source defines maximum void shear force as an integral over snow shear strength.
- [[Void Shrinkage]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source calculates void shear force as a function of void shrinkage.
- [[FEA of Tire Traction on Snow]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The FEA section focuses on predicting the shear force of snow in voids.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 3-7 and 9-12.
