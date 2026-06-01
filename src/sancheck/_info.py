from rich import print
from rich.table import Table, box
from rich.console import Group
from rich.panel import Panel

def metrics():
    cleanliness_tab = Table(title="Cleanliness metrics", header_style="green", box=box.ROUNDED)
    cleanliness_tab.add_column("Metric")
    cleanliness_tab.add_column("Info")
    
    cleanliness_tab.add_row("Cleanliness score", 
                            "Taken from the weighted accumulation of the invalid value ratio (0.30), inconsistent column type (0.20), abnormal column similarity (0.20), and row problem severity (0.30).")
    cleanliness_tab.add_row("Invalid value ratio", 
                            "The proportion of invalid values (NaN, inf) to total values in the data.")
    cleanliness_tab.add_row("Feature similarity", 
                            "The similarity of two feature pairs through their correlation, optimized using the upper triangle operation.")
    cleanliness_tab.add_row("Inconsistent type column",
                            "Feature columns with inconsistent data types, such as rows 1-10 being floats but row 11 being strings. Inconsistent data, such as strings of letters, are converted to NA and then the ratio of their number to the total number of values in the column is calculated.")
    cleanliness_tab.add_row("Row problem severity", 
                            "A score of the severity of a row's problems based on the ratio of invalid values (finite values) and outliers (using the robust z-score with MAD).")

    dist_tab = Table(title="Distribution metrics", header_style="green", box=box.ROUNDED)
    dist_tab.add_column("Metric")
    dist_tab.add_column("Info")

    dist_tab.add_row("Entropy", 
                     "The irregularity of a feature. The mean calculation results are presented normalized using 'H / max(H_max, ε)', and with H_max 'log2(len(hist))' or 1.0 if len(hist) < 1. Other forms of presentation are the top 5 highest or the mean entropy of all features.")
    dist_tab.add_row("Variance (spread)", 
                     "How spread out the data values are. The mean calculation results are presented normalized using 'var / (var + baseline + ε)', and with baseline '(IQR / σ)^2' (σ = 1.349) or STD^2 features if IQR < 0. Other forms of presentation are the top 5 highest or the mean var of all features.")
    
    normality_tab = Table(title="Normality metrics", header_style="green", box=box.ROUNDED)
    normality_tab.add_column("Metric")
    normality_tab.add_column("Info")

    normality_tab.add_row("Shapiro-Wilk and Kolmogorov-Smirnov score", 
                          "Results of tests of normality of distribution from raw p-values.")
    normality_tab.add_row("Distribution score", 
                          "Based on kurtosis and skewness using '1 - (0.5 * skew_score + 0.5 * kurt_score)' with skew_score = np.tanh(skew_mean / 2) and kurt_score = np.tanh(kurt_mean / 5). The mean is taken from the kurtosis or skewness scores of all features.")

    struc_n_rel_tab = Table(title="Structure and relation metrics", header_style="green", box=box.ROUNDED)
    struc_n_rel_tab.add_column("Metric")
    struc_n_rel_tab.add_column("Info")

    struc_n_rel_tab.add_row("Sparsity", 
                            "The proportion of zero-value (0) data points to the total data set. This is calculated by taking into account the data size as a penalty of '0.7 * sparsity_ratio + 0.3 * dim_penalty'. The penalty is calculated as 'n_feature / (n_feature + n_sample)'.")
    struc_n_rel_tab.add_row("Class override ratio", 
                            "The proportion of data points with the exact same feature but different classes in the dataset.")
    struc_n_rel_tab.add_row("Class imbalance", 
                            "The degree of imbalance in the classes, calculated using the normalized 'Gini' criterion formula 'gini / (1 - 1 / n_class)'.")

    struc_n_rel_tab.add_section()

    struc_n_rel_tab.add_row("Multicollinearity", 
                            "Multicollinearity is calculated using the VIF (Variance Inflation Factor). The calculated mean is presented normalized using 'tanh(mean_VIF / 10)'. Another form of presentation is the top 5 highest of all features.")

    info_report = Group(
        cleanliness_tab,
        dist_tab,
        normality_tab, 
        struc_n_rel_tab,
    )

    print(Panel(info_report, title="[bold]Metrics Info[/]", expand=False))