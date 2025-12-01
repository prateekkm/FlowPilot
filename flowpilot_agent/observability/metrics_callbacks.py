# flowpilot_agent/observability/metrics_callbacks.py

import time

TOTAL = 0
LAST_LATENCY = 0.0

def start():
    return time.time()

def end(start_time):
    global TOTAL, LAST_LATENCY
    TOTAL += 1
    LAST_LATENCY = time.time() - start_time
