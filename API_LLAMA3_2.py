import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from typing import Union
from fastapi.responses import JSONResponse
from Embedding_Store.db import query_similar_vectors_from_pgvector, get_pgvector_store
from model import get_entities_as_string_GEMINI
from utils import get_top_k_contexts
from prompt import prompt_template

# load env
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, 'config', '.env')

if os.path.exists(dotenv_path):
    print(f"Loading env file from: {dotenv_path}")
    load_dotenv(dotenv_path=dotenv_path) 
else:
    print(f"warning: file .env at {dotenv_path} not found")

app = FastAPI()
collection_name = os.getenv("COLLECTION_NAME", "my_default_collection")
vector_store = get_pgvector_store(collection_name=collection_name)

@app.post("/answer")
async def rag_api(question: str = Form(None), audio: Union[UploadFile, str] = File(None)):
    if isinstance(audio, str) and audio == "":
        audio = None
    if not question and not audio:
        return JSONResponse(status_code=400, content={"error": "No question or audio provided"})

    if question:
        # --- Query PGVector ---
        output_database = query_similar_vectors_from_pgvector(question, vector_store, top_k=5)
        
        # rerank contexts
        similarities = []
        documents = []
        for document, score in output_database:
            documents.append(document.page_content)
            similarities.append(score)
        reranked_indices = get_top_k_contexts(documents, question, similarities, k=3)
        # print(f"Saved reranked indices to {reranked_indices}")

        output_text = get_entities_as_string_GEMINI(prompt_template, information=reranked_indices, question=question)

        return {"type": "text", "content": output_text}
    else:
        # convert speech to text
        response_stt = requests.post("http://0.0.0.0:8000/STT/", files={"file": audio.file})
        data = response_stt.json()
        output_stt = data["output_text"]
        # --- Query PGVector ---
        output_database = query_similar_vectors_from_pgvector(output_stt, vector_store, top_k=5)
        
        # rerank contexts
        similarities = []
        documents = []
        for document, score in output_database:
            documents.append(document.page_content)
            similarities.append(score)
        reranked_indices = get_top_k_contexts(documents, output_stt, similarities, k=3)

        output_text = get_entities_as_string_GEMINI(prompt_template, information=reranked_indices, question=output_stt)
        # convert text to speech
        answer_audio_base64 = requests.post("http://0.0.0.0:8001/transcribe/", data={"text_input": output_text})
        answer_audio_base64.raise_for_status() # Kiểm tra lỗi HTTP 

        # 2. Trích xuất dữ liệu JSON từ response
        tts_data = answer_audio_base64.json()

        # 3. Sử dụng đúng key là "output_sound" để lấy chuỗi base64
        final_audio_base64 = tts_data.get("output_sound")

        return {"type": "audio","audio_base64": final_audio_base64}
    

# uvicorn API_LLAMA3_2:app --host 0.0.0.0 --port 4096 --reload

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )