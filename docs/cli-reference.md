# CLI Reference

## Basic Usage

```bash
sancheck data.csv
```

Run a quick statistical sanity check on a CSV dataset.

---

## Common Examples

### Basic inspection
```bash
sancheck data.csv
```

### Analyze with specified target and task
```bash
sancheck data.csv --target target_col --task classification
```

### JSON Export
```bash
sancheck data.csv --get-json
```

## Arguments

### Positional Arguments

#### csv
Expect input DataFrame. Path to CSV dataset file.

### Optional Arguments

#### --target
Expect str. Specifies the target column used for supervised analysis. Enables target-based metrics and reports.

#### --cat-encode
Expect comma-separated list. Encode columns into categorical number representation and consider them as categorical columns.

#### --exclude
Expect comma-seperated list. Exclude selected columns from analysis

#### --plot-chunk
Expect Int or 'all'. Split plot generation into smaller column groups. Useful for wide datasets with many numeric features.

#### --download-plot
No input required. Download plots as PNG files.

#### --no-plot
No input required. Skip plotting (overrides --download-plot).

#### --metrics-info
No input required. Show detailed explanation of SanCheck analysis metrics.

#### --get-json
No input required. Output the report as JSON file instead of printing to console.

#### --mute
No input required. Mute safeguards and automatically fallback to the safest option.

## Output Modes

### Console output
Print the analysis result to the console. The analysis results are mapped with reports per data element such as column report, row report, distribution report, normality report, etc.

### JSON output
Export the analysis result as a JSON file with the strcuture as below:

```json
╭── metadata
│   ├── version
│   ├── task
│   ├── target
│   ├── num_rows
│   ├── num_cols
│   └── categorical_cols
├── feature_similarity_report
│   ├── pairs
│   ├── affected_columns
│   └── severity
├── nan_inf_report
│   └── [0]
│       ├── column
│       ├── total
│       ├── non_null
│       ├── nan_total
│       ├── inf_total
│       ├── bad_parse_total
│       ├── invalid_total
│       └── invalid_ratio
├── type_inconsistency_report
│   └── [0]
|       ├── total
│       ├── column
│       ├── bad_type_total
│       ├── bad_type_ratio
│       └── flagged
├── problematic_rows_report
│   ├── rows
│   │   └── [0]
│   │       ├── row_index
│   │       ├── has_invalid_numeric
│   │       └── row_anomaly_score
│   ├── severity
│   └── scores
│       └── "<index>"
├── distribution_report
│   └── [0]
│       ├── column
│       ├── entropy
│       ├── entropy_label
│       ├── spread_score
│       ├── spread_label
│       ├── variance
│       └── iqr
├── cleanliness_breakdown
│   ├── overall
│   ├── label
│   ├── missing_severity
│   ├── type_severity
│   ├── similarity_severity
│   └── row_severity
├── sparsity_ratio
├── vif
│   ├── mean
│   └── per_feature
│       └── "<feature>"
├── relation_signal
|   └── [0]
│       ├── feature
│       ├── mi
│       └── f
├── class_override_ratio
├── class_imbalance_ratio
├── structure_normality
├── ks_scores
│   └── "<feature>"
├── shapiro_scores
│   └── "<feature>"
├── exceptions
└── warnings
```

## Error Behavior

### Invalid Dataset Path
Occurs when the dataset path is invalid or inaccessible.

### Empty Dataset
Occurs when receives an empty DataFrame as input data to be analyzed.

### Non-Numeric Data
Occurs when receives a DataFrame without any valid numeric columns.

### Runtime Warnings
Some warnings can appear due to several things, such as numerical calculation errors, internal system errors, or other issues related to the data analysis process.