import uvicorn
from fastapi import FastAPI

from agent.orchestrator import AutonomousAgent
from models.request import AgentRequest
from models.response import AgentResponse

app = FastAPI(title="Autonomous Document Agent")
agent = AutonomousAgent()


@app.post("/agent", response_model=AgentResponse)
def generate(request: AgentRequest):
    result = agent.run(request.request, request.conversation_id)
    return AgentResponse(**result)


@app.get("/health")
def health():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
