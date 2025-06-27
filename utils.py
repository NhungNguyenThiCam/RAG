from model import kw_model
import requests,os
from prompt import prompt_entities,prompt_keyword
 
# --- Extract keywords with POS filtering ---
def extract_keywords_from_question(question, top_n=5):
    url = os.getenv("API_GEMINI_ENTITIES")
    prompt = prompt_keyword.format(top_n=top_n, text=question)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json=payload).json()
        text = response['candidates'][0]['content']['parts'][0]['text']
        return [i.strip().lower() for i in text.replace('[','').replace(']','').replace('"','').split(',') if i.strip()]
    except Exception as e:
        print(f"[Keyword Extraction Error] {e}")
        return []

# --- Extract named entities (names, objects) ---
def extract_entities(question):
    url = os.getenv("API_GEMINI_ENTITIES")
    prompt = prompt_entities.format(text=question)
    try:
        response = requests.post(url, headers={"Content-Type": "application/json"}, json={
            "contents": [{"parts": [{"text": prompt}]}]
        }).json()
        text = response['candidates'][0]['content']['parts'][0]['text']
        # Làm sạch như trong extract_keywords_from_question
        return [i.strip().lower() for i in text.replace('[','').replace(']','').replace('"','').replace("'", '').split(',') if i.strip()]
    except Exception as e:
        print(f"[Entity extraction error] {e}")
        return []




# --- Rerank contexts ---
def rerank_contexts_with_keywords(output_database, similarities, keywords, entities, question, weight=0.8, k=3):
    question_lower = question.lower()
    scores = []

    for i, chunk in enumerate(output_database):
        try:
            chunk_lower = chunk.lower()
            score = similarities[i] if i < len(similarities) else 0.0

            keyword_bonus = sum(1.0 for kw in keywords if kw.lower() in chunk_lower)

            # Only bonus if entity is relevant to question
            entity_bonus = 0.0
            for ent in entities:
                if ent in chunk_lower and ent in question_lower:
                    entity_bonus += 2.0

            final_score = score + weight * (keyword_bonus + entity_bonus)
            scores.append((final_score, i))
        except Exception:
            scores.append((0.0, i))

    scores.sort(reverse=True)
    return [i for _, i in scores[:k]]
