from underthesea import pos_tag
from model import kw_model

# --- Extract keywords with POS filtering ---
def extract_keywords_from_question(question, top_n=5):
    try:
        tags = pos_tag(question)
        filtered = " ".join(word for word, tag in tags if tag in ['N', 'Np', 'Nc', 'V'])
        keywords = kw_model.extract_keywords(filtered, keyphrase_ngram_range=(1, 3), stop_words=None, top_n=top_n)
        return [kw for kw, _ in keywords]
    except Exception:
        return []

# --- Extract named entities (names, objects) ---
def extract_entities(question):
    try:
        tagged = pos_tag(question)
        return [word.lower() for word, tag in tagged if tag in ["Np", "N", "Nc"]]
    except:
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


