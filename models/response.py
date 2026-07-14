from pydantic import BaseModel


class AgentResponse(BaseModel):
    status: str
    plan: list[str]
    assumptions: list[str]
    review: dict
    document: str
    conversation_id: str
