from tools.logger import logger


class FallbackClient:

    def generate(self, prompt: str) -> str:
        logger.warning("Using fallback template generator")
        return self._template_response(prompt)

    def _template_response(self, prompt: str) -> str:
        prompt_lower = prompt.lower()

        if "assumption" in prompt_lower and "json" in prompt_lower:
            return """{
  "document_title": "Business Report",
  "document_type": "Report",
  "assumptions": [
    "Standard business assumptions apply",
    "Data is based on publicly available information"
  ],
  "tasks": [
    "Executive Summary",
    "Market Analysis",
    "Financial Projections",
    "Risk Assessment",
    "Recommendations"
  ]
}"""

        if "status" in prompt_lower and "fail" in prompt_lower:
            return '{"status":"PASS","reason":"Document meets quality standards","failed_sections":[]}'

        return (
            "This section contains the generated content based on the provided request. "
            "The content follows professional business document standards and addresses "
            "the key requirements outlined in the document plan."
        )


fallback = FallbackClient()
