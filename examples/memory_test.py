import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.runtime import build_runtime

runtime = build_runtime("configs/agent_basic.yaml")
for idx in range(5):
    print(runtime.step(f"event {idx}"))
