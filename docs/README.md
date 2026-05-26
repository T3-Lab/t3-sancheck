# SanCheck Documentation

## Overview

`SanCheck (Sanity Check)` is a program that helps provide a statistical overview of data, including several things such as multicollinearity via VIF (Variance Inflation Factor), invalid value ratio, etc. The SanCheck project was created to address the inefficiency of repetitive preprocessing tasks in machine learning. The main objective of SanCheck is to provide a statistical overview of the data as it is without cleaning or outputting transformed input data.

## Documentation Structure

### Getting Started
- Quickstart: Contains information regarding general use of the program.
- CLI Reference: Contains information regarding the use of the program in depth.

### Interpretation Guides
- Anomalies: Interpretation of metrics related to anomalies in data such as infinite ​​or NaN values.
- Cleanliness: Interpretation of cleanliness metrics.
- Structures: Interpretation of metrics related to data structure such as sparsity.
- Distributions: Interpretation of metrics related to data distribution such as KS and Shapiro test score.
- Normality: Interpretation of metrics related to data normality such as skewness.

### Examples
- Clean Dataset: Provides an overview of program use on clean data.
- Noisy Dataset: Provides an overview of program use on noisy data.
- Multicollinearity: Provides an overview of program use on multicollinear data.

### Technical Notes
- Architecture: Provides information about structure of the SanCheck program.
- Limitations: Provides information about limitation of the SanCheck program.