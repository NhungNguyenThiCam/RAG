from prompt import prompt_template  
import requests
from Embedding_Store.Model import *
import os
from dotenv import load_dotenv
# load env
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, 'config', '.env')

if os.path.exists(dotenv_path):
    print(f"Loading env file from: {dotenv_path}")
    # Tải các biến môi trường từ file .env được chỉ định
    load_dotenv(dotenv_path=dotenv_path) 
else:
    print(f"warning: file .env at {dotenv_path} not found")
    

embedding_model = initialize_embedding_model(os.getenv("MODEL_NAME_EMBED"))

# --- Gọi mô hình llama3.2 qua Ollama ---
def call_ollama_llama32(question, context_chunks):
    try:
        # print("context:", context_chunks)
        prompt = prompt_template.format(
            subject="about programing java",
            information=(context_chunks),
            question=question
        )
        
        payload = {
            "model": "llama3.2:3b",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        result = response.json()
        return result['response'].strip()
    except Exception as e:
        print("❌ Error when call ollama:", e)
        return "Cannot connect to the model. Please check again."