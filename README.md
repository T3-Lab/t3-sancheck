[![PyPI version](https://badge.fury.io/py/sancheck.svg)](https://pypi.org/project/sancheck/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/sancheck/blob/main/LICENSE)
![JSON Output](https://img.shields.io/badge/output-JSON-orange)
![Statistical Diagnostics](https://img.shields.io/badge/focus-statistics-purple)
![CLI Tool](https://img.shields.io/badge/interface-CLI-black)
![Docs](https://img.shields.io/badge/docs-available-blue)

# SanCheck — Sanity Check

SanCheck is a minimal-tuning CLI tool for quickly assessing the statistical overview of CSV datasets. It provides a fast, high-level overview before deeper analysis or modeling.

## When should I use it?
- Before exploratory data analysis (EDA)
- Before training statistical or machine learning models
- When you want a quick sanity check without manual inspection 

## What it does NOT do
- It does not clean or modify data
- It does not model relationships
- It does not replace proper EDA or data validation pipelines

## Quick start
Run the tool on a CSV file:

```bash
sancheck [csv_path]
```

## Example output with tests/fixtures/noisy.csv

### 💬 Terminal output

```bash
Done! 
⚠️  Without task and target specification some metrics are disabled 

            Dataset Summary            
╭─────────────────────────────┬───────╮
│ Info                        │ Value │
├─────────────────────────────┼───────┤
│ Valid numeric columns       │     2 │
│ Ignored non-numeric columns │     3 │
╰─────────────────────────────┴───────╯
╭────────────────────── Column Report ──────────────────────╮
│                      Invalid Values                       │
│ ╭────────────────────┬────────┬─────────────────────────╮ │
│ │ Issue              │ Column │ Details                 │ │
│ ├────────────────────┼────────┼─────────────────────────┤ │
│ │ NaN/Inf            │ absent │ invalid  = 0/10 (0.000) │ │
│ │ NaN/Inf            │ salary │ invalid  = 0/10 (0.000) │ │
│ │ Type inconsistency │ absent │ bad_type = 0/10 (0.000) │ │
│ │ Type inconsistency │ salary │ bad_type = 0/10 (0.000) │ │
│ ╰────────────────────┴────────┴─────────────────────────╯ │
│ NaN/Inf columns: 0                                        │
│ Type inconsistent columns: 0                              │
│ Column Similarity                                         │
│       Pairs                                               │
│ ╭──────┬────────╮                                         │
│ │ Pair │ |corr| │                                         │
│ ├──────┼────────┤                                         │
│ │ -    │      - │                                         │
│ ╰──────┴────────╯                                         │
│ Affected columns: -                                       │
│ Severity: 0.000                                           │
╰───────────────────────────────────────────────────────────╯
╭────────────── Row report ───────────────╮
│          Top 5 anomalous rows           │
│ ╭───────────┬───────────────┬─────────╮ │
│ │ Row index │ Anomaly score │ Invalid │ │
│ ├───────────┼───────────────┼─────────┤ │
│ │   row 5   │         0.916 │  False  │ │
│ │   row 4   │         0.897 │  False  │ │
│ │   row 9   │         0.865 │  False  │ │
│ │   row 6   │         0.778 │  False  │ │
│ │   row 3   │         0.448 │  False  │ │
│ ╰───────────┴───────────────┴─────────╯ │
│ Problematic rows: 0 / 10                │
│ Row severity: 0.135 / 1.000             │
╰─────────────────────────────────────────╯
╭────────────────────────────── Distribution Report ──────────────────────────────╮
│                                Top 2 Spread                                     │
│ ╭────────┬───────────────┬────────────────────────┬────────────┬─────────╮      │
│ │ Column │        Spread │         Label          │        Var │     IQR │      │
│ ├────────┼───────────────┼────────────────────────┼────────────┼─────────┤      │
│ │ absent │ 0.671 / 1.000 │ wide / large variation │      1.122 │   1.000 │      │
│ │ salary │ 0.613 / 1.000 │ wide / large variation │ 387271.111 │ 667.500 │      │
│ ╰────────┴───────────────┴────────────────────────┴────────────┴─────────╯      │
│                                  Top 2 Entropy                                  │
│ ╭────────┬───────────────┬────────────────────────────────────────────────────╮ │
│ │ Column │       Entropy │                       Label                        │ │
│ ├────────┼───────────────┼────────────────────────────────────────────────────┤ │
│ │ absent │ 0.865 / 1.000 │ very spread / more uniform or complex distribution │ │
│ │ salary │ 0.785 / 1.000 │ very spread / more uniform or complex distribution │ │
│ ╰────────┴───────────────┴────────────────────────────────────────────────────╯ │
│ Avg entropy: 0.825                                                              │
│ Avg spread score: 0.642                                                         │
╰─────────────────────────────────────────────────────────────────────────────────╯
╭───────────────────── Normality Report ─────────────────────╮
│    Distribution Normality                                  │
│ ╭─────────┬─────────┬───────╮                              │
│ │ Feature │ Shapiro │    KS │                              │
│ ├─────────┼─────────┼───────┤                              │
│ │ absent  │   0.002 │ 0.120 │                              │
│ │ salary  │   0.071 │ 0.219 │                              │
│ ╰─────────┴─────────┴───────╯                              │
│                 Structure Distribution                     │
│ ╭─────────┬──────────┬──────────┬────────────────────╮     │
│ │ Feature │ Skewness │ Kurtosis │ Distribution score │     │
│ ├─────────┼──────────┼──────────┼────────────────────┤     │
│ │ absent  │    1.218 │    0.166 │              0.646 │     │
│ │ salary  │    1.042 │    0.052 │              0.735 │     │
│ ╰─────────┴──────────┴──────────┴────────────────────╯     │
│ Overall structure distribution score: 0.733 / 1.000 (high) │
╰────────────────────────────────────────────────────────────╯
╭───── Structure & Relation Report ─────╮
│               Structure               │
│ ╭──────────┬────────────────────────╮ │
│ │ Metric   │                  Value │ │
│ ├──────────┼────────────────────────┤ │
│ │ Sparsity │ 0.260 / 1.000 (medium) │ │
│ ╰──────────┴────────────────────────╯ │
│              Relation                 │
│ ╭─────────┬───────┬────┬─────────╮    │
│ │ Feature │   VIF │ MI │ F-score │    │
│ ├─────────┼───────┼────┼─────────┤    │
│ │ absent  │ 1.346 │  - │       - │    │
│ │ salary  │ 1.346 │  - │       - │    │
│ ╰─────────┴───────┴────┴─────────╯    │
│ Avg VIF: 0.134 / 1.000 (low)          │
╰───────────────────────────────────────╯
                 Cleanliness Status                 
╭─────────────────────┬────────────────────────────╮
│ Metric              │ Value                      │
├─────────────────────┼────────────────────────────┤
│ Cleanliness score   │ 0.959 / 1.000 (very clean) │
│ Missing severity    │ 0.000 / 1.000 (low)        │
│ Type severity       │ 0.000 / 1.000 (low)        │
│ Similarity severity │ 0.000 / 1.000 (low)        │
│ Row severity        │ 0.135 / 1.000 (low)        │
╰─────────────────────┴────────────────────────────╯
                                               Actions Suggestion                                               
╭──────┬───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Type │ Action                                                                                                │
├──────┼───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Row  │ Moderate anomaly detected in row 5. Check for any potential outlier or data quality issue in the row. │
│ Row  │ Moderate anomaly detected in row 4. Check for any potential outlier or data quality issue in the row. │
│ Row  │ Moderate anomaly detected in row 9. Check for any potential outlier or data quality issue in the row. │
│ Row  │ Moderate anomaly detected in row 6. Check for any potential outlier or data quality issue in the row. │
╰──────┴───────────────────────────────────────────────────────────────────────────────────────────────────────╯
⏱️ Elapsed time: 0.31 seconds
```

### 📊 Boxplot visualization
![Boxplot Example](assets/noisy_data_plots/boxplot_numeric_columns(all_features).png)

### 🔥 Heatmap visualization
![Heatmap Example](assets/noisy_data_plots/heatmap_correlation(all_features).png)


## Interpretation tips
- Higher cleanliness scores indicate cleaner numeric data

- Anomalous rows are ranked, not classified — use them for inspection

- Non-numeric columns are ignored by design

- This tool is best used as a fast pre-analysis step

- Certain metrics such as VIF may produce infinite values under near-perfect multicollinearity.