import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


class GeminiClient:

    def __init__(self):

        load_dotenv(
            Path(__file__).resolve().parents[2] / ".env"
        )

        api_key = os.getenv(
            "GEMINI_API_KEY",
        )

        print("Gemini Key Loaded:", api_key is not None)

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable not found."
            )

        self.client = genai.Client(
            api_key=api_key,
        )

    def generate(
        self,
        prompt: str,
    ) -> str:

        models = [
            "gemini-flash-lite-latest",
            "gemini-3.5-flash-lite",
            "gemini-3.6-flash",
            "gemini-3.5-flash",
            "gemini-2.5-flash",
        ]

        last_exception = None

        for model in models:

            try:

                response = self.client.models.generate_content(
                    model=model,
                    contents=prompt,
                )

                return response.text.strip()

            except Exception as e:

                print(f"Model {model} failed.")

                last_exception = e

        raise last_exception
