# Limitations

## Scope of the Tool
As outlined in the "Final Design Decisions" section of [architecture.md](./architecture.md), SanCheck aims to provide reports on dataset statistical analysis—based on heuristic metrics—and present the results in an easily understandable format. However, SanCheck is not intended to replace proper Exploratory Data Analysis (EDA) or serve as the primary benchmark for determining dataset quality.

### Why this matters
Understanding the conceptual or capability limits of a system is crucial for shaping one's perspective on a project—in this case, SanCheck. Knowing the extent to which a project addresses conceptual gaps or meets functional requirements enables more informed conclusions regarding its objectives, targets, appropriate use cases, and so forth.

## Known Tradeoffs

### Analysis depth
SanCheck performs lightweight data analysis, which is useful when users want a quick analysis of their dataset. However, this also prevents the analysis from directly drawing conclusions about the data's characteristics. The metrics in the report do not comprehensively describe the data's characteristics, providing an overview of the data's condition.

### Small dataset instability
In small datasets, some metrics and analysis results can be unstable because certain thresholds, such as the threshold for valid numeric columns, are fixed.

### Limited contextual understanding
SanCheck is limited in the context of the metrics provided, potentially omitting some insights about the data.

### Numerical stability
Although SanCheck's numerical stability is maintained, it is possible for unusual values ​​to appear in reports, such as the common case of a VIF value of infinity, which can be caused by feature duplication or abnormal correlation between features.

### Lack of automation
SanCheck is designed not to assume anything from the user about the data, such as categorical feature detection; the --cat-encode argument indicates that SanCheck was originally designed not to automate data based on assumptions about the user's data. However, because of this, SanCheck can be difficult to use if a dataset contains many categorical columns, as the user must enter the column names one by one into the --cat-encode argument to ensure SanCheck truly recognizes the columns as categorical.

## Statistical Caveats

### Correlation and VIF caveats
Correlation in data is crucial, especially for machine learning. SanCheck provides metrics such as VIF, MI, and f-score to aid in its observation of data. However, these metrics are also sensitive. For example, VIF can result in infinity if there are duplicated features; therefore, further observation of correlation is recommended.

### Small dataset limitations
In small datasets, some metrics, such as variance, normality, entropy, and the like, are relatively unstable, even biased anomaly rankings. Therefore, caution is recommended when interpreting metrics.

### Interpretation warnings
Some potential misconceptions about common metrics are that high entropy indicates noise, high normality indicates a good dataset, poor anomaly scores mean bad data, and so on. It's important to remember that the metrics presented by SanCheck are contextual, so looking at a single metric alone cannot accurately determine the overall condition of the dataset.

### Visualization constraints
SanCheck provides visualizations such as correlation heatmaps and boxplots to facilitate observation. However, conditions such as outlier-heavy data can distort plots like boxplots, and in high-dimensional data, the plots can be difficult to read.

### Performance considerations
Although designed to be a lightweight tool, the computational cost of SanCheck's analysis can increase with increasing dimensions or sample sizes. This can lead to slower processing times due to the increased complexity of the metric calculations and the time-consuming visualization process.

### Recommended usage context
SanCheck is designed for quick and lightweight checks on numeric-heavy CSV datasets, performed before EDA, model training, data engineering, and other data sanity checks. This is important to avoid misunderstandings about how SanCheck assists data analysis.
