from google.adk.agents import Agent
from google.adk.tools import google_search
from ..config import DEFAULT_MODEL

insight_agent = Agent(
    name="insight_agent",
    model=DEFAULT_MODEL,
    description="Explains metrics & recommends improvements.",
    instruction=(
        "Analyze `issue_metrics` in state. "
        "Explain causes and suggest improvements. "
        "Use google_search if needed to enhance guidance."
    ),
    tools=[google_search],
)
