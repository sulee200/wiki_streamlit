# Outcome-Only Package Insights for Snow Braking Development

## 1. Purpose

This note summarizes eight historically observed change packages that were associated with the actual winner in pairwise snow braking comparisons.

The analysis is **outcome-only**. It uses the actual pairwise result only, not model prediction columns. In practical terms, each package below should be read as:

> "In past pairwise comparisons, when the second tire had this directional package relative to the first tire, it won with the listed historical win rate."

These results are not proof of single-factor causality. Pattern, edge, mold, belt, compound, and weight changes often move together in tire development data. The intent is to identify development hypotheses that are directionally consistent with past winners and can guide future tire design review.

## 2. How To Read the Direction Terms

- `_up` means the first tire value was meaningfully higher than the second tire.
- `_down` means the first tire value was meaningfully lower than the second tire.
- `n` is the number of directional evidence rows supporting the package.
- `req` is the number of unique `req_no` values represented by those rows.
- The win rate is the historical package success rate, i.e. the share of directional rows where that package appeared on the actual winner side.

## 3. Feature Meaning

The compound feature meanings below are based on `Feature_Dict/ctb_column_dictionary_updated.md`.

- `Tg` / `delta_tg`: Glass transition temperature. Lower `Tg` generally indicates that the compound remains in a more rubbery, compliant state at lower temperature.
- `TAND_-10`, `TAND_-20`: Tan delta measured at -10 degC and -20 degC. In this outcome-only analysis, lower tan delta at these cold temperatures was more often associated with the actual snow braking winner.
- `HS`: Hysteresis. This is the compound energy-loss characteristic under deformation. In the selected package, `HS_up` means higher hysteresis on the winner side.

The pattern and edge feature meanings below are inferred from the engineered feature names used in the pairwise dataset.

- `edge_plain_total_by_width`: Plain edge resource normalized by tire or tread width. Higher values indicate more plain edge contribution per width.
- `edge_depth_total_per_pitch`: Edge depth resource normalized per pitch. Higher values indicate more depth-related edge resource within each pitch unit.
- `edge_shoulder_share`: Share of depth edge resource located in the shoulder region. Lower values indicate less shoulder-side concentration and relatively more redistribution away from shoulder.
- `land_pixel`: Pixel-based land area measure. Lower values indicate reduced land area in the pattern image representation.
- `land_ratio`: Ratio of land area to total pattern region. Lower values indicate more void/edge exposure relative to land.
- `tpi`: Total pitch count or pitch density feature. Higher values indicate more pitch segmentation.
- `kerf_pixel`: Pixel-based kerf/sipe measure. Higher values indicate more kerf/sipe expression in the image-derived feature.

## 4. Selected Historical Packages

### (1) Pattern and edge feature packages

| Package | Historical win rate | n / req | Interpretation and development insight |
|---|---:|---:|---|
| `edge_plain_total_by_width_up + land_pixel_down + land_ratio_down` | 75.5% | 110 / 56 | Past winners often had more plain edge resource per width while land area and land ratio were lower. This suggests a pattern direction where the tread exposes more functional edges and avoids excessive closed land area. For future snow braking development, this supports reviewing designs that increase plain edge availability while carefully reducing land dominance, without making the pattern mechanically weak. |
| `edge_shoulder_share_down + edge_plain_total_by_width_up + tpi_up` | 73.1% | 119 / 60 | Past winners tended to combine higher plain edge resource, higher pitch density, and lower shoulder-side edge concentration. This points toward distributing snow braking work away from an overly shoulder-heavy layout and increasing repeated biting opportunities through pitch segmentation. A future design implication is to raise useful edge frequency while keeping the edge distribution more central or balanced. |
| `edge_plain_total_by_width_up + kerf_pixel_up + tpi_up + edge_shoulder_down` | 72.9% | 118 / 60 | This package combines more plain edge, more kerf/sipe expression, higher pitch density, and lower shoulder edge share. It is a richer biting-edge package: more repeated pattern elements plus more kerf/edge detail, but less shoulder concentration. The development insight is that snow braking may benefit from increasing micro- and macro-edge opportunities together, as long as block stiffness is preserved. |
| `edge_shoulder_share_down + edge_plain_total_by_width_up` | 71.8% | 163 / 86 | This is the simplest edge package among the selected candidates and has the largest support within the edge/plain group. Historically, winners more often had higher plain edge resource and lower shoulder concentration. Because it uses only two terms, it is a useful baseline design rule: before adding complexity, check whether the candidate pattern increases plain edge resource while avoiding shoulder-heavy edge allocation. |
| `edge_shoulder_share_down + edge_depth_total_per_pitch_up + edge_plain_total_by_width_up` | 71.0% | 145 / 75 | Past winners often combined lower shoulder edge share with more depth edge resource per pitch and more plain edge per width. This suggests that not only the amount of edge matters, but also how much usable edge depth is packed into each pitch unit and where that edge is distributed. For future designs, this supports increasing edge resource density while keeping it from being too shoulder-biased. |


### (2) Compound feature packages

| Package | Historical win rate | n / req | Interpretation and development insight |
|---|---:|---:|---|
| `tand_-10_down + Tg_down` | 79.0% | 281 / 145 | This is the cleanest compound package among the selected candidates. Historically, the winner side often had lower tan delta at -10 degC and lower Tg. This suggests a cold-temperature compound direction where the material remains more favorable in the near-snow braking temperature range. For future development, this package supports prioritizing lower Tg and lower -10 degC tan delta as a compound screening signal, while still checking wear, dry/wet balance, and handling constraints. |
| `tand_-20_down + Tg_down` | 74.5% | 306 / 156 | This package is similar to the previous one but focuses on the colder -20 degC tan delta region. It has the largest support among the selected compound packages. Historically, winners often had lower Tg and lower -20 degC tan delta, which points toward a compound that remains effective deeper into the cold range. This is useful as a robustness check for cold-weather compound selection rather than a single-temperature rule. |
| `HS_up + tand_-10_down + Tg_down` | 66.2% | 133 / 76 | This package has a lower win rate than the other compound packages, but it is technically interesting. It combines higher hysteresis with lower -10 degC tan delta and lower Tg. The interpretation is not simply "softer is always better"; rather, it suggests a possible balance where the compound keeps favorable cold Tg/tan delta behavior while retaining or increasing hysteresis-related energy loss. For future development, this is a secondary hypothesis to test when trying to improve snow braking without losing too much compound response. |

## 5. Practical Takeaways

Across the selected packages, two directions repeat.

First, the pattern and edge packages point toward **more useful edge resource**: higher plain edge per width, higher edge depth per pitch, higher pitch/kerf expression, and lower shoulder-heavy edge concentration. The repeated signal is not just "more edge" but "more usable and better distributed edge."

Second, the compound packages point toward **lower Tg and lower cold-temperature tan delta** in the historical winner direction. The HS package adds nuance: hysteresis may still need to be maintained or increased in some cases, so the compound direction should not be reduced to a one-dimensional "make everything softer" rule.

For future tire development, the most actionable combined hypothesis is:

> Build candidate patterns with higher useful edge resource and less shoulder concentration, while pairing them with compounds that show lower Tg and lower cold-range tan delta. Then verify that pattern/block stiffness and hysteresis balance are not sacrificed.

Because the analysis is observational and outcome-only, these packages should be treated as development hypotheses. They are best used for candidate screening, design review, and follow-up experiment planning, not as final causal rules.
