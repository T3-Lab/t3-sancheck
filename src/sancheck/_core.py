from . import _helper as Help
from . import _check_func as Check
from . import __version__ as VERSION

import pandas as pd

# =============================
# Containers
# =============================
EXCEPTIONS = Help.Container("Exceptions", "Exceptions that occur during checks and analyses")
WARNINGS = Help.Container("Warnings", "Warnings that occur during checks and analyses")


# =============================
# Analysis
# =============================
def analyze(df: pd.DataFrame,
            categorical_cols: list[str],
            target: str,
            task: str,
            json_output: bool = False) -> dict:
    categorical_cols = categorical_cols if categorical_cols is not None else []

    no_target_idx = df.columns.difference([target]).tolist()

    if task == 'classification':
        override_rat = Check.class_override_ratio(df, no_target_idx, target)
        imbalance_rat = Check.class_imbalance_ratio(df[target])
    else:
        override_rat = None
        imbalance_rat = None

    rel_signal = Check.relation_signal(df, target, task) if task else None

    sim_pairs, sim_cols, sim_severity = Check.abnormal_similarity_report(df)
    nan_inf_df = Check.nan_inf_column_report(df)
    type_df = Check.inconsistent_type_report(df, thresh=0.05)

    non_cat_cols = df.columns.difference(categorical_cols)
    non_cat_df = df.drop(columns=categorical_cols, errors='ignore')

    struc_dist_df, overall_dist = Check.structure_distribution(non_cat_df)
    row_df, row_scores, row_severity = Check.problematic_row_report(df)
    dist_df = Check.distribution_breakdown(df, categorical_cols)
    cleanliness = Check.cleanliness_breakdown(nan_inf_df, type_df, sim_severity, row_severity)
    sparsity = Check.sparsity_ratio(df)
    vif = Check.compute_vif(df)

    shapiro = {}
    ks = {}
    for c in non_cat_cols:
        shapiro[c] = Check.shapiro_per_feature(df[c])
        ks[c] = Check.ks_per_feature(df[c])
    
    if not json_output:
        return {
            "similarity_report": {
                "pairs": sim_pairs,
                "affected_columns": sim_cols,
                "severity": sim_severity,
            },
            "nan_inf_report": nan_inf_df,
            "type_inconsistency_report": type_df,
            "problematic_rows_report": {
                "rows": row_df,
                "severity": row_severity,
                "scores": row_scores,
            },
            "distribution_report": dist_df.reset_index(),
            "cleanliness_breakdown": cleanliness,
            "sparsity_ratio": sparsity,
            "vif": vif,
            "rel_signal": rel_signal,
            "class_override_ratio": override_rat,
            "class_imbalance_ratio": imbalance_rat,
            "structure_dist": struc_dist_df,
            "overall_dist": overall_dist,
            "ks_scores": ks,
            "shapiro_scores": shapiro,
        }

    else:
        return {
            "metadata": {
                "version": VERSION,
                "task": task,
                "target": target,
                "num_rows": len(df),
                "num_cols": len(df.columns),
                "categorical_cols": categorical_cols,
                },
            "feature_similarity_report": {
                "pairs": sim_pairs.to_dict(orient="records"),
                "affected_columns": sim_cols,
                "severity": sim_severity,
            },
            "nan_inf_report": nan_inf_df.to_dict(orient="records"),
            "type_inconsistency_report": type_df.to_dict(orient="records"),
            "problematic_rows_report": {
                "rows": row_df.to_dict(orient="records"),
                "severity": row_severity,
                "scores": row_scores.to_dict(),
            },
            "distribution_report": dist_df,
            "cleanliness_breakdown": {
                "overall": cleanliness.overall,
                "label": Help._label_from_score(cleanliness.overall, no_color=True),
                "missing_severity": cleanliness.missing_severity,
                "type_severity": cleanliness.type_severity,
                "similarity_severity": cleanliness.similarity_severity,
                "row_severity": cleanliness.row_severity,
            },
            "sparsity_ratio": sparsity,
            "vif": {
                "mean": vif["mean"],
                "per_feature": vif["per_feature"],
            },
            "relation_signal": rel_signal,
            "class_override_ratio": override_rat,
            "class_imbalance_ratio": imbalance_rat,
            "structure_distribution": struc_dist_df.to_dict(orient='records'),
            "overall_distribution": overall_dist,
            "ks_scores": ks,
            "shapiro_scores": shapiro,
            "exceptions": EXCEPTIONS.data,
            "warnings": WARNINGS.data
        }