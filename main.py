from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from livekit import api
from dotenv import load_dotenv
import os
import asyncio

from agent_runner import run_agent

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

LIVEKIT_URL = os.getenv("LIVEKIT_URL")
API_KEY = os.getenv("LIVEKIT_API_KEY")
API_SECRET = os.getenv("LIVEKIT_API_SECRET")

agent_task = None

@app.get("/token")
def generate_token(identity: str = "browser-user"):
    at = api.AccessToken(API_KEY, API_SECRET)
    at.identity = identity
    at.grants = api.VideoGrants(room="demo-room", room_join=True)
    token = at.to_jwt()
    return {"url": LIVEKIT_URL, "token": token}

@app.get("/start_agent")
async def start_agent():
    global agent_task
    if agent_task:
        return {"message": "Agent already running"}

    at = api.AccessToken(API_KEY, API_SECRET)
    at.identity = "python-agent"
    at.grants = api.VideoGrants(room="demo-room", room_join=True)
    token = at.to_jwt()

    agent_task = asyncio.create_task(run_agent(LIVEKIT_URL, token))
    return {"message": "Agent started"}

@app.get("/status")
def status():
    return {"agent_running": agent_task is not None}

# Serve static files
try:
    app.mount("/", StaticFiles(directory=".", html=True), name="static")
except Exception as e:
    print(f"Warning: Could not mount static files: {e}")
