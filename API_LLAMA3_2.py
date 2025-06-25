import torch
import tempfile
import os
import requests
import json
import pickle
from prompt import prompt_template
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from fastapi import FastAPI, UploadFile, File, Form
from Embedding_Store.Model import *
from fastapi.responses import JSONResponse
from sentence_transformers import SentenceTransformer, util
from model import embedding_model
from utils import extract_keywords_from_question, extract_entities, rerank_contexts_with_keywords

# load env
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, 'config', '.env')

if os.path.exists(dotenv_path):
    print(f"Loading env file from: {dotenv_path}")
    # Tải các biến môi trường từ file .env được chỉ định
    load_dotenv(dotenv_path=dotenv_path) 
else:
    print(f"warning: file .env at {dotenv_path} not found")

app = FastAPI()


@app.post("/answer")
async def rag_api(question: str = Form(None), audio: UploadFile = File(None)):
    if not question and not audio:
        return JSONResponse(status_code=400, content={"error": "No question or audio provided"})

    if question:
        # extract keywords and entities from question
        keywords = extract_keywords_from_question(question)
        entities = extract_entities(question)

        # --- Embedding input ---
        model = SentenceTransformer(embedding_model, device='cuda' if torch.cuda.is_available() else 'cpu')
        embeddings_question = model.encode(question)
        
        # rerank contexts
        output_database = []  # This should be your context chunks
        similarities = []  # This should be the similarities for each context chunk
        reranked_indices = rerank_contexts_with_keywords(output_database, similarities, keywords, entities, question, k=3)
        
        return {"type": "text", "content": output}

    if audio:
        # xử lý tệp âm thanh
        response = requests.post("http://0.0.0.0:8000/STT/", files={"file": audio.file})
        data = response.json()
        output = data["output_text"]
        
        return {"type": "text", "content": output}
    

# uvicorn API_LLAMA3_2:app --host 0.0.0.0 --port 4096 --reload

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )