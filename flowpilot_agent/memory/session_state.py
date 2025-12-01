# flowpilot_agent/memory/session_state.py

from dataclasses import dataclass, field
from typing import Dict, List, Any

@dataclass
class SessionContext:
    session_id: str
    history: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)

_STORE: Dict[str, SessionContext] = {}

def get_session(sid: str) -> SessionContext:
    return _STORE.setdefault(sid, SessionContext(session_id=sid))

def append_history(sid: str, text: str) -> None:
    get_session(sid).history.append(text)
