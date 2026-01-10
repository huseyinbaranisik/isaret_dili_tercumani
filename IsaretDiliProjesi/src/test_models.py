import google.generativeai as genai
import os

api_key = os.environ.get("GOOGLE_API_KEY", "YOUR_API_KEY_HERE")

try:
    genai.configure(api_key=api_key)
    print("Listing available models:")
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"- {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
