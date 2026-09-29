import os
from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
models = list(client.models.list())
for m in models:
    print(m.name)
