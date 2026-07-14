from agent.executor import Executor
from agent.planner import Planner
from agent.reflection import Reflection

from tools.document_tool import document_tool
from tools.logger import logger
from utils.memory import memory


class AutonomousAgent:

    def __init__(self):
        self.planner = Planner()
        self.executor = Executor()
        self.reviewer = Reflection()

    def run(self, request: str, conversation_id: str = ""):
        logger.info("Agent Started")

        if not conversation_id:
            conversation_id = memory.create_conversation()
            logger.info(f"New conversation: {conversation_id}")
        else:
            logger.info(f"Continuing conversation: {conversation_id}")

        memory_context = memory.get_context(conversation_id)

        plan = self.planner.create_plan(request, memory_context)

        sections = self.executor.execute(plan)

        review = self.reviewer.review(sections)

        if review["status"] == "FAIL":
            logger.warning("Reflection Failed - regenerating failed sections")

            for section in review.get("failed_sections", []):
                logger.info(f"Regenerating: {section}")
                sections[section] = self.executor.regenerate_section(
                    plan, section
                )

            review = self.reviewer.review(sections)

        filepath = document_tool.create_document(plan, sections)

        response = {
            "status": "success",
            "plan": plan["tasks"],
            "assumptions": plan["assumptions"],
            "review": review,
            "document": filepath,
            "conversation_id": conversation_id,
        }

        memory.add_turn(conversation_id, request, response)

        logger.info("Document Generated Successfully")
        return response
