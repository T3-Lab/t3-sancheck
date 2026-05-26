# Normality Interpretation

Purpose
-------
Explain tests and shape metrics used to assess how close feature distributions are to normal: Shapiro-Wilk, KS test, skewness, kurtosis, and a combined structure score.

Metrics
-------
- `shapiro_p` (Shapiro-Wilk p-value): p > 0.05 generally means you cannot reject normality; p <= 0.05 suggests non-normality. For n > 5000 the implementation uses a 5000-sample.
- `ks_p` (Kolmogorov–Smirnov p-value): tests sample against a normal distribution with empirical mean/std. If std <= eps the function returns 1.0.
- `skew` and `kurtosis`: measures of asymmetry and tail/heaviness; absolute values used in structure scoring.
- `dist_score`: combined per-feature score in [0,1] where values closer to 1 indicate shapes nearer to normal.

How to use these metrics
------------------------
- Use p-values as indicators, not absolute proof. Large samples can make small deviations statistically significant.
- Visual checks (histograms, QQ-plots) are recommended to complement tests.

If non-normality matters
-----------------------
- Apply transformations (log, Box-Cox, Yeo-Johnson) to reduce skew.
- Use robust estimators or non-parametric methods when normality assumptions are violated.

Caveats
-------
- Small samples (n < 3) are not testable; the code returns 0 for Shapiro in those cases.
- Outliers can strongly influence tests; treat them before testing where appropriate.