from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.runtime import build_runtime

app = FastAPI()
runtime = build_runtime()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class StepRequest(BaseModel):
    observation: str


@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "agent": runtime.agent_name}


@app.post("/step")
async def step(req: StepRequest) -> dict:
    result = runtime.step(req.observation)
    return result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)