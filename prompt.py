# --- Prompt builder ---
prompt_template = """
You are a smart AI assistant. Below is some (but not all) information about a group of students.

RULES:
- Only use the information provided.
- Answer specifically for the person being asked about; do not use information about others.
- If information is similar or can be reasonably inferred, confirmation is allowed.
- No need to repeat the question.
- Keep the answer short and focused. Do not elaborate unnecessarily.
- If there is not enough information, simply answer: "Not enough information to answer the question."

INFORMATION (context):
{chr(10).join('- ' + c for c in context_data)}

QUESTION:
{question}

📤 CÂU TRẢ LỜI:
"""

#--- PROMPT ENTITIES QUESTION ---
prompt_entities = """
You are an AI assistant for entity extraction.

TASK:
Extract the main entities mentioned in the input text. These can include people, objects, animals, places, concepts, organizations, or any other clearly defined subject.

REQUIREMENTS:
- Return a list of the most central or prominent entities.
- All entity names must be in **lowercase**.
- Do **not** include explanations, formatting, or any extra content.
- Return an empty list if no relevant entity is found.

OUTPUT FORMAT:
A JSON-style list of lowercase entity names. Example:
["entity1", "entity2", "entity3"]

INPUT:
{text}

OUTPUT:
"""


#--- PROMPT KEYWORD QUESTION ---
prompt_keyword = """
You are an AI assistant for keyword extraction.

TASK:
Extract the top {top_n} most important keywords from the input text.

REQUIREMENTS:
- Return exactly {top_n} keywords.
- All keywords must be in **lowercase**.
- Do **not** include explanations, formatting, or any extra content.
- Focus on the most relevant or central words.
- Avoid stopwords and uninformative words.

OUTPUT FORMAT:
A JSON-style list of lowercase keywords. Example:
["keyword1", "keyword2", "keyword3"]

INPUT:
{text}

OUTPUT:
"""