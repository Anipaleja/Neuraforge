import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data.image_pipeline import fuse_sensors

sample = fuse_sensors(
    text="detected movement",
    vision={"objects": ["person", "door"], "confidence": 0.88},
    audio={"keywords": ["open"], "energy": 0.31},
)
print(sample)
