from google.adk.agents import Agent
from ..config import DEFAULT_MODEL
from .. import tools as t

data_ingestion_agent = Agent(
    name="data_ingestion_agent",
    model=DEFAULT_MODEL,
    description="Loads and validates Jira-like CSV data.",
    instruction=(
        "Use `load_issues_csv` to load the uploaded file. "
        "On success, store parsed issues in state under 'issues'."
    ),
    tools=[t.load_issues_csv],
)
