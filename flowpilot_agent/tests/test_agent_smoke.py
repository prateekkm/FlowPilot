# tests/test_agent_smoke.py

"""
Very small smoke test for FlowPilot.

This doesn't check correctness of insights, just that the agent runs without
crashing when given a simple prompt.
"""

from flowpilot_agent.agent import run_flowpilot


def test_smoke_run():
    response = run_flowpilot(
        "Hello FlowPilot, this is a smoke test. You can ignore data analysis."
    )
    assert isinstance(response, str)
    assert len(response) > 0
