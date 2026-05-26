# Structure Interpretation

Purpose
-------
Identify relationships among features that affect modeling: strong pairwise similarity, multicollinearity, and overall structural complexity.

Metrics
-------
- `feature correlation` (absolute Pearson): used to find strongly similar pairs; pairs above the similarity threshold are reported.
- `similarity_report` / `similarity_severity`: identifies correlated column pairs and a severity combining pair ratio and mean correlation.
- `VIF (per_feature)`: raw variance inflation factor per feature; raw values > 5 (or >10) typically indicate problematic multicollinearity. The code also returns a normalized `mean` via `tanh(raw_mean / 10)` in [0,1].

Defaults
--------
- The analysis flags very strong correlations using `DEFAULT_SIM_THRESHOLD = 0.95` (i.e., near-perfect linear similarity).

Interpretation
--------------
- Pairs with abs(corr) >= 0.95: likely duplicated or linearly-derived features — consider merging or dropping one member.
- High per-feature VIF: a feature is predictable from others; models can become unstable (coefficients large/unstable).
- Normalized VIF mean near 1: dataset-level multicollinearity concern; near 0: low concern.

Actions
-------
- Remove or combine near-duplicate features; keep the most interpretable or complete column.
- Use PCA or feature selection when many features are highly correlated.
- Use regularized models (Ridge/Lasso) if removing features is not desirable.

Caveats
-------
- Correlation captures linear relationships only; non-linear dependencies may require mutual information or visualization.
- VIF is computed on numeric data with missing values dropped; ensure adequate sample size.

References
----------
- Default similarity threshold: `DEFAULT_SIM_THRESHOLD = 0.95`.