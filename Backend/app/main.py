import asyncio
from contextlib import asynccontextmanager
from typing import List

import requests

from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from app.websocket.manager import ConnectionManager
from app.websocket.producer import mock_event_producer

from app.data.mock_data import (
    MOCK_STATISTICS,
    MOCK_RECENT_EVENTS,
    MOCK_TOP_ATTACKERS,
    MOCK_COUNTRIES
)

from app.models.schemas import (
    HoneypotStatus,
    StatisticsResponse,
    RecentEvent,
    TopAttacker,
    CountryAttacks
)


manager = ConnectionManager()


@asynccontextmanager
async def lifespan(app: FastAPI):

    producer_task = asyncio.create_task(
        mock_event_producer(manager)
    )

    yield

    producer_task.cancel()

    try:
        await producer_task
    except asyncio.CancelledError:
        pass


app = FastAPI(
    title="Smart Honeypot Backend",
    version="1.0.0",
    lifespan=lifespan
)


ORCHESTRATOR_URL = "http://127.0.0.1:8000"


@app.get("/")
def root():
    return {
        "message": "Smart Honeypot Backend is running"
    }


@app.get("/honeypots", response_model=List[HoneypotStatus])
def get_honeypots():

    response = requests.get(
        f"{ORCHESTRATOR_URL}/status"
    )

    response.raise_for_status()

    return response.json()


@app.get("/statistics", response_model=StatisticsResponse)
def get_statistics():

    honeypots = get_honeypots()

    active_honeypots = sum(
        1
        for honeypot in honeypots
        if honeypot["status"] == "running"
    )

    return {
        "totalAttacks": MOCK_STATISTICS["totalAttacks"],
        "activeHoneypots": active_honeypots,
        "uniqueSources": MOCK_STATISTICS["uniqueSources"],
        "countries": MOCK_STATISTICS["countries"]
    }


@app.get("/events/recent", response_model=List[RecentEvent])
def get_recent_events():
    return MOCK_RECENT_EVENTS


@app.get("/attackers/top", response_model=List[TopAttacker])
def get_top_attackers():
    return MOCK_TOP_ATTACKERS


@app.get("/attacks/countries", response_model=List[CountryAttacks])
def get_attacks_by_country():
    return MOCK_COUNTRIES


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)