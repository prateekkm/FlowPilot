# flowpilot_agent/config.py

DEFAULT_MODEL = "gemini-2.0-flash"
APP_NAME = "flowpilot_engineering_productivity_insight_agent"

ISSUE_COLUMNS = {
    "ticket_id": "ticket_id",
    "summary": "summary",
    "status": "status",
    "air_hops": "air_hops",
    "air_days": "air_days",
    "resolution_time_days": "resolution_time_days",
    "priority": "priority",
    "assignee": "assignee",
    "created_at": "created_at",
    "resolved_at": "resolved_at",
}

DEFAULT_SLA_DAYS = 3
