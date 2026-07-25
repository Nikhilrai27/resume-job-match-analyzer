from google import genai
from google.genai import types

from careermatch_ai.infrastructure.llm.base import LLMClient


class GeminiClient(LLMClient):
    def __init__(self, api_key: str, model: str = "gemini-2.0-flash") -> None:
        self._client = genai.Client(api_key=api_key)
        self._model = model

    def generate(self, system_prompt: str, user_prompt: str, json_mode: bool = True) -> str:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"
        config_kwargs = {}
        if json_mode:
            config_kwargs["response_mime_type"] = "application/json"
        response = self._client.models.generate_content(
            model=self._model,
            contents=full_prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        return response.text
