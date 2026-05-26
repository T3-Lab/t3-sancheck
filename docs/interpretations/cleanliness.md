# Cleanliness Interpretation

Overview
--------
Cleanliness is a dataset-level summary that combines four severity components into an overall score in [0,1]. The score is intended as a quick measure of data readiness.

Components
----------
- `missing_severity`: average proportion of invalid values per column (nan/inf/bad-parse).
- `type_severity`: average proportion of values that fail numeric coercion (`bad_type_ratio`).
- `similarity_severity`: dataset-level severity coming from strongly correlated feature pairs.
- `row_severity`: severity derived from row-level anomalies (see Anomalies doc).

How overall is computed
-----------------------
The code computes a penalty as a weighted sum:

```
penalty = 0.30*missing_severity + 0.20*type_severity + 0.20*similarity_severity + 0.30*row_severity
overall = clip(1.0 - penalty, 0.0, 1.0)
```

Labels
------
- `overall >= 0.85` → very clean
- `overall >= 0.70` → fairly clean
- `overall >= 0.50` → some issues
- `overall < 0.50` → dirty

Actionable guidance
-------------------
- High `missing_severity`: check ingestion, enforce schema, impute or drop low-quality columns.
- High `type_severity`: fix parsing issues, remove stray characters, cast columns to expected types.
- High `similarity_severity`: remove/merge redundant columns or use dimensionality reduction/regularization.
- High `row_severity`: inspect flagged rows and decide to correct, impute, or exclude them from modeling.

Notes & caveats
---------------
- Cleanliness is a heuristic summary: interpret alongside domain checks and model sensitivity tests.
- Component thresholds are context-dependent; small datasets can produce noisy averages.