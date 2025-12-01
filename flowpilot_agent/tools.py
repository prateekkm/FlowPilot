# flowpilot_agent/tools.py

from __future__ import annotations

import io
from dataclasses import dataclass
from typing import List, Dict, Any

import pandas as pd

from .config import ISSUE_COLUMNS, DEFAULT_SLA_DAYS


@dataclass
class IssueMetrics:
    total_issues: int
    avg_resolution_time: float
    slow_issues_count: int
    slow_issues_ratio: float
    top_bottleneck_statuses: List[Dict[str, Any]]


def load_issues_csv(csv_bytes: bytes) -> Dict[str, Any]:
    try:
        df = pd.read_csv(io.BytesIO(csv_bytes))

        for canonical, actual in ISSUE_COLUMNS.items():
            if actual not in df.columns:
                return {"status": "error", "error_message": f"Missing column: {actual}"}

        df = df[list(ISSUE_COLUMNS.values())]
        issues = df.to_dict(orient="records")
        return {"status": "success", "issues": issues}

    except Exception as exc:
        return {"status": "error", "error_message": f"Failed to parse CSV: {exc}"}


def compute_issue_metrics(issues: List[Dict[str, Any]]) -> Dict[str, Any]:
    if not issues:
        return {"status": "error", "error_message": "No issues provided."}

    df = pd.DataFrame(issues)
    df["resolution_time_days"] = pd.to_numeric(df["resolution_time_days"], errors="coerce")

    total = len(df)
    avg = float(df["resolution_time_days"].mean())
    slow_mask = df["resolution_time_days"] > DEFAULT_SLA_DAYS

    metrics = IssueMetrics(
        total_issues=total,
        avg_resolution_time=avg,
        slow_issues_count=int(slow_mask.sum()),
        slow_issues_ratio=float(slow_mask.sum() / total) if total else 0.0,
        top_bottleneck_statuses=[
            {"status": s, "avg_resolution_time_days": float(v)}
            for s, v in df.groupby("status")["resolution_time_days"]
            .mean().sort_values(ascending=False).head(5).items()
        ],
    )
    return {"status": "success", "metrics": metrics.__dict__}


def propose_long_running_action_plan(metrics: Dict[str, Any]) -> Dict[str, Any]:
    plan = {
        "focus": "Reduce cycle times",
        "candidate_actions": [
            {"status": x["status"], "reason": "High resolution time"}
            for x in metrics.get("top_bottleneck_statuses", [])
        ],
    }
    return {"status": "success", "proposed_plan": plan}
