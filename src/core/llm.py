from typing import Literal
from pydantic import BaseModel
from google import genai
from google.genai import types
from src.settings import SETTINGS


class GeminiClient:
    """Handles low-level API calls to Google Gemini."""
    def __init__(self) -> None:
        self.client = genai.Client(api_key=SETTINGS.gemini_api_key)

    def generate(self, prompt: "Prompt") -> BaseModel:
        response = self.client.models.generate_content(
            model=prompt.model,
            contents=prompt.content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=prompt.response_schema,
            ),
        )
        return prompt.response_schema.model_validate_json(response.text)


class Prompt(BaseModel):
    provider: Literal["Gemini"] = "Gemini"
    model: str
    content: str
    response_schema: type[BaseModel]

    def generate(self) -> BaseModel:
        """Executes the prompt using the specified provider's client."""
        if self.provider == "Gemini":
            return GeminiClient().generate(self)

        raise ValueError(f"Unsupported provider: {self.provider}")
