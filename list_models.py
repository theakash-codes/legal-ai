# list_models.py

import google.generativeai as genai
import os
from dotenv import load_dotenv

print("Attempting to load API key and list models...")

try:
    # Load the API key from your .env file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        print("!!! ERROR: GEMINI_API_KEY not found in .env file.")
    else:
        genai.configure(api_key=api_key)
        
        print("\n--- Available Models ---")
        # List all models that support the 'generateContent' method
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(model.name)
        print("------------------------\n")

except Exception as e:
    print(f"!!! An error occurred: {e}")