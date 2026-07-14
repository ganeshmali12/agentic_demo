import google.generativeai as genai

from config import config
from tools.fallback_client import fallback
from tools.logger import logger

genai.configure(api_key=config.GEMINI_API_KEY)


class GeminiClient:

    def __init__(self):
        self.model = None
        self._init_model()

    def _init_model(self):
        try:
            self.model = genai.GenerativeModel(config.MODEL_NAME)
            self.model.generate_content("test")
        except Exception as e:
            logger.warning(f"Gemini init failed: {e}. Will use fallback.")
            self.model = None

    def generate(self, prompt: str) -> str:
        if self.model is None:
            return fallback.generate(prompt)

        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            logger.warning(f"Gemini API error: {e}. Falling back.")
            return fallback.generate(prompt)


gemini = GeminiClient()
