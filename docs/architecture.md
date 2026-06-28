# Architecture

## Project Philosophy
Tool that supports heuristic dataset analysis with optimized performance, providing easy-to-understand statistical analysis report interpretation.

## Analysis Pipeline
Numerical data is processed through a series of modular functions that generate analysis reports for each problem type. For illustration:

Incoming CSV data -> Target encoding process (if task and classification target are specified) and categorical columns -> Sorting data columns containing valid numeric values ​​-> Statistical analysis process (structure, distribution, correlation, etc.) -> Presenting report results in tables to the console or exporting reports with a JSON extension -> Plotting process (box plot, correlation heatmap) if the --no-plot flag is disabled.

## Data Flow
Incoming CSV data goes through a series of processes during analysis. For illustration:

Format change to DataFrame -> Encode categorical columns -> Sorting numeric columns -> Analysis process using statistical functions -> Organizing analysis results into reports -> Export phase via visualization, printing to the console, or JSON extension files

Data undergoes several transformations for analysis purposes that do not change the nature of the encoding and sorting of numeric columns.

## Metric Categories

### Distribution Analysis
Analysis of dataset characteristics in terms of distribution, including dispersion and entropy, to determine the nature of the numeric information contained in the data.

### Structural Analysis
Data structure analysis using statistical functions, including sparsity, class imbalance, and class override.

### Normality Analysis
Data normality analysis, from structure to distribution, includes KS and Shapiro scores, skewness and kurtosis, and distribution scores.

### Cleanliness Analysis
Data cleanliness analysis from a structural perspective, including data type inconsistencies, invalid values ​​such as NaN or inf, outlier rows, and abnormal column similarities.

## Visualization Pipeline
Visualization is performed after the main analysis results are exported. Supported visual plots include correlation heatmaps to identify feature correlations in the data and boxplots to assist in observing the distribution of data values. Chunking plots based on --plot-chunk use chunk slicing and looping in the main plotting function, which is helpful for high-dimensional data. Visualization is optional due to the various pipeline uses of SanCheck and the potential user desire to only observe statistics through numerical presentation.

## CLI Execution Flow
From the start, the user runs SanCheck with several arguments -> parses the arguments -> acts on the arguments with specific output expectations, such as --get-json and --metrics-info -> triggers data analysis and performs further analysis if specified. --target and --task -> triggers visualization if the --no-plot flag is disabled.

## Internal Module Structure

### __main__.py
CLI entrypoint for module-based execution.

### __init__.py
Contains package initiation, including metadata.

### _cli.py
Orchestration of modules and generation of data analysis reports, exporting them to the console or a JSON file.

### _core.py
The brain handles statistical analysis calculations and formatting and contains error containers.

### _check_func.py
A module containing the statistical calculation functions required for the analysis.

### _plotting.py
A dedicated module that manages plotting processes such as correlation heatmaps and boxplots.

### _helper.py
A module containing utilities that assist with the analysis process, such as labeling, container classes, etc.

### _info.py
A module containing information about SanCheck for interpretive purposes, such as when the --metrics-info argument is active.

### _reports.py
A Module containing a package of analysis report structures.

### _configs.py
Contains configuration settings for statistical calculations such as threshold, epsilon, and others.

## Final Design Decisions

### Why SanCheck prioritizes interpretability
Because SanCheck's goal is to facilitate rapid data inspection through heuristic and some normalized metrics.

### Why doesn't it replace EDA?
Because SanCheck's role is limited to performing brief checks or providing an overview of the statistical condition of the data without cleaning or making a final diagnosis.

### Why CLI instead of GUI
One reason is the inadequate skills of the stack maintainer, but a SanCheck demo in GUI format on Streamlit will be available soon at an unspecified time.

### Why 'lightweight'
SanCheck was originally created because the process of checking light statistics on datasets, such as entropy, class imbalance, etc., which are usually performed, was considered repetitive, and SanCheck allows for simple, one-line commands without burdening the user. This is why SanCheck was designed as a lightweight data characteristic checking tool.

### Why there's no automatic cleaning
SanCheck, as its name suggests, "Sanity `Check`", only checks data characteristics using statistical metrics. If SanCheck were to perform data cleaning, it would violate its purpose as a checking tool.