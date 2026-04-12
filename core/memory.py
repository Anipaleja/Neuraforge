from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class EpisodicMemory:
    max_items: int = 100
    events: List[Dict[str, str]] = field(default_factory=list)

    def add(self, event: Dict[str, str]) -> None:
        self.events.append(event)
        if len(self.events) > self.max_items:
            self.events = self.events[-self.max_items :]

    def recent(self, n: int = 5) -> List[Dict[str, str]]:
        return self.events[-n:]

    def size(self) -> int:
        return len(self.events)
