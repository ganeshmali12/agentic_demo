import json
import re


def extract_json(text: str) -> dict:
    text = text.strip()

    code_block = re.search(
        r"```(?:json)?\s*([\s\S]*?)```", text, re.IGNORECASE
    )
    if code_block:
        text = code_block.group(1).strip()

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON object found in response.")

    raw = match.group()

    raw = re.sub(r",\s*}", "}", raw)
    raw = re.sub(r",\s*\]", "]", raw)

    return json.loads(raw)
