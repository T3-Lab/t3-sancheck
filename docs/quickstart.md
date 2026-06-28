# Quickstart

## Installation
```bash
pip install sancheck
```

## Basic Usage
```bash
sancheck data.csv
```

## Positional Arguments
- csv: Path to CSV data.

## Example Command
```bash
sancheck tests/fixtures/clean.csv
```

## Understanding the Output

### Terminal output
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
╭────────────────────────── Column Report ───────────────────────────╮
│                           Invalid Values                           │
│ ╭────────────────────┬─────────────────┬─────────────────────────╮ │
│ │ Issue              │ Column          │ Details                 │ │
│ ├────────────────────┼─────────────────┼─────────────────────────┤ │
│ │ NaN/Inf            │ score           │ invalid  = 0/10 (0.000) │ │
│ │ NaN/Inf            │ get_scholarship │ invalid  = 0/10 (0.000) │ │
│ │ Type inconsistency │ score           │ bad_type = 0/10 (0.000) │ │
│ │ Type inconsistency │ get_scholarship │ bad_type = 0/10 (0.000) │ │
│ ╰────────────────────┴─────────────────┴─────────────────────────╯ │
│ NaN/Inf columns: 0                                                 │
│ Type inconsistent columns: 0                                       │
│ Column Similarity                                                  │
│       Pairs                                                        │
│ ╭──────┬────────╮                                                  │
│ │ Pair │ |corr| │                                                  │
│ ├──────┼────────┤                                                  │
│ │ -    │      - │                                                  │
│ ╰──────┴────────╯                                                  │
│ Affected columns: -                                                │
│ Severity: 0.000                                                    │
╰────────────────────────────────────────────────────────────────────╯
╭────────────── Row report ───────────────╮
│          Top 5 anomalous rows           │
│ ╭───────────┬───────────────┬─────────╮ │
│ │ Row index │ Anomaly score │ Invalid │ │
│ ├───────────┼───────────────┼─────────┤ │
│ │   row 2   │         0.825 │  False  │ │
│ │   row 8   │         0.796 │  False  │ │
│ │   row 3   │         0.380 │  False  │ │
│ │   row 9   │         0.347 │  False  │ │
│ │   row 4   │         0.262 │  False  │ │
│ ╰───────────┴───────────────┴─────────╯ │
│ Problematic rows: 0 / 10                │
│ Row severity: 0.100 / 1.000             │
╰─────────────────────────────────────────╯
╭────────────────────────────────── Distribution Report ───────────────────────────────────╮
│                                      Top 2 Spread                                        │
│ ╭─────────────────┬───────────────┬───────────────────────────────┬─────────┬────────╮   │
│ │ Column          │        Spread │             Label             │     Var │    IQR │   │
│ ├─────────────────┼───────────────┼───────────────────────────────┼─────────┼────────┤   │
│ │ score           │ 0.626 / 1.000 │    wide / large variation     │ 529.789 │ 24.000 │   │
│ │ get_scholarship │ 0.500 / 1.000 │ moderate / moderate variation │   0.178 │  0.000 │   │
│ ╰─────────────────┴───────────────┴───────────────────────────────┴─────────┴────────╯   │
│                                      Top 2 Entropy                                       │
│ ╭─────────────────┬───────────────┬────────────────────────────────────────────────────╮ │
│ │ Column          │       Entropy │                       Label                        │ │
│ ├─────────────────┼───────────────┼────────────────────────────────────────────────────┤ │
│ │ score           │ 0.985 / 1.000 │ very spread / more uniform or complex distribution │ │
│ │ get_scholarship │ 0.000 / 1.000 │ very concentrated / single value or dominant mode  │ │
│ ╰─────────────────┴───────────────┴────────────────────────────────────────────────────╯ │
│ Avg entropy: 0.493                                                                       │
│ Avg spread score: 0.563                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────── Normality Report ───────────────────────╮
│        Distribution Normality                                  │
│ ╭─────────────────┬─────────┬───────╮                          │
│ │ Feature         │ Shapiro │    KS │                          │
│ ├─────────────────┼─────────┼───────┤                          │
│ │ score           │   0.814 │ 0.971 │                          │
│ │ get_scholarship │   0.000 │ 0.009 │                          │
│ ╰─────────────────┴─────────┴───────╯                          │
│                     Structure Distribution                     │
│ ╭─────────────────┬──────────┬──────────┬────────────────────╮ │
│ │ Feature         │ Skewness │ Kurtosis │ Distribution score │ │
│ ├─────────────────┼──────────┼──────────┼────────────────────┤ │
│ │ score           │    0.452 │    0.734 │              0.576 │ │
│ │ get_scholarship │    1.500 │    0.250 │              0.560 │ │
│ ╰─────────────────┴──────────┴──────────┴────────────────────╯ │
│ Overall structure distribution score: 0.725 / 1.000 (high)     │
╰────────────────────────────────────────────────────────────────╯
╭─────── Structure & Relation Report ────────╮
│               Structure                    │
│ ╭──────────┬────────────────────────╮      │
│ │ Metric   │                  Value │      │
│ ├──────────┼────────────────────────┤      │
│ │ Sparsity │ 0.330 / 1.000 (medium) │      │
│ ╰──────────┴────────────────────────╯      │
│                  Relation                  │
│ ╭─────────────────┬───────┬────┬─────────╮ │
│ │ Feature         │   VIF │ MI │ F-score │ │
│ ├─────────────────┼───────┼────┼─────────┤ │
│ │ score           │ 1.590 │  - │       - │ │
│ │ get_scholarship │ 1.590 │  - │       - │ │
│ ╰─────────────────┴───────┴────┴─────────╯ │
│ Avg VIF: 0.158 / 1.000 (low)               │
╰────────────────────────────────────────────╯
                 Cleanliness Status                 
╭─────────────────────┬────────────────────────────╮
│ Metric              │ Value                      │
├─────────────────────┼────────────────────────────┤
│ Cleanliness score   │ 0.970 / 1.000 (very clean) │
│ Missing severity    │ 0.000 / 1.000 (low)        │
│ Type severity       │ 0.000 / 1.000 (low)        │
│ Similarity severity │ 0.000 / 1.000 (low)        │
│ Row severity        │ 0.100 / 1.000 (low)        │
╰─────────────────────┴────────────────────────────╯
                                               Actions Suggestion                                               
╭──────┬───────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ Type │ Action                                                                                                │
├──────┼───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Row  │ Moderate anomaly detected in row 2. Check for any potential outlier or data quality issue in the row. │
│ Row  │ Moderate anomaly detected in row 8. Check for any potential outlier or data quality issue in the row. │
╰──────┴───────────────────────────────────────────────────────────────────────────────────────────────────────╯
⏱️ Elapsed time: 0.43 seconds
```

The warning at the beginning of the output is a warning caused because --task and --target are not specified as such

```bash
... --target col_target_name --task regression / classification
```

Per-report output explanation:

- Data Summary: Contains information regarding data management (only numeric columns are processed) and task type (if any)

- Column Report: Contains information regarding column problems in the data.

- Row Report: Contains information regarding row problems in the data.

- Distribution Report: Presents information about data distribution which includes spread (var) and entropy.

- Normality Report: Contains information regarding the normality of data in terms of distribution and structure.

- Structure & Relation Report: Contains information about relationships such as feature <-> target or feature_a <-> feature_b, and data structures such as sparsity.

- Cleanliness Status: Contains information regarding 'data cleanliness' from invalid values ​​such as inf or NaN, noise or outliers, and inconsistent value types.

- Actions Suggestion: Contains suggestions for managing problems in the data.

### Box plot visualization
![Boxplot Example](../assets/clean_data_plots/boxplot_numeric_columns(all_features).png)

### Correlation heatmap
![Boxplot Example](../assets/clean_data_plots/heatmap_correlation(all_features).png)

## Common Workflow

### 1. Prepare the dataset
Prepare a dataset with 2 or more columns where most of the values ​​are numeric values.

### 2. Run SanCheck
Run SanCheck CLI with:

```bash
sancheck your_data.csv
```

for quick inspection.

But not only that, we can make SanCheck carry out deeper analysis by specifying targets and tasks, for example:

```bash
sancheck your_data.csv --target col_target --task classification
```

That way, SanCheck will provide deeper analysis results about the dataset provided.
If we want the output in JSON, we can make SanCheck provide output in that format with the command:

```bash
sancheck your_data.csv --target col_target --task classification --get-json
```

That way, SanCheck will provide output in the form of a JSON file of analysis results without printing the analysis results to the console.

### 3. Review structural warnings
Pay attention to column and row reports for features or samples that have a lot of invalid values ​​in them, some rows can be flagged 'invalid' if there are too many invalid values.

It can be seen in the console output example above that the column and row reports indicate that the data is quite clean, although some rows have high anomaly scores, but this does not mean they are labeled invalid.

### 4. Inspect distributions and anomalies
Then pay attention to the distribution and normality reports of the data to find out the characteristics.

In the console output example above, the 'score' feature has a fairly high distribution ratio followed by high entropy, indicating high variation in values ​​as well as high normality scores (KS and Shapiro), indicating a normal distribution form in the data; Inversely proportional to 'get_scholarship' with a low distribution ratio followed by low entropy, indicating low variation in values ​​caused by the binary value of this feature as well as low structural normality indicating a distribution shape that is far from a normal distribution.

It can also be noted in the normality report that the overall dataset structure normality score is quite high.

### 5. Continue to deeper analysis
SanCheck does not replace proper EDA, so it is recommended to continue the data engineering process with more in-depth checks.

## Next Steps
- Read the interpretation guides: [interpretaions/](./interpretations/)
- Review CLI options: [cli-reference.md](./cli-reference.md)
- Understand known limitations: [limitations.md](./limitations.md)
- Learn about the internal architecture: [architecture.md](./architecture.md)