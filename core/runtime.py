import json
from pathlib import Path
from typing import Any, Dict

import yaml

from core.agent import AXNLAgent, AgentConfig
from core.memory import EpisodicMemory
from core.neural_planner import SimplePlanner
from tools.file_tool import list_files, read_file, safe_resolve, write_file


class Runtime:
    def __init__(self, agent: AXNLAgent):
        self.agent = agent
        self.agent_name = agent.config.name

    def step(self, observation: str) -> dict:
        return self.agent.step(observation)


def _load_config(config_path: str | None = None) -> Dict[str, Any]:
    default_path = Path("configs/agent_basic.yaml")
    path = Path(config_path) if config_path else default_path
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    if path.suffix.lower() == ".json":
        return json.loads(path.read_text(encoding="utf-8"))
    if path.suffix.lower() in {".yaml", ".yml"}:
        return yaml.safe_load(path.read_text(encoding="utf-8"))

    raise ValueError("Config must be .json, .yaml, or .yml")


def build_runtime(config_path: str | None = None) -> Runtime:
    cfg = _load_config(config_path)
    agent_cfg = cfg.get("agent", {})

    actions = agent_cfg.get("actions", ["text_output"])
    memory = EpisodicMemory(max_items=agent_cfg.get("memory_size", 100))
    planner = SimplePlanner(actions=actions)

    workspace_root = str(Path(".").resolve())

    def text_tool(observation: str) -> str:
        return f"AXNL observed: {observation}"

    def math_tool(observation: str) -> str:
        normalized = observation.replace("+", " + ").replace("*", " * ").split()
        nums = [float(tok) for tok in normalized if tok.replace(".", "", 1).isdigit()]
        if "*" in normalized and len(nums) >= 2:
            return str(nums[0] * nums[1])
        if len(nums) >= 2:
            return str(sum(nums))
        return "No math operands detected"

    def file_tool(observation: str) -> str:
        parts = observation.split(" ", 2)
        command = parts[0].lower() if parts else ""
        if command == "ls":
            rel = parts[1] if len(parts) > 1 else "."
            path = safe_resolve(workspace_root, rel)
            return json.dumps(list_files(path))
        if command == "read" and len(parts) > 1:
            path = safe_resolve(workspace_root, parts[1])
            return read_file(path)
        if command == "write" and len(parts) > 2:
            path = safe_resolve(workspace_root, parts[1])
            write_file(path, parts[2])
            return "ok"
        return "File tool commands: ls [path], read <path>, write <path> <content>"

    registry = {
        "text_output": text_tool,
        "math": math_tool,
        "file": file_tool,
    }

    config = AgentConfig(
        name=agent_cfg.get("name", "AXN-Agent"),
        actions=actions,
    )
    return Runtime(AXNLAgent(config, memory, planner, registry))
