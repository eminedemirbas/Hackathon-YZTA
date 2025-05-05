import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ GEMINI_API_KEY bulunamadı.")
    exit()

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-pro-001")

prompt = "türkçe biliyor musun? türkçe cevap ver."

response = model.generate_content(prompt)

print("🧠 Gemini'nin Cevabı:\n")
print(response.text)
