---
title: Analytical Model of Tire Traction on Snow
node_type: concept
concept_type: model
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# Analytical Model of Tire Traction on Snow

## Concept Type

model

## Definition

A longitudinal snow-traction model that decomposes tire force on snow into snow compression, snow shear in voids, tread-snow friction, and edge/plowing effects.

## Key Claims

- At small slip ratio, tractive force is represented by [[Shear Force of Snow in Void]], [[Frictional Force Between Tread and Snow]], [[Plowing Force]], and the opposing [[Braking Force from Snow Compression]].
- At large slip ratio, the void-shear force and forward-motion snow compression contribution are removed from the tractive-force expression.
- The model predictions agree well with measured static traction and traction at slip ratio 1.0 in the source data.

## Design Implications

The model gives tire designers interpretable knobs: increase useful void shear, tune edge length, manage frictional contact, and reduce harmful snow compression resistance.

## Related Concepts

- [[Snow Traction]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The model quantitatively predicts tire traction on snow.
- [[Shear Force of Snow in Void]]
  - relation: consists_of
  - confidence: EXTRACTED
  - rationale: The source lists snow shear in voids as one of the four modeled forces.
- [[Frictional Force Between Tread and Snow]]
  - relation: consists_of
  - confidence: EXTRACTED
  - rationale: The source lists tread-snow friction as one of the modeled forces.
- [[Plowing Force]]
  - relation: consists_of
  - confidence: EXTRACTED
  - rationale: The source lists plowing force at block and sipe edges as one of the modeled forces.
- [[Braking Force from Snow Compression]]
  - relation: consists_of
  - confidence: EXTRACTED
  - rationale: The source lists snow-compression braking force as one of the modeled forces.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 3-8.
