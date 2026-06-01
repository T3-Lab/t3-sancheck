from . import _helper as Help
from . import _configs as Config
from . import _check_func as Check

from dataclasses import dataclass

import numpy as np
import pandas as pd

@dataclass
class CleanlinessBreakdown:
    missing_severity: float
    type_severity: float
    similarity_severity: float
    row_severity: float

    @property
    def overall(self) -> float:
        weights = {
            "missing_severity": 0.30,
            "type_severity": 0.20,
            "similarity_severity": 0.20,
            "row_severity": 0.30,
        }
        penalty = (
            self.missing_severity * weights["missing_severity"]
            + self.type_severity * weights["type_severity"]
            + self.similarity_severity * weights["similarity_severity"]
            + self.row_severity * weights["row_severity"]
        )
        return float(np.clip(1.0 - penalty, 0.0, 1.0))

    @property
    def label(self) -> str:
        score = self.overall
        if score >= 0.85:
            return "[green]very clean[/green]"
        if score >= 0.70:
            return "[yellow]fairly clean[/yellow]"
        if score >= 0.50:
            return "[orange1]some issues[/orange1]"
        return "[red]dirty[/red]"

@dataclass
class DistributionReport:
    series: pd.Series
    is_cat: bool
    eps: float=Config.EPS
    bins=Config.ENTROPY_BINS

    @property
    def dist(self) -> dict:
        ent = Check.normalized_entropy(self.series, self.eps, self.is_cat, self.bins)
        spread_score, raw_var, iqr = Check.normalized_spread_score(self.series, self.eps)
        report = {
            "entropy": ent,
            "entropy_label": Help.entropy_interpretation(ent),
            "spread_score": spread_score,
            "spread_label": Help.spread_interpretation(spread_score),
            "variance": raw_var,
            "iqr": iqr,
        }

        return report