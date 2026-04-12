from dataclasses import dataclass
from typing import List


@dataclass
class PlanDecision:
    action: str
    confidence: float
    rationale: str


class SimplePlanner:
    """A transparent planner with deterministic action selection rules."""

    def __init__(self, actions: List[str]):
        if not actions:
            raise ValueError("Planner requires at least one action")
        self.actions = actions

    def choose(self, observation: str, memory_size: int) -> PlanDecision:
        normalized = observation.lower().strip()
        if any(token in normalized for token in ["sum", "add", "multiply", "math"]):
            action = "math" if "math" in self.actions else self.actions[0]
            return PlanDecision(action=action, confidence=0.9, rationale="math intent detected")
        if any(token in normalized for token in ["read", "write", "file", "path"]):
            action = "file" if "file" in self.actions else self.actions[0]
            return PlanDecision(action=action, confidence=0.85, rationale="file intent detected")

        # Fall back to text output while retaining memory length as interpretable context.
        fallback = "text_output" if "text_output" in self.actions else self.actions[0]
        return PlanDecision(
            action=fallback,
            confidence=max(0.5, min(0.8, 0.5 + memory_size * 0.01)),
            rationale="default response path",
        )
