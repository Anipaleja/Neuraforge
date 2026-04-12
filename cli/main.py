import typer
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.runtime import build_runtime

app = typer.Typer()
runtime = build_runtime()

@app.command()
def step(observation: str):
    """Run one agent loop iteration for a single observation."""
    typer.echo(runtime.step(observation))


@app.command()
def run(steps: int = 3):
    """Run a tiny interactive loop for quick experimentation."""
    for i in range(steps):
        obs = typer.prompt(f"Observation {i + 1}")
        typer.echo(runtime.step(obs))

if __name__ == "__main__":
    app()
