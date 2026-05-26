# Anomaly Interpretation

Purpose
-------
Detect rows with invalid numeric values and per-row anomaly scores. This document explains the outputs from `problematic_row_report` and how to interpret them.

Key metrics
-----------
- `row_anomaly_score` — per-row score in [0, 1]. Computed using a robust z-score (median + MAD) and scaled via `z/(z+1)`, then averaged across columns.
- `has_invalid_numeric` — boolean flag if a row contains NaN/Inf/non-finite values after numeric coercion.
- `invalid_ratio` — proportion of rows with invalid numeric entries (used to compute dataset severity).
- `row_severity` — dataset-level severity computed as `0.7 * invalid_ratio + 0.3 * mean(row_anomaly_score)`.

How to read the scores
----------------------
- `row_anomaly_score` thresholds (guideline):
	- >= 0.95: very likely an anomaly; inspect carefully.
	- 0.70–0.95: suspicious; investigate context and parsing.
	- 0.30–0.70: mild deviation; monitor or transform if needed.
	- < 0.30: typical / not anomalous.
- `row_severity`: closer to 1 indicates many problematic rows (either invalid numerics or many outlying values).

Suggested actions
-----------------
- For rows with `has_invalid_numeric` True: check parsing, encoding, and source types; fix parsing or impute values.
- For high `row_anomaly_score`: inspect the row contents — decide whether the value is a valid rare event or a data error. Consider winsorizing or removing erroneous rows.
- If `invalid_ratio` is high across the dataset, investigate ingestion and schema enforcement before modeling.

Caveats
-------
- These scores are numeric-focused; pure categorical anomalies may not be captured well.
- A high score does not always imply an error — it can represent legitimate rare events. Use domain knowledge.

Examples
--------
- A row with many NaNs after numeric coercion → `has_invalid_numeric = True` and high `row_anomaly_score`.
- A row with an extreme but valid measurement (e.g., an unusual large sale) → high score but may be kept.