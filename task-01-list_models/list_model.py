from google.ai import generativelanguage_v1beta as genai
from google.ai.generativelanguage_v1beta.services import model_service
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env!")

# Pass API key explicitly
client = model_service.ModelServiceClient(
    client_options={"api_key": api_key}
)

# List available models
print("Available models:")
for model in client.list_models().models:
    print(model.name)
