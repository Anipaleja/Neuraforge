import typer

from core.runtime import build_runtime


def run(mode: str = "basic", config: str = "configs/agent_basic.yaml", steps: int = 3):
    """Run AXNL in the selected mode.

    README quickstart expects: python main.py --mode basic
    """
    if mode != "basic":
        raise typer.BadParameter("Only mode='basic' is currently implemented")

    runtime = build_runtime(config)
    typer.echo(f"Agent: {runtime.agent_name}")

    for i in range(steps):
        obs = typer.prompt(f"Observation {i + 1}")
        result = runtime.step(obs)
        typer.echo(result)
if __name__ == "__main__":
    typer.run(run)
