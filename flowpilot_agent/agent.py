# flowpilot_agent/agent.py

"""Root orchestrator agent for FlowPilot.

This file defines:
- `root_agent`: the ADK Agent discovered by `adk web` / `adk run`.
- `run_flowpilot`: a convenience function to invoke the agent with observability.
"""

from __future__ import annotations

import os
from typing import Optional

from dotenv import load_dotenv
from google.adk.agents import Agent  # type: ignore

from .config import DEFAULT_MODEL
from .sub_agents.data_ingestion_agent import data_ingestion_agent
from .sub_agents.analytics_agent import analytics_agent
from .sub_agents.insight_agent import insight_agent
from .sub_agents.action_agent import action_agent
from .memory import session_state
from .observability.logging_callbacks import (
    configure_logging,
    log_request,
    log_response,
)
from .observability.metrics_callbacks import (
    record_request_start,
    record_request_end,
    get_metrics_snapshot,
)

# Load .env file if it exists
load_dotenv()

# Validate API key exists
if "GOOGLE_API_KEY" not in os.environ:
    print("WARNING: GOOGLE_API_KEY not found in environment.")
    print("Please set it via .env file or OS environment variable.")

root_agent = Agent(
    name="flowpilot_root",
    model=DEFAULT_MODEL,
    description=(
        "FlowPilot – Engineering Productivity Insight Agent. "
        "A multi-agent system that analyzes Jira-like issue data (CSV exports) "
        "to uncover bottlenecks and recommend improvements."
    ),
    instruction=(
        "You are the orchestrator of a team of specialized agents.\n\n"
        "Typical workflow:\n"
        "1) Ask the user to upload an issue CSV file if not already provided.\n"
        "2) Delegate to data_ingestion_agent to parse and validate the file.\n"
        "3) Once issues are available in state, delegate to analytics_agent "
        "   to compute metrics (cycle time, AIR delays, SLA compliance).\n"
        "4) Delegate to insight_agent to explain the metrics and propose insights.\n"
        "5) If the user asks for concrete action plans, delegate to action_agent.\n\n"
        "Maintain a conversational tone and support follow-up questions. "
        "If tools return errors (e.g., malformed CSV), surface them clearly and "
        "guide the user to fix the input."
    ),
    sub_agents=[
        data_ingestion_agent,
        analytics_agent,
        insight_agent,
        action_agent,
    ],
)


def run_flowpilot(prompt: str, session_id: Optional[str] = None) -> str:
    """
    Convenience function to run the root agent with basic
    session handling, logging, and metrics.

    Args:
        prompt: The user prompt or question.
        session_id: Optional identifier to group related requests.

    Returns:
        The agent's response as a string.
    """
    configure_logging()  # idempotent
    sid = session_id or "default"

    # Session memory: append prompt to history
    session_state.append_to_history(sid, f"USER: {prompt}")

    # Observability: log + metrics
    log_request(prompt, session_id=sid)
    start = record_request_start()

    # Run the orchestrator agent
    response = root_agent.run(prompt)  # type: ignore[no-any-return]

    # Post-processing observability
    record_request_end(start)
    log_response(response, session_id=sid)
    session_state.append_to_history(sid, f"FLOWPILOT: {response}")

    # (Optional) Print metrics snapshot to make it visible in CLI logs
    metrics = get_metrics_snapshot()
    print(
        f"[FlowPilot Metrics] total_requests={metrics.total_requests} "
        f"last_latency_seconds={metrics.last_latency_seconds:.3f}"
    )

    return response
