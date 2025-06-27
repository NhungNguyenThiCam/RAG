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