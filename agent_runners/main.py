import os
import asyncio
from typing import Dict, Any, Optional

import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager

from core import config
from agents.agent_paper_crawler import AgentPaperCrawler

# Initialize agent globally
agent = AgentPaperCrawler(model_name="gpt-4o-mini", description="Assistant for analyzing papers")

class AgentRequest(BaseModel):
    question: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    print(f"Initializing agent with model: {agent.model_name}")
    agent.setup()
    print("Agent setup complete.")
    yield
    await agent.shutdown()

app = FastAPI(title="Agent Runner Service", lifespan=lifespan)

@app.get("/health")
async def health_check():
    return {"status": "ok", "agent_id": agent.agent_id}

@app.post("/request")
async def run_agent(request: AgentRequest):
    """
    Trigger the agent with the provided parameters.
    """
    result = await agent.run(request.dict())
    return result

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8002))
    uvicorn.run("main:app", host="localhost", port=port, reload=True)