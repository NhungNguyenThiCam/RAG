from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer, util
import torch
import tempfile
import os
import requests
import json

app = FastAPI()

@app.post("/answer")
async def rag_api(question: str = Form(None), audio: UploadFile = File(None)):
    if not question and not audio:
        return JSONResponse(status_code=400, content={"error": "No question or audio provided"})

    if question:
        # xử lý câu hỏi văn bản
        answer = generate_answer(question)
        return {
            "question": question,
            "answer": answer
        }

    if audio:
        response = requests.post("http://0.0.0.0:8000/STT/", files={"file": audio.file})
        data = response.json()
        output = data["output_text"]
        # xử lý tệp âm thanh
        return {"type": "text", "content": output}
    

# uvicorn API_LLAMA3_2:app --host 0.0.0.0 --port 4096 --reload

# if __name__ == "__main__":
#     uvicorn.run(
#         "main:app",
#         host="0.0.0.0",
#         port=8000,
#         reload=True
#     )