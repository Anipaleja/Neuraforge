import os
from pathlib import Path

def list_files(path='.'):
    return sorted(os.listdir(path))

def read_file(file):
    with open(file, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(file, content):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)


def safe_resolve(base_dir: str, user_path: str) -> str:
    """Resolve relative paths and prevent escaping the configured workspace root."""
    base = Path(base_dir).resolve()
    target = (base / user_path).resolve()
    if not str(target).startswith(str(base)):
        raise ValueError("path escapes workspace root")
    return str(target)