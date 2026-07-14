REFLECTION_PROMPT = """
You are an AI Quality Reviewer.

Review the following document for:
1. Completeness - Are all required sections present and substantive?
2. Coherence - Does the document flow logically?
3. Professionalism - Is the tone and language appropriate for a business document?
4. Relevance - Does the content match the document type and title?

Return ONLY valid JSON.

{{
    "status": "PASS or FAIL",
    "reason": "Brief explanation of the assessment",
    "failed_sections": []
}}

Document:
{document}
"""
