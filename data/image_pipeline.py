from typing import Any, Dict


def fuse_sensors(text: str = "", vision: Dict[str, Any] | None = None, audio: Dict[str, Any] | None = None) -> Dict[str, Any]:
    """Normalize multimodal observations into one inspectable payload."""
    return {
        "text": text,
        "vision": vision or {},
        "audio": audio or {},
        "has_vision": bool(vision),
        "has_audio": bool(audio),
    }
