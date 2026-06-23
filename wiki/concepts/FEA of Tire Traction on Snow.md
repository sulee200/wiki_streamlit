---
title: FEA of Tire Traction on Snow
node_type: concept
concept_type: analysis_method
sources:
  - "[[advanced-tire-mechanics-1-snow]]"
last_updated: 2026-06-18
---

# FEA of Tire Traction on Snow

## Concept Type

analysis_method

## Definition

Computational analysis of tire-snow interaction using finite element modeling for the tire and finite volume or Eulerian treatment for snow, coupled to predict snow deformation and shear forces.

## Key Claims

- FEA can analyze practical tread patterns that simpler models could not previously handle.
- Simulation makes shear stress distributions visible in the contact patch.
- The cited simulation predicts the experimental tendency that wider lateral grooves increase average tractive force on snow.
- Prediction trends for lug angle are qualitatively useful, though braking-force predictions still show discrepancies.

## Design Implications

FEA can screen tread designs and expose where snow shear is generated, especially around lateral grooves. Its results should be interpreted as pattern-directional evidence unless quantitatively validated for the specific snow and tire condition.

## Related Concepts

- [[Tire Tread Pattern]]
  - relation: utilizes
  - confidence: EXTRACTED
  - rationale: The source applies FEA to tires with practical tread patterns and compares pattern designs.
- [[Shear Force of Snow in Void]]
  - relation: utilizes
  - confidence: EXTRACTED
  - rationale: The simulation focuses on predicting the shear force of snow in voids.
- [[Lateral Groove Width]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source validates FEA against experiments varying lateral groove width.
- [[Lug Angle]]
  - relation: related_to
  - confidence: EXTRACTED
  - rationale: The source validates FEA tendencies for tread patterns with different lug angles.
- [[Snow Shear Strength]]
  - relation: utilizes
  - confidence: EXTRACTED
  - rationale: The simulation uses a Mohr-Coulomb yield model to represent snow shear behavior.

## Source

- [[advanced-tire-mechanics-1-snow]] pages 9-13.
