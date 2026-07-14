from prompts.writer_prompt import WRITER_PROMPT
from tools.gemini_client import gemini
from tools.logger import logger


class Executor:

    def execute(self, plan: dict):

        logger.info("Executor Started")

        sections = {}

        assumptions = "\n".join(plan["assumptions"])

        for task in plan["tasks"]:

            logger.info(f"Executing: {task}")

            prompt = WRITER_PROMPT.format(
                title=plan["document_title"],
                doc_type=plan["document_type"],
                task=task,
                assumptions=assumptions
            )

            content = gemini.generate(prompt)

            sections[task] = content

        logger.info("All Tasks Completed")

        return sections

    def regenerate_section(self, plan: dict, section_name: str):

        logger.info(f"Regenerating Section: {section_name}")

        assumptions = "\n".join(plan["assumptions"])

        prompt = WRITER_PROMPT.format(
            title=plan["document_title"],
            doc_type=plan["document_type"],
            task=section_name,
            assumptions=assumptions
        )

        return gemini.generate(prompt)