from ._core import analyze, EXCEPTIONS, WARNINGS
from . import _helper as Help
from . import _plotting as PLT
from . import _info as Info
from . import _configs as Config

import argparse
import sys
from sklearn.preprocessing import LabelEncoder

import pandas as pd
import numpy as np
import time
import json

from rich import print
from rich import box
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel

def main():
    console = Console()
    elapsed = time.time()
    ao = Help.ActionOptions()
    parser = argparse.ArgumentParser(
        description="SanCheck — data sanity checker"
    )
    parser.add_argument(
                        "csv", 
                        help="Path to CSV file"
                        )
    
    parser.add_argument(
                        "--target",
                        default=None,
                        help="Target column name"
                        )
    
    parser.add_argument(
        "--task",
        choices=["classification", "regression"],
        default=None,
        help="Type of machine learning task (default: None)"
    )

    parser.add_argument(
        "--exclude",
        default=None,
        help="Comma-separated list of columns to exclude from analysis"
    )

    parser.add_argument(
        "--cat-encode",
        default=None,
        help="Comma-separated list of categorical columns to encode using label encoding"
    )
    
    parser.add_argument(
        "--plot-chunk",
        default='all',
        type=Help.parse_slice_arg,
        help="Number of columns per chunk for plotting, or 'all' (default: 'all')",
    )
    
    parser.add_argument(
        "--download-plot",
        action="store_true",
        help="Download plots as PNG files (no plot visualization)",
    )

    parser.add_argument(
        "--no-plot",
        action="store_true",
        help="Skip plotting (overrides --download-plot)",
    )

    parser.add_argument(
        "--metrics-info",
        action=Help.InfoAction,
        help="Show detailed explanation of metrics",
        nargs=0
    )

    parser.add_argument(
        "--get-json",
        action="store_true",
        help="Output the report as JSON instead of printing to console"
    )

    parser.add_argument(
        "--mute",
        action="store_true",
        help="Mute safeguards and automatically fallback to the safest option"
    )
    
    args = parser.parse_args()

    Config.MUTE = args.mute

    cat_col = args.cat_encode
    exclude = args.exclude

    target = args.target
    task = args.task

    cat_col = cat_col.split(",") if cat_col else None
    exclude = exclude.split(",") if exclude else None

    if args.metrics_info:
        Info.metrics()

    try:
        df = pd.read_csv(args.csv)

    except Exception as e:
        print(f"❌ Failed to load the CSV file: {e}")
        sys.exit(1)

    if target is not None and task is None:
        print(f"❌ Failed to process target. 'target' argument must be followed by task spesification.")
        sys.exit(1)

    elif target is None and task is not None:
        print(f"❌ Failed to process task. 'task' argument must be followed by target spesification.")
        sys.exit(1)

    if target and not isinstance(target, str):
        print(f"❌ Failed to process target. 'target' argument must be a string")
        sys.exit(1)

    elif target and target not in df.columns:
        print(f"❌ Failed to process target. {target} column is not exist in the DataFrame.")
        sys.exit(1)
    
    # Valid col encode
    if cat_col and any(c not in df.columns for c in cat_col):
        print(f"❌ Failed to process categorical columns. One or more specified columns do not exist in the DataFrame.")
        sys.exit(1)

    if exclude and any(c not in df.columns for c in exclude):
        print(f"❌ Failed to process exclude columns. One or more specified columns do not exist in the DataFrame.")
        sys.exit(1)

    if exclude:
        df = df.drop(exclude, axis=1)

    if task == "classification":
        cat_col = [target] if cat_col is None else list(set(cat_col) | {target})

    if cat_col:
        for c in cat_col:
            le = LabelEncoder()
            mask = df[c].notna()
            encoded = le.fit_transform(df[c].loc[mask])
            encoded_series = pd.Series(index=df[c].index, dtype="Int64")
            encoded_series.loc[mask] = encoded
            df[c] = encoded_series

    numeric_cols = Help.get_numeric_valid_columns(df)
    ignored_cols = [c for c in df.columns if c not in numeric_cols]

    df_numeric = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    if not numeric_cols:
        print("❌ No numeric columns found with sufficient valid numeric ratio.")
        print(f"Non-numeric columns / ignored: {', '.join(ignored_cols) if ignored_cols else '-'}")
        sys.exit(1)

    # JSON output
    if args.get_json:
        with console.status("[bold yellow]Processing your data...", spinner='dots') as status:
            with open("sancheck_report.json", "w") as f:
                json.dump(analyze(df_numeric, cat_col, target, task, True), f, cls=Help.ReportEncoder, indent=4)

            console.print("✅ [bold green]Report saved to sancheck_report.json[/bold green]")
            # plotting
            if not args.no_plot:
                PLT.plots(df_numeric, cat_col, n_slice=args.plot_chunk, download_plot=args.download_plot)
            return
    
    with console.status("[bold yellow]Processing your data...", spinner='dots'):
        # Reports
        analysis_results = analyze(df_numeric, cat_col, target, task, False)
        sim_pairs = analysis_results["similarity_report"]["pairs"]
        sim_cols = analysis_results["similarity_report"]["affected_columns"]
        sim_severity = analysis_results["similarity_report"]["severity"]
        nan_inf_df = analysis_results["nan_inf_report"]
        type_df = analysis_results["type_inconsistency_report"]
        structure_dist = analysis_results["structure_dist"]
        overall_dist = analysis_results["overall_dist"]
        rel_signal = analysis_results["rel_signal"]
        row_df = analysis_results["problematic_rows_report"]["rows"]
        row_scores = analysis_results["problematic_rows_report"]["scores"]
        row_severity = analysis_results["problematic_rows_report"]["severity"]
        dist_df = analysis_results["distribution_report"]
        cleanliness = analysis_results["cleanliness_breakdown"]
        sparsity = analysis_results["sparsity_ratio"]
        vif = analysis_results["vif"]
        override_rat = analysis_results["class_override_ratio"]
        imbalance_rat = analysis_results["class_imbalance_ratio"]
        shapiro = analysis_results["shapiro_scores"]
        ks = analysis_results["ks_scores"]

        # Cache commonly reused, small subsets to avoid repeated sorting/indexing
        top_entropy = dist_df.sort_values("entropy", ascending=False).head(5)
        top_spread = dist_df.sort_values("spread_score", ascending=False).head(5)
        top_rows = row_df.head(5)

        top_nan = nan_inf_df.sort_values("invalid_ratio", ascending=False).head(10) if len(nan_inf_df) else nan_inf_df
        top_type = type_df.sort_values("bad_type_ratio", ascending=False).head(10) if len(type_df) else type_df
        sim_pairs_head = sim_pairs.head(10) if hasattr(sim_pairs, "head") else sim_pairs

        nan_count = int((nan_inf_df.get("invalid_ratio", pd.Series([], dtype=float)) > 0).sum()) if len(nan_inf_df) else 0
        flagged_count = int(type_df["flagged"].sum()) if len(type_df) else 0

        # Precompute relation maps for faster lookup by feature name
        if rel_signal is not None and hasattr(rel_signal, "__len__") and len(rel_signal):
            rel_map_mi = dict(zip(rel_signal["feature"], rel_signal["mi"]))
            rel_map_f = dict(zip(rel_signal["feature"], rel_signal["f"]))
        else:
            rel_map_mi = {}
            rel_map_f = {}

        # Cache structure distribution values to avoid repeated .values access
        structure_dist_vals = list(structure_dist.values) if hasattr(structure_dist, "values") else list(structure_dist)
    console.print("[bold green] Done! [/bold green]")

    try:
        if not task or not target:
            print("⚠️ [red] Without task and target specification some metrics are disabled [/red]\n")

        # Dataset summary
        summary_table = Table(title="Dataset Summary", header_style="yellow", box=box.ROUNDED)
        summary_table.add_column("Info", style='cyan', justify="left")
        summary_table.add_column("Value", justify="right")
        summary_table.add_row("Valid numeric columns", str(len(numeric_cols)))
        summary_table.add_row("Ignored non-numeric columns", str(len(ignored_cols)))
        if args.task:
            summary_table.add_row("Task type", task)

        console.print(summary_table)

        # Column problems
        col_table = Table(title="Invalid Values", box=box.ROUNDED, header_style="yellow")
        col_table.add_column("Issue", style="red", justify="left")
        col_table.add_column("Column", justify="left")
        col_table.add_column("Details", justify="left")

        for _, r in top_nan.iterrows():
            col_table.add_row("NaN/Inf", str(r["column"]), f"invalid  = {int(r['invalid_total'])}/{int(r['total'])} ({r['invalid_ratio']:.3f})")

        for _, r in top_type.iterrows():
            col_table.add_row("Type inconsistency", str(r["column"]), f"bad_type = {int(r['bad_type_total'])}/{int(r['total'])} ({r['bad_type_ratio']:.3f})")

        col_table_2 = Table(title="Column Similarity Pairs", box=box.ROUNDED, header_style="yellow")
        col_table_2.add_column("Pair", style="blue", justify="left")
        col_table_2.add_column("|corr|", justify="right")
        
        if len(sim_pairs) > 0:
            for _, r in sim_pairs_head.iterrows():
                col_table_2.add_row(f"{r['col_a']} <-> {r['col_b']}", f"{r['abs_corr']:.3f}")
            if sim_cols:
                col_detail = f"Affected columns: {', '.join(sim_cols)}"
        else:
            col_detail = "Affected columns: -"
            col_table_2.add_row("-", "-")
        
        column_report = Group(
            col_table,
            f"NaN/Inf columns: {str(nan_count)}",
            f"Type inconsistent columns: {str(flagged_count)}",
            col_table_2,
            col_detail,
            f"Severity: {sim_severity:.3f}"
        )

        console.print(Panel(column_report, title="[bold]Column Report[/]", expand=False))

        # Row problems
        row_table = Table(title=f"Top {"5" if len(top_rows) >= 5 else str(len(top_rows))} anomalous rows", header_style="yellow", box=box.ROUNDED)
        row_table.add_column("Row index", style="blue", justify="center")
        row_table.add_column("Anomaly score", justify="right")
        row_table.add_column("Invalid", justify="center")

        invalid_row_count = int(row_df["has_invalid_numeric"].sum()) if len(row_df) else 0

        for _, r in top_rows.iterrows():
            row_table.add_row(f"row {int(r['row_index'])}", f"{r['row_anomaly_score']:.3f}", f"{bool(r['has_invalid_numeric'])}")
        
        row_report = Group(
            row_table,
            f"Problematic rows: {invalid_row_count} / {len(df)}",
            f"Row severity: {row_severity:.3f} / 1.000"
        )

        console.print(Panel(row_report, title="[bold]Row report[/]", expand=False))

        # Distribution: top entropy and top spread
        entropy_table = Table(title=f"Top {"5" if len(top_entropy) >= 5 else str(len(top_entropy))} Entropy", box=box.ROUNDED, header_style="yellow")
        entropy_table.add_column("Column", style="blue", justify="left")
        entropy_table.add_column("Entropy", justify="right")
        entropy_table.add_column("Label", justify='center')
        for _, r in top_entropy.iterrows():
            entropy_table.add_row(str(r["index"]), f"{r['entropy']:.3f} / 1.000", r.get("entropy_label", "-"))

        spread_table = Table(title=f"Top {"5" if len(top_spread) >= 5 else str(len(top_spread))} Spread", box=box.ROUNDED, header_style="yellow")
        spread_table.add_column("Column", style="blue", justify="left")
        spread_table.add_column("Spread", justify="right")
        spread_table.add_column("Label", justify="center")
        spread_table.add_column("Var", justify="right")
        spread_table.add_column("IQR", justify="right")
        for _, r in top_spread.iterrows():
            spread_table.add_row(str(r["index"]), f"{r['spread_score']:.3f} / 1.000", r.get("spread_label", "-"), f"{r['variance']:.3f}", f"{r['iqr']:.3f}")

        distribution_report = Group(
            spread_table,
            entropy_table,
            f"Avg entropy: {dist_df['entropy'].mean():.3f}",
            f"Avg spread score: {dist_df['spread_score'].mean():.3f}"
        )

        console.print(Panel(distribution_report, title="[bold]Distribution Report[/]", expand=False))
        
        # Normality
        normality_table = Table(title="Distribution Normality", box=box.ROUNDED, header_style="yellow")
        normality_table.add_column("Feature", style="blue", justify="left")
        normality_table.add_column("Shapiro", justify="right")
        normality_table.add_column("KS", justify="right")
        for c in numeric_cols:
            sh = shapiro.get(c, None)
            ksval = ks.get(c, None)
            sh_s = f"{sh:.3f}" if sh is not None else "None"
            ks_s = f"{ksval:.3f}" if ksval is not None else "None"

            if sh is None and ksval is None:
                continue

            normality_table.add_row(str(c), sh_s, ks_s)

        struc_dist_table = Table(title="Structure Distribution", box=box.ROUNDED, header_style="yellow")
        struc_dist_table.add_column("Feature", style="blue", justify="left")
        struc_dist_table.add_column("Skewness", justify="right")
        struc_dist_table.add_column("Kurtosis", justify="right")
        struc_dist_table.add_column("Distribution score", justify="right")
        for c, s, k, v in structure_dist_vals:
            skew = f"{s:.3f}"
            kurt = f"{k:.3f}"
            score = f"{v:.3f}"
            struc_dist_table.add_row(str(c), skew, kurt, score)

        normality_report = Group(
            normality_table,
            struc_dist_table,
            f"Overall structure distribution score: {overall_dist:.3f} / 1.000 ({Help._label_from_score(overall_dist, ascending=True)})"
        )
        console.print(Panel(normality_report, title="[bold]Normality Report[/]", expand=False))

        # Relation and structure
        struc_table = Table(title="Structure", header_style="yellow", box=box.ROUNDED)
        struc_table.add_column("Metric", style="blue", justify="left")
        struc_table.add_column("Value", justify="right")
        struc_table.add_row("Sparsity", f"{sparsity:.3f} / 1.000 ({Help._label_from_score(sparsity)})")
        if task == 'classification':
            struc_table.add_row("Class imbalance ratio", f"{imbalance_rat:.3f} / 1.000 ({Help._label_from_score(imbalance_rat)})")
            struc_table.add_row("Class override ratio", f"{override_rat:.3f} / 1.000 ({Help._label_from_score(override_rat)})")

        rel_table = Table(title="Relation", box=box.ROUNDED, header_style="yellow")
        rel_table.add_column("Feature", style="blue", justify="left")
        rel_table.add_column("VIF", justify="right")
        rel_table.add_column("MI", justify="right")
        rel_table.add_column("F-score", justify="right")

        for c in numeric_cols:
            val = vif["per_feature"][c]
            if val is None:
                v = "-"
            elif np.isinf(val):
                v = "inf"
            else:
                v = f"{val:.3f}"

            m = "-"
            f_val = "-"
            if task and c != target:
                mi = rel_map_mi.get(c, None)
                fscore = rel_map_f.get(c, None)

                if mi is None:
                    m = "-"
                elif np.isinf(mi):
                    m = "inf"
                else:
                    m = f"{mi:.3f}"

                if fscore is None:
                    f_val = "-"
                elif np.isinf(fscore):
                    f_val = "inf"
                else:
                    f_val = f"{fscore:.3f}"

            rel_table.add_row(str(c), v, m, f_val)

        struc_n_rel_report = Group(
            struc_table,
            rel_table,
            f"Avg VIF: {vif['mean']:.3f} / 1.000 ({Help._label_from_score(vif['mean'])})"
        )
        console.print(Panel(struc_n_rel_report, title="[bold]Structure & Relation Report", expand=False))

        # Cleanliness
        clean_table = Table(title="Cleanliness Status", box=box.ROUNDED, header_style="yellow")
        clean_table.add_column("Metric", style="blue")
        clean_table.add_column("Value")
        clean_table.add_row("Cleanliness score", f"{cleanliness.overall:.3f} / 1.000 ({cleanliness.label})")
        clean_table.add_row("Missing severity", f"{cleanliness.missing_severity:.3f} / 1.000 ({Help._label_from_score(cleanliness.missing_severity)})")
        clean_table.add_row("Type severity", f"{cleanliness.type_severity:.3f} / 1.000 ({Help._label_from_score(cleanliness.type_severity)})")
        clean_table.add_row("Similarity severity", f"{cleanliness.similarity_severity:.3f} / 1.000 ({Help._label_from_score(cleanliness.similarity_severity)})")
        clean_table.add_row("Row severity", f"{cleanliness.row_severity:.3f} / 1.000 ({Help._label_from_score(cleanliness.row_severity)})")
        console.print(clean_table)

        # Action suggestions
        act_tab = Table(title="[bold]Actions Suggestion[/]", box=box.ROUNDED, header_style="yellow")
        act_tab.add_column("Type", style="blue", header_style="yellow")
        act_tab.add_column("Action", header_style="yellow")

        for _, r in top_nan.iterrows():
            act = ao.col_act(r["invalid_ratio"], r["column"])
            if act is None:
                continue
            act_tab.add_row("Column", act)

        for _, r in top_rows.iterrows():
            act = ao.row_act(r["row_anomaly_score"], r["row_index"])
            if act is None:
                continue
            act_tab.add_row("Row", act)

        if len(sim_pairs) > 0:
            for _, r in sim_pairs_head.iterrows():
                act = ao.corr_act(r['abs_corr'], f"{r['col_a']} <-> {r['col_b']}")
                if act is None:
                    continue
                act_tab.add_row("Correlation", act)

        for c, s, k, v in structure_dist_vals:
            struc_act = ao.struc_norm(v, c)
            if struc_act is not None:
                act_tab.add_row("Structure normality", struc_act)

        for c in numeric_cols:
            val = vif["per_feature"][c]
            vif_act = ao.vif_act(val, c)
            if vif_act is not None:
                act_tab.add_row("Multicollinearity", vif_act)

        console.print(act_tab)

        console.print(f"⏱️ Elapsed time: {time.time() - elapsed:.2f} seconds", style="bold green")

    except Exception as e:
        EXCEPTIONS.store({
            "type": type(e).__name__,
            "message": str(e),
            "where": "Print analysis result"
        })

        console.print("[bold red]========== SNAP! ==========[/bold red]")
        console.print(f"⚠️ There's an exception during printing process: {str(e)}", style="bold red")

    # Exceptions and warnings (if any)
    if EXCEPTIONS.data:
        exc_table = Table(title="❌ Exceptions During Process", header_style="bold red", box=box.ROUNDED)
        exc_table.add_column("Type", style="red")
        exc_table.add_column("Message")
        exc_table.add_column("Where")
        for ex in EXCEPTIONS.data:
            exc_table.add_row(ex.get("type"), ex.get("message"), ex.get("where"))
        console.print(exc_table)

    if WARNINGS.data:
        warn_table = Table(title="⚠️ Warnings During Process", header_style="bold yellow", box=box.ROUNDED)
        warn_table.add_column("Type", style="yellow")
        warn_table.add_column("Message")
        warn_table.add_column("Where")
        for w in WARNINGS.data:
            warn_table.add_row(w.get("type"), w.get("message"), w.get("where"))
        console.print(warn_table)

    # plotting
    if not args.no_plot:
        PLT.plots(df_numeric, cat_col, n_slice=args.plot_chunk, download_plot=args.download_plot)
