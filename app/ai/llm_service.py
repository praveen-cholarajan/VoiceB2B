import os
import re

from openai import OpenAI



class LLMService:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        print("[OK] OpenAI client initialized.")

    def generate(self, messages):
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_completion_tokens=120,
        )

        answer = response.choices[0].message.content or ""
        answer = self.clean_response(answer)

        print("\n========== RESPONSE ==========\n")
        print(answer)

        return answer

    def clean_response(self, text: str):
        if not text:
            return ""

        text = text.replace("```json", "")
        text = text.replace("```", "")

        text = re.sub(r"^assistant\s*:\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"^assistant\s*", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text.strip()
