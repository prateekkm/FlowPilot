# flowpilot_agent/observability/logging_callbacks.py

import logging

log = logging.getLogger("flowpilot")

def configure_logging():
    if not log.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter("%(asctime)s | %(message)s")
        handler.setFormatter(formatter)
        log.addHandler(handler)
    log.setLevel(logging.INFO)

def log_in(prompt: str):
    log.info(f"USER: {prompt[:200]}")

def log_out(response: str):
    log.info(f"AGENT: {response[:200]}")
