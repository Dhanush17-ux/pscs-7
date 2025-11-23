import os
import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

VECTOR_DB_PATH = "vector_db"

# Connect to remote LLM (llama-server)
LLAMA_SERVER_URL = "http://127.0.0.1:8080/v1/chat/completions"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Load Vector DB
# ---------------------
def load_vector_db():
    print(">> Loading Chroma vector DB...")
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embedding_function
    )
    print(">> Vector DB loaded.")
    return db


VECTOR_DB = load_vector_db()
retriever = VECTOR_DB.as_retriever(search_kwargs={"k": 3})


# ---------------------
# Custom Chacha Prompt
# ---------------------
prompt_template = """
You are Chacha Chaudhary, mascot of the Namami Gange Programme.
Your brain works faster than a computer.

Answer the user's question using ONLY the provided context.

If the info is missing, reply:
"My friend, this question is outside my current knowledge."

Context: {context}
Question: {question}

Helpful Answer:
"""

PROMPT = PromptTemplate(
    template=prompt_template,
    input_variables=["context", "question"]
)


# ---------------------
# API Endpoints
# ---------------------

@app.get("/api/status")
def status():
    return {
        "vector_db_loaded": True,
        "llama_server_ok": True
    }


@app.post("/api/chat")
def chat(query: dict):
    try:
        question = query.get("query", "")

        if not question:
            return {"error": "Empty query"}

        # Get relevant context from vector DB
        docs = retriever.get_relevant_documents(question)
        context = "\n".join([d.page_content for d in docs])

        # Prepare LLM input
        final_prompt = PROMPT.format(context=context, question=question)

        payload = {
            "model": "model",
            "messages": [
                {"role": "user", "content": final_prompt}
            ],
            "max_tokens": 300
        }

        response = requests.post(LLAMA_SERVER_URL, json=payload)

        if response.status_code != 200:
            raise Exception(f"LLM Server Error: {response.text}")

        answer = response.json()["choices"][0]["message"]["content"]

        return {
            "answer": answer
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
