from prompt import prompt_template  
import requests
from keybert import KeyBERT
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
kw_model = KeyBERT(model=embedding_model)

# --- Gọi mô hình llama3.2 qua Ollama ---
def call_ollama_llama32(question, k=3):
    try:
        prompt = prompt_template
        payload = {
            "model": "llama3.2",
            "prompt": prompt,
            "stream": False
        }

        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        result = response.json()
        return result['response'].strip()
    except Exception as e:
        print("❌ Lỗi khi gọi Ollama API:", e)
        return "Không thể kết nối với mô hình. Vui lòng kiểm tra lại."