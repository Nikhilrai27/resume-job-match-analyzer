from openai import OpenAI

from careermatch_ai.infrastructure.llm.base import LLMClient


class GroqClient(LLMClient):
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile") -> None:
        self._client = OpenAI(api_key=api_key, base_url="https://api.groq.com/openai/v1")
        self._model = model

    def generate(self, system_prompt: str, user_prompt: str, json_mode: bool = True) -> str:
        kwargs = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.1,
        }
        if json_mode:
            kwargs["response_format"] = {"type": "json_object"}
        response = self._client.chat.completions.create(**kwargs)
        return response.choices[0].message.content or ""
