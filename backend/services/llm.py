import google.generativeai as genai
import os

# 🔐 Make sure this env variable is set
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash")

def generate_answer(question: str, context: str) -> str:
    prompt = f"""
You are a helpful assistant.
Answer the question using ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""
    print(f"DEBUG: Using model: {model.model_name}", flush=True)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"DEBUG: LLM Error: {e}", flush=True)
        raise e
