from prompts.reflection_prompt import REFLECTION_PROMPT
from tools.gemini_client import gemini
from utils.json_parser import extract_json


class Reflection:

    def review(self, sections):

        document = ""

        for heading, content in sections.items():

            document += f"\n\n## {heading}\n\n{content}"

        prompt = REFLECTION_PROMPT.format(
            document=document
        )

        response = gemini.generate(prompt)

        return extract_json(response)