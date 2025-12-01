from google.adk.agents import Agent
from ..config import DEFAULT_MODEL
from .. import tools as t

analytics_agent = Agent(
    name="analytics_agent",
    model=DEFAULT_MODEL,
    description="Computes bottleneck metrics.",
    instruction=(
        "Run `compute_issue_metrics` on issues in state. "
        "Store results as 'issue_metrics'."
    ),
    tools=[t.compute_issue_metrics],
)
