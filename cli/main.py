import typer
import requests

app = typer.Typer()

@app.command()
def predict(image_path: str):
    with open(image_path, "rb") as f:
        files = {"file": (image_path, f, "image/jpeg")}
        response = requests.post("http://localhost:8000/predict", files=files)
    typer.echo(response.json())

if __name__ == "__main__":
    app()
