from prompts.planner_prompt import PLANNER_PROMPT
from tools.gemini_client import gemini
from tools.logger import logger
from utils.json_parser import extract_json


class Planner:

    MAX_RETRIES = 3

    def create_plan(self, request: str, memory_context: str = ""):
        memory_block = ""
        if memory_context:
            memory_block = f"Conversation History:\n{memory_context}"

        prompt = PLANNER_PROMPT.format(
            request=request, memory_context=memory_block
        )

        for attempt in range(self.MAX_RETRIES):
            logger.info(f"Planner Attempt {attempt+1}")

            response = gemini.generate(prompt)

            try:
                plan = extract_json(response)
                self._validate_plan(plan)
                logger.info(f"Plan Created: {plan['document_title']}")
                return plan

            except Exception as e:
                logger.warning(f"Planner attempt {attempt+1} failed: {e}")

        raise Exception("Planner failed after all retries.")

    def _validate_plan(self, plan: dict):
        required = ["document_title", "document_type", "assumptions", "tasks"]
        for key in required:
            if key not in plan:
                raise ValueError(f"Plan missing required key: {key}")
        if not isinstance(plan["tasks"], list) or len(plan["tasks"]) == 0:
            raise ValueError("Plan must have at least one task")
        if not isinstance(plan["assumptions"], list):
            plan["assumptions"] = []
