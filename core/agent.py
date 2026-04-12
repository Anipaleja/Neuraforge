from dataclasses import dataclass
from typing import Callable, Dict

from core.memory import EpisodicMemory
from core.neural_planner import SimplePlanner


@dataclass
class AgentConfig:
    name: str
    actions: list[str]


class AXNLAgent:
    def __init__(
        self,
        config: AgentConfig,
        memory: EpisodicMemory,
        planner: SimplePlanner,
        tool_registry: Dict[str, Callable[[str], str]],
    ):
        self.config = config
        self.memory = memory
        self.planner = planner
        self.tool_registry = tool_registry

    def step(self, observation: str) -> dict:
        self.memory.add({"type": "observation", "value": observation})
        decision = self.planner.choose(observation, memory_size=self.memory.size())

        tool = self.tool_registry.get(decision.action, self.tool_registry["text_output"])
        output = tool(observation)

        self.memory.add({"type": "action", "value": decision.action})
        self.memory.add({"type": "output", "value": output})

        return {
            "agent": self.config.name,
            "decision": {
                "action": decision.action,
                "confidence": decision.confidence,
                "rationale": decision.rationale,
            },
            "output": output,
            "memory_size": self.memory.size(),
        }
