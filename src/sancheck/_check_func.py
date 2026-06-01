from . import _helper as Help
from . import _configs as Config
from . import _core
from . import _reports as Reports

from rich.console import Console
import pandas as pd
import numpy as np
import math
from scipy import stats

from scipy.stats import skew, kurtosis
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.feature_selection import f_classif, f_regression, mutual_info_classif, mutual_info_regression

import warnings

# =============================
# Distribution analysis
# =============================
def normalized_entropy(series: pd.Series, eps: float, is_cat: bool, bins):
    vals = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna().to_numpy()
    if len(vals) < 2:
        return 0.0

    if np.all(vals == vals[0]):
        return 0.0

    try:
        if is_cat:
            probs = pd.Series(vals).value_counts(normalize=True).values
            H = -(probs * np.log2(probs)).sum()
            H_max = np.log2(len(probs)) if len(probs) > 1 else 1.0
            return float(np.clip(H / max(H_max, eps), 0.0, 1.0))

        hist, edges = np.histogram(vals, bins=bins)

    except Exception as e:
        _core.EXCEPTIONS.store({
                "type": type(e).__name__,
                "message": str(e),
                "where": "normalized_entropy computation",
            })

        hist, edges = np.histogram(vals, bins=min(10, max(2, int(np.sqrt(len(vals))))))

    total = hist.sum()
    if total <= 0:
        return 0.0

    probs = hist / total
    probs = probs[probs > 0]
    if len(probs) <= 1:
        return 0.0

    H = -(probs * np.log2(probs)).sum()
    H_max = math.log2(len(hist)) if len(hist) > 1 else 1.0
    return float(np.clip(H / max(H_max, eps), 0.0, 1.0))


def normalized_spread_score(series: pd.Series, eps: float):
    vals = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna().to_numpy(dtype=float)
    if len(vals) < 2:
        return 0.0, 0.0, 0.0

    var = float(np.var(vals, ddof=1)) if len(vals) > 1 else 0.0
    q75, q25 = np.percentile(vals, [75, 25])
    iqr = float(q75 - q25)
    robust_sigma = iqr / 1.349 if iqr > 0 else float(np.std(vals, ddof=1))
    baseline = robust_sigma ** 2

    score = var / (var + baseline + eps)
    score = float(np.clip(score, 0.0, 1.0))
    return score, var, iqr


def distribution_report(df: pd.DataFrame,
                        cat_col: list[str],
                        eps: float=Config.EPS,
                        bins=Config.ENTROPY_BINS):
    rows = []
    cat_col = np.asarray(cat_col)
    for c in df.columns:
        is_cat = np.any(c == cat_col)
        ent = normalized_entropy(df[c], eps, is_cat, bins)
        spread_score, raw_var, iqr = normalized_spread_score(df[c], eps)
        rows.append({
            "column": c,
            "entropy": ent,
            "entropy_label": Help.entropy_interpretation(ent),
            "spread_score": spread_score,
            "spread_label": Help.spread_interpretation(spread_score),
            "variance": raw_var,
            "iqr": iqr,
        })
    return pd.DataFrame(rows)

def class_override_ratio(df: pd.DataFrame, no_target_idx: list[str], target: str):
    grouped = df.groupby(no_target_idx)[target].nunique()

    conflict = (grouped > 1).sum()
    total = len(grouped)

    if total == 0:
        return 0.0

    return conflict / total

def class_imbalance_ratio(target: pd.Series):
    unique_classes = target.dropna().unique()
    if len(unique_classes) <= 1:
        return 0.0
    
    if len(unique_classes) > 50:
        _core.WARNINGS.store({
            "type": "UserWarning",
            "message": f"Too many unique classes in target ({len(unique_classes)}), imbalance ratio may be less meaningful.",
            "where": "class_imbalance_ratio computation"
        })
        status = "n"
        if not Config.MUTE:
            status = input(f"⚠️ Too many unique classes in target ({len(unique_classes)}), imbalance ratio may be less meaningful.\nContinue with imbalance ratio calculation? (y/n): ").strip().lower()
        if status == 'n':
            return 0.0

        elif status == 'y':
            print("Continuing with imbalance ratio calculation...")
        
        else:
            print("Invalid input, skipping imbalance ratio calculation.")
            return 0.0

    max_label = target.max() if len(target) > 0 else 0
    counts = np.bincount(target, minlength=max_label + 1)
    probs = counts / len(target)
    gini = 1.0 - np.sum(probs ** 2)
    balance_rat = gini / (1 - 1 / len(unique_classes))
    
    return 1.0 - balance_rat

# =============================
# Column problems
# =============================
def nan_inf_column_report(df: pd.DataFrame):
    rows = []
    for c in df.columns:
        s = df[c]
        coerced, finite_mask, nan_mask, bad_parse_mask = Help._to_numeric_with_mask(s)

        total = len(s)
        non_null = int(s.notna().sum())
        invalid_total = int((~finite_mask).sum())  # nan + inf setelah coercion
        inf_total = int(np.isinf(coerced.to_numpy(dtype="float64", copy=False)).sum()) if non_null else 0
        nan_total = int(coerced.isna().sum())
        bad_parse_total = int(bad_parse_mask.sum())

        severity = invalid_total / max(total, 1)

        rows.append({
            "column": c,
            "total": total,
            "non_null": non_null,
            "nan_total": nan_total,
            "inf_total": inf_total,
            "bad_parse_total": bad_parse_total,
            "invalid_total": invalid_total,
            "invalid_ratio": float(severity),
        })
    return pd.DataFrame(rows)


def inconsistent_type_report(df: pd.DataFrame,
                             thresh: float=0.05):
    rows = []
    for c in df.columns:
        s = df[c]
        coerced = pd.to_numeric(s, errors="coerce")
        bad = coerced.isna() & s.notna()
        ratio = float(bad.mean())
        rows.append({
            "total": len(s),
            "column": c,
            "bad_type_total": int(bad.sum()),
            "bad_type_ratio": ratio,
            "flagged": ratio > thresh,
        })
    return pd.DataFrame(rows)


def abnormal_similarity_report(df: pd.DataFrame,
                               threshold: float=Config.DEFAULT_SIM_THRESHOLD):
    if len(df.columns) < 2:
        return pd.DataFrame(), [], 0.0

    corr = df.corr().abs()
    mask = np.triu(np.ones_like(corr, dtype=bool), k=1)
    pairs_df = corr.where(mask).stack().reset_index()
    pairs_df.columns = ["col_a", "col_b", "abs_corr"]

    filtered = pairs_df[pairs_df["abs_corr"] >= threshold]
    pairs = filtered[["col_a", "col_b", "abs_corr"]].values.tolist()
    flagged_cols = set(filtered[["col_a", "col_b"]].values.ravel())
    over_threshold_scores = filtered["abs_corr"].tolist()

    pair_ratio = 1.0 if pairs else 0.0
    excess_mean = float(np.mean(over_threshold_scores)) if over_threshold_scores else 0.0

    severity = float(np.clip(0.6 * pair_ratio + 0.4 * excess_mean, 0.0, 1.0))
    report = pd.DataFrame(pairs, columns=["col_a", "col_b", "abs_corr"]).sort_values("abs_corr", ascending=False)

    return report, sorted(flagged_cols), severity


# =============================
# Row problems
# =============================
def problematic_row_report(df: pd.DataFrame,
                           eps: float=Config.EPS):
    if not df.shape[1]:
        return pd.DataFrame(), pd.Series(dtype=float), 0.0

    invalid_mask = ~np.isfinite(df.to_numpy(dtype="float64", copy=False))
    invalid_row_mask = invalid_mask.any(axis=1)

    col_scores = []
    for c in df.columns:
        vals = df[c]
        med = vals.median(skipna=True)
        mad = np.median(np.abs(vals.dropna() - med)) if vals.notna().any() else 0.0
        robust_z = (vals - med).abs() / (mad + eps)
        col_scores.append(robust_z / (robust_z + 1.0))

    if col_scores:
        score_df = pd.concat(col_scores, axis=1)
        row_scores = score_df.mean(axis=1, skipna=True).fillna(0.0)
    else:
        row_scores = pd.Series(np.zeros(len(df)), index=df.index)

    invalid_ratio = float(invalid_row_mask.mean()) if len(df) else 0.0
    anomaly_mean = float(row_scores.mean()) if len(row_scores) else 0.0
    severity = float(np.clip(0.7 * invalid_ratio + 0.3 * anomaly_mean, 0.0, 1.0))

    out = pd.DataFrame({
        "row_index": df.index,
        "has_invalid_numeric": invalid_row_mask,
        "row_anomaly_score": row_scores.values,
    })
    out = out.sort_values("row_anomaly_score", ascending=False)

    return out, row_scores, severity

# =============================
# Relation and sparsity
# =============================
def compute_vif(df: pd.DataFrame):
    if df.shape[1] < 2:
        return {
            "mean": 0.0,
            "per_feature": dict(zip(df.columns, np.zeros_like(df.columns, dtype=float)))
        }
    
    vif_scores = []
    arr = df.dropna().to_numpy(dtype=float)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        
        for i in range(df.shape[1]):
            try:
                vif = variance_inflation_factor(arr, i)
                vif = pd.to_numeric(vif, errors="coerce")
            except Exception as e:
                vif_scores.append(float('inf'))
                _core.EXCEPTIONS.store({
                "type": type(e).__name__,
                "message": str(e),
                "where": "compute_vif computation",
                })
                continue

            if np.isnan(vif) or np.isinf(vif):
                vif_scores.append(float('inf'))

            else:
                vif_scores.append(float(vif))
            
        for warn in w:
            _core.WARNINGS.store({
            "type": warn.category.__name__,
            "message": str(warn.message),
            "where": "compute_vif computation",
        })

    raw = np.mean(vif_scores)
    norm_vif = np.tanh(raw / 10)

    return {
    "mean": norm_vif,
    "per_feature": dict(zip(df.columns, vif_scores))
    }

def relation_signal(df: pd.DataFrame,
                  target: str, 
                  task: str) -> float:
    if df.shape[0] < 2:
        return 0.0

    df = df.dropna()
    y = df[target]
    df = df.drop(target, axis=1)

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        try:
            if task == "classification":
                f_scores, _ = f_classif(df, y)
 
                mi = mutual_info_classif(df, y, discrete_features='auto')

                return pd.DataFrame(columns=["feature", "f", "mi"], data=list(zip(df.columns, f_scores, mi)))

            elif task == "regression":
                f_scores, _ = f_regression(df, y)

                mi = mutual_info_regression(df, y, discrete_features='auto')

                return pd.DataFrame(columns=["feature", "f", "mi"], data=list(zip(df.columns, f_scores, mi)))
            
        except Exception as e:
            _core.EXCEPTIONS.store({
                "type": type(e).__name__,
                "message": str(e),
                "where": "relation_signal computation",
            })

        for warn in w:
            _core.WARNINGS.store({
                "type": warn.category.__name__,
                "message": str(warn.message),
                "where": "relation_signal computation",
            })
    return pd.DataFrame(columns=["feature", "f", "mi"], data=list(zip(df.columns, np.zeros(len(df.columns)), np.zeros(len(df.columns)))))

def sparsity_ratio(df: pd.DataFrame):
    n_samples, n_features = df.shape

    zero_ratio = np.sum(df == 0) / df.size
    dim_penalty = n_features / (n_samples + n_features)
    
    return 0.7 * zero_ratio + 0.3 * dim_penalty

# =============================
# Normality
# =============================
def shapiro_per_feature(series: pd.Series):
    vals = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna().to_numpy()
    n = len(vals)
    
    if n < 3:
        return 0.0
    
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        try:
            if n <= 5000:
                _, p = stats.shapiro(vals)
                return float(p)
            
            rng = np.random.default_rng(42)
            sample = rng.choice(vals, size=5000, replace=False)

            _, p = stats.shapiro(sample)
            return float(p)
        
        except Exception as e:
            _core.EXCEPTIONS.store({
                "type": type(e).__name__,
                "message": str(e),
                "where": "shapiro_per_feature computation",
            })

        for warn in w:
            _core.WARNINGS.store({
                "type": warn.category.__name__,
                "message": str(warn.message),
                "where": "shapiro_per_feature computation",
            })

    return 0.0


def ks_per_feature(series: pd.Series, eps: float=Config.EPS):
    vals = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna().to_numpy()
    if len(vals) < 3:
        return 0.0

    std = np.std(vals)
    if std <= eps:
        return 1.0

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        try:
            _, p = stats.kstest(vals, "norm", args=(np.mean(vals), std))
            return float(p)

        except Exception as e:
            _core.EXCEPTIONS.store({
                "type": type(e).__name__,
                "message": str(e),
                "where": "ks_per_feature computation",
            })

        for warn in w:
            _core.WARNINGS.store({
                "type": warn.category.__name__,
                "message": str(warn.message),
                "where": "ks_per_feature computation",
            })

    return 0.0

def structure_distribution(df: pd.DataFrame):
    if df.shape[1] == 0:
        return 0.5

    skew_vals = []
    kurt_vals = []

    for col in df.columns:
        if df[col].nunique() > 1:
            skew_vals.append(abs(skew(df[col].dropna())))
            kurt_vals.append(abs(kurtosis(df[col].dropna())))

    dist_score = [1 - (0.5 * np.tanh(s / 2) + 0.5 * np.tanh(k / 5)) for s, k in zip(skew_vals, kurt_vals)]

    skew_mean = np.mean(skew_vals) if skew_vals else 0.0
    kurt_mean = np.mean(kurt_vals) if kurt_vals else 0.0

    skew_score = np.tanh(skew_mean / 2)
    kurt_score = np.tanh(kurt_mean / 5)

    overall_dist = 1 - (0.5 * skew_score + 0.5 * kurt_score)

    return pd.DataFrame({"column": df.columns, "skew": skew_vals, "kurt": kurt_vals, "dist_score": dist_score}), np.clip(overall_dist, 0.0, 1.0)

# =============================
# Reports
# =============================
def cleanliness_breakdown(
    nan_inf_df: pd.DataFrame,
    type_df: pd.DataFrame,
    sim_severity: float,
    row_severity: float,
) -> Reports.CleanlinessBreakdown:
    if len(nan_inf_df) == 0:
        missing_severity = 0.0
    else:
        missing_severity = float(np.clip(nan_inf_df["invalid_ratio"].mean(), 0.0, 1.0))

    if len(type_df) == 0:
        type_severity = 0.0
    else:
        type_severity = float(np.clip(type_df["bad_type_ratio"].mean(), 0.0, 1.0))

    return Reports.CleanlinessBreakdown(
        missing_severity=missing_severity,
        type_severity=type_severity,
        similarity_severity=float(np.clip(sim_severity, 0.0, 1.0)),
        row_severity=float(np.clip(row_severity, 0.0, 1.0)),
    )

def distribution_breakdown(
        df: pd.DataFrame,
        cat_col: list[str]
) -> Reports.DistributionReport:
    reports = {}
    for c in df.columns:
        is_cat = c in cat_col
        reports[c] = Reports.DistributionReport(df[c], is_cat).dist

    return pd.DataFrame.from_dict(reports, orient="index")