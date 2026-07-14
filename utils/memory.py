import json
import os
from datetime import datetime
from uuid import uuid4


class ConversationMemory:

    MEMORY_DIR = "conversations"

    def __init__(self):
        os.makedirs(self.MEMORY_DIR, exist_ok=True)

    def create_conversation(self) -> str:
        cid = str(uuid4())[:8]
        self._save(cid, {"history": [], "created_at": str(datetime.now())})
        return cid

    def add_turn(self, conversation_id: str, user_request: str, agent_response: dict):
        data = self._load(conversation_id)
        turn = {
            "timestamp": str(datetime.now()),
            "user_request": user_request,
            "agent_response": {
                "status": agent_response.get("status"),
                "plan": agent_response.get("plan"),
                "document": agent_response.get("document"),
            },
        }
        data["history"].append(turn)
        self._save(conversation_id, data)

    def get_context(self, conversation_id: str) -> str:
        try:
            data = self._load(conversation_id)
            if not data["history"]:
                return ""
            lines = ["Previous conversation context:"]
            for h in data["history"][-3:]:
                lines.append(f"User asked: {h['user_request']}")
                lines.append(f"Agent generated: {h['agent_response']['document']}")
            return "\n".join(lines)
        except Exception:
            return ""

    def _save(self, cid: str, data: dict):
        path = os.path.join(self.MEMORY_DIR, f"{cid}.json")
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def _load(self, cid: str) -> dict:
        path = os.path.join(self.MEMORY_DIR, f"{cid}.json")
        if os.path.exists(path):
            with open(path) as f:
                return json.load(f)
        return {"history": []}


memory = ConversationMemory()
