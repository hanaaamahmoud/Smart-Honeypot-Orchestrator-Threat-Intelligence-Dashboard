from fastapi import FastAPI
from core.orchestrator import Orchestrator


app = FastAPI(
    title="Smart Honeypot Orchestrator API",
    version="1.0.0"
)

orchestrator = Orchestrator()


@app.get("/status")
def get_status():
    return orchestrator.get_honeypot_status()