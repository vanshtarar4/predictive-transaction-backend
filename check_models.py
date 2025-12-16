import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
URL = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

def list_models():
    try:
        response = requests.get(URL)
        if response.status_code == 200:
            models = response.json()
            print("Available Models:")
            for m in models.get('models', []):
                if 'generateContent' in m['supportedGenerationMethods']:
                    print(f"- {m['name']}")
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    list_models()
