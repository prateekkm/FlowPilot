from google.adk.agents import Agent
from ..config import DEFAULT_MODEL
from .. import tools as t

action_agent = Agent(
    name="action_agent",
    model=DEFAULT_MODEL,
    description="Drafts actionable improvement plans.",
    instruction=(
        "Use `propose_long_running_action_plan` on issue_metrics. "
        "Clearly state plan requires approval before execution."
    ),
    tools=[t.propose_long_running_action_plan],
)
