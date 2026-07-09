from google import genai
from google.genai import types

from src.config.settings import settings
from src.llm.base import BaseLLM


class GeminiLLM(BaseLLM):
    """
    Gemini implementation of the BaseLLM interface.
    """

    def __init__(self):

        self.client = genai.Client(
            api_key=settings.GEMINI_API_KEY,
        )

        self.model = settings.MODEL_NAME

    def generate(
        self,
        prompt: str,
        system_prompt: str = "",
        json_output: bool = False,
    ) -> str:

        full_prompt = prompt

        if system_prompt:

            full_prompt = (
                f"{system_prompt}\n\n"
                f"{prompt}"
            )

        config = types.GenerateContentConfig(
            temperature=settings.TEMPERATURE,
        )

        if json_output:

            config.response_mime_type = "application/json"

        response = self.client.models.generate_content(
            model=self.model,
            contents=full_prompt,
            config=config,
        )

        return response.text