from . import _check_func as Check
from . import _core
from . import _configs as Config

import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_numeric_boxplot(df: pd.DataFrame, cat_col: list[str], title_suffix: str = "", download_plot: bool = False):

    spread_df = Check.distribution_report(df, cat_col, 1e-12, "fd").set_index("column")
    ordered_cols = spread_df.sort_values("spread_score", ascending=False).index.tolist()
    plot_df = df[ordered_cols]

    fig_w = max(12, 0.6 * len(ordered_cols) + 4)
    fig_h = max(6, 0.35 * len(ordered_cols) + 2)

    plt.figure(figsize=(fig_w, fig_h))
    sns.boxplot(data=plot_df, orient="h", showfliers=True, linewidth=1)
    plt.title(f"Boxplot Numeric Columns {title_suffix}".strip())
    plt.xlabel("Value")
    plt.ylabel("Column")
    plt.tight_layout()
    if download_plot:
      plt.savefig(f"boxplot_numeric_columns{title_suffix.replace(' ', '_')}.png", dpi=300)
      return
    plt.show()

def plot_numeric_heatmap(
    df: pd.DataFrame,
    title_suffix: str = "",
    download_plot: bool = False,
):
    corr = df.corr().fillna(0)

    mask = np.triu(np.ones_like(corr, dtype=bool))
    annot = len(df.columns) <= 12

    n_cols = len(df.columns)

    fig_size = max(10, min(24, 0.8 * n_cols))

    if n_cols <= 10:
        tick_size = 10
    elif n_cols <= 20:
        tick_size = 8
    else:
        tick_size = 6

    fig, ax = plt.subplots(
        figsize=(fig_size, fig_size),
        constrained_layout=True,
    )

    sns.heatmap(
        corr,
        mask=mask,
        cmap="coolwarm",
        vmin=-1,
        vmax=1,
        center=0,
        square=False,
        annot=annot,
        fmt=".2f" if annot else None,
        linewidths=0.4,
        cbar_kws={"shrink": 0.8},
        ax=ax,
    )

    ax.set_title(f"Heatmap Correlation {title_suffix}".strip())

    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        ha="right",
        fontsize=tick_size,
    )

    ax.set_yticklabels(
        ax.get_yticklabels(),
        rotation=0,
        fontsize=tick_size,
    )

    if download_plot:
        plt.savefig(
            f"heatmap_correlation{title_suffix.replace(' ', '_')}.png",
            dpi=300,
            bbox_inches="tight",
        )
        return

    plt.show()

def plots(df: pd.DataFrame, cat_col: list[str], n_slice: int, download_plot: bool = False):
    if df.empty:
        print("⚠️ No data available for plotting.")
        return
    
    if (df.shape[1] > 20 and n_slice == 'all') or (isinstance(n_slice, int) and n_slice > 20):
        _core.WARNINGS.store(
            {
                "type": "UserWarning",
                "message": f"Too many features to be plotted ({df.shape[1] if not isinstance(n_slice, int) else n_slice}), plot may be too ambiguous.",
                "where": "plots function"
            }
        )
        status = "n"
        if not Config.MUTE:
            status = input(f"Too many features to be plotted ({df.shape[1] if not isinstance(n_slice, int) else n_slice}), plot may be too ambiguous. \nContinue with plotting? (y/n): ").strip().lower()
        
        if status == "n":
            return
        
        elif status == "y":
            pass

        else:
            print("Invalid input, skipping plotting process.")
            return

    if n_slice == "all":
        if df.shape[1] < 2:
            print("⚠️ Number of valid numeric column has to be greater than 2 for plotting.")
            return
        
        plot_numeric_boxplot(df, cat_col, title_suffix="(all features)", download_plot=download_plot)
        plot_numeric_heatmap(df, title_suffix="(all features)", download_plot=download_plot)
        return

    n_slice = int(n_slice)
    cols = list(df.columns)

    for start in range(0, len(cols), n_slice):
        chunk_cols = cols[start:start + n_slice]
        chunk_df = df[chunk_cols]
        if chunk_df.empty or chunk_df.shape[1] < 2:
            continue

        title_suffix = f"(features {start + 1}-{start + len(chunk_cols)})"
        plot_numeric_boxplot(chunk_df, cat_col, title_suffix=title_suffix, download_plot=download_plot)
        plot_numeric_heatmap(chunk_df, title_suffix=title_suffix, download_plot=download_plot)
