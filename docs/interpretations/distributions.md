# Distribution Interpretation

Purpose
-------
Explain per-feature distribution metrics produced by the analysis: entropy, spread score, variance and IQR. Use these to decide if a feature is informative, constant, or requires transformation.

Metrics
-------
- `entropy` (normalized, 0..1): measures unpredictability/diversity. For categorical features it is based on value counts; for numeric features it uses a histogram. Close to 1 → high diversity; close to 0 → low diversity or constant.
- `spread_score` (0..1): normalized measure of variance relative to a robust baseline derived from IQR. Close to 0 → narrow / low variance; close to 1 → wide spread or large variance relative to IQR.
- `variance` and `IQR`: raw moments. Variance is sensitive to outliers; IQR is robust.

Interpretation guidelines
------------------------
- Low entropy + low spread: likely constant or low-information feature — consider dropping.
- Low entropy + high spread: feature has a few common values and some extreme outliers — inspect outliers.
- High entropy + low spread: many distinct values but tightly clustered — check measurement precision or sampling.
- High entropy + high spread: typically informative continuous feature.

Actions
-------
- Drop or hash near-constant features.
- For heavy-tailed or wide-spread features apply scaling (standardization), winsorization, or transformation (log/Box-Cox).
- For high-cardinality categorical features, check if they are identifiers or leakage; consider grouping rare categories.

Caveats
-------
- Numeric entropy depends on binning (`ENTROPY_BINS` configuration). Interpret entropy with spread and domain context.