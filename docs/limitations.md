# Limitations

## Scope of the Tool

### Why this matters
To prevent misunderstandings about the extent and role of SanCheck in data analysis. SanCheck is designed to perform a quick and lightweight check on numeric-heavy CSV datasets, performed before EDA during the data sanity check phase. With normalized metrics and heuristics, SanCheck is intended for ML engineers, data analysts, data engineers, and others involved in data management.

### Common situations
Users may perceive SanCheck reports as a final diagnosis of data conditions, or misinterpret the presented metrics, leading to misleading observations of the data.

### Recommended interpretation
Use SanCheck as an overview of the statistical condition of the data and then take further action with an EDA pipeline or proper preprocessing.

### What SanCheck Does NOT Do

### Why this matters
To prevent misunderstandings about SanCheck's role in the statistical data analysis process. SanCheck is not intended to replace proper EDA or automated preprocessing, nor is it designed to improve data or provide a final diagnosis. SanCheck's role is limited to performing quick and simple checks using statistical metrics and providing an easy-to-understand interpretation of the data's condition.

### Common situations
Users use SanCheck as a benchmark for making final preprocessing decisions before model training or other needs, which can lead to misconceptions about SanCheck's role as a supporting analysis tool.

## Statistical Caveats

### Why this matters
To prevent misunderstandings about the interpretation of the presented metrics, the statistical metrics in SanCheck are heuristic, with some normalized interpretations, such as entropy and variance (spread), which can obscure some statistical insights from the data.

## Correlation and VIF Caveats
Correlation in data is crucial, especially for machine learning. SanCheck provides metrics such as VIF, MI, and f-score to aid in its observation of data. However, these metrics are also sensitive. For example, VIF can result in infinity if there are duplicated features; therefore, further observation of correlation is recommended.

## Small Dataset Limitations
In small datasets, some metrics, such as variance, normality, entropy, and the like, are relatively unstable, even biased anomaly rankings. Therefore, caution is recommended when interpreting metrics.

## Interpretation Warnings
Some potential misconceptions about common metrics are that high entropy indicates noise, high normality indicates a good dataset, poor anomaly scores mean bad data, and so on. It's important to remember that the metrics presented by SanCheck are contextual, so looking at a single metric alone cannot accurately determine the overall condition of the dataset.

## Visualization Constraints
SanCheck provides visualizations such as correlation heatmaps and boxplots to facilitate observation. However, conditions such as outlier-heavy data can distort plots like boxplots, and in high-dimensional data, the plots can be difficult to read.

## Performance Considerations
Although designed to be a lightweight tool, the computational cost of SanCheck's analysis can increase with increasing dimensions or sample sizes. This can lead to slower processing times due to the increased complexity of the metric calculations and the time-consuming visualization process.

## Recommended Usage Context
SanCheck is designed for quick and lightweight checks on numeric-heavy CSV datasets, performed before EDA, model training, data engineering, and other data sanity checks. This is important to avoid misunderstandings about how SanCheck assists data analysis.