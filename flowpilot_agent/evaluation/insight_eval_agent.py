# flowpilot_agent/evaluation/insight_eval_agent.py

"""
Insight evaluation agent for FlowPilot.

Implements an LLM-as-judge pattern to rate the quality of generated insights.
"""

from __future__ import annotations

from google.adk.agents import Agent  # type: ignore

from ..config import DEFAULT_MODEL


insight_eval_agent = Agent(
    name="flowpilot_insight_evaluator",
    model=DEFAULT_MODEL,
    description=(
        "Evaluates the quality of FlowPilot's insights for engineering workflows."
    ),
    instruction=(
        "You are an evaluation agent. Given a FlowPilot answer and the original "
        "user question, rate the answer on:\n"
        "- relevance to the question (1-5)\n"
        "- clarity (1-5)\n"
        "- actionability (1-5)\n"
        "- appropriate use of the provided data (1-5)\n\n"
        "Respond ONLY with a JSON object of the form:\n"
        "{\n"
        "  'relevance': <int>,\n"
        "  'clarity': <int>,\n"
        "  'actionability': <int>,\n"
        "  'data_use': <int>,\n"
        "  'comments': '<short explanation>'\n"
        "}\n"
    ),
)


def evaluate_insights(question: str, answer: str) -> str:
    """
    Convenience wrapper to call the evaluation agent.

    Returns:
        The raw string response from the evaluation agent, expected to be JSON.
    """
    prompt = (
        "User question:\n"
        f"{question}\n\n"
        "FlowPilot answer:\n"
        f"{answer}\n\n"
        "Now evaluate this answer according to your instructions."
    )
    return insight_eval_agent.run(prompt)  # type: ignore[no-any-return]
