from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    request: str = Field(
        ...,
        min_length=10,
        max_length=5000,
        description="Natural language request (10-5000 characters)"
    )
    conversation_id: str = Field(
        default="",
        description="Optional conversation ID for multi-turn memory"
    )