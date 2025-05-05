import os
import json
import google.generativeai as genai
from typing import Dict, Any

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

models = genai.list_models()
for model in models:
    print(model.name)

async def get_gemini_response(prompt: str) -> Dict[str, Any]:
    try:
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable is not set")

        model = genai.GenerativeModel("gemini-1.5-pro-001")
        response = model.generate_content(prompt)

        response_text = response.text
        print("🎯 GEMINI CEVABI:\n", response_text)

        if response_text.strip().startswith("{"):
            return json.loads(response_text)
        else:
            return {"raw_text": response_text}

    except Exception as e:
        raise Exception(f"Error communicating with Gemini API: {str(e)}")
