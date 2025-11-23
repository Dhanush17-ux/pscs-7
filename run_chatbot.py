import os
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

# UPDATED IMPORTS
from langchain_community.llms import CTransformers
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# --- SCRIPT SETUP ---
VECTOR_DB_PATH = "vector_db"
MODEL_FILE_PATH = "Phi-3-mini-4k-instruct-q4.gguf"   # ✅ Use the new fast model

# Custom prompt template for Chacha Chaudhary
prompt_template = """
Namaste! You are Chacha Chaudhary, the mascot for the Namami Gange Programme.
Your brain is as sharp as a computer. Answer the user's question based only on the
information provided below. Be friendly, wise, and encouraging.

If the information is not in the context, politely say:
"My friend, this question is outside my current knowledge about the Ganga mission."

Context: {context}
Question: {question}

Helpful Answer:
"""
PROMPT = PromptTemplate(template=prompt_template, input_variables=["context", "question"])


def create_rag_chain():
    """Sets up the entire RAG pipeline and returns the QA chain."""

    # 1. Load the LLM
    print("--- Loading Chacha Chaudhary's brain (LLM)... ---")
    print(f"Model file path: {MODEL_FILE_PATH}")

    if not os.path.exists(MODEL_FILE_PATH):
        print(f"!!! ERROR: Model file not found at '{MODEL_FILE_PATH}'")
        return None

    llm = CTransformers(
        model=MODEL_FILE_PATH,
        model_type='phi3',      # ✅ Must be phi3 for Phi-3 models
        config={'context_length': 1024},  # ✅ Reduced for speed
        max_new_tokens=150,     # ✅ Faster generation
        temperature=0.3
    )
    print("--- LLM loaded successfully. ---")

    # 2. Load the knowledge base
    print("--- Loading knowledge base (Vector DB)... ---")
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = Chroma(
        persist_directory=VECTOR_DB_PATH,
        embedding_function=embedding_function
    )
    print("--- Knowledge base loaded successfully. ---")

    # 3. Create the RAG chain
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=vector_db.as_retriever(search_kwargs={'k': 3}),
        return_source_documents=True,
        chain_type_kwargs={'prompt': PROMPT}
    )
    print("--- RAG chain created. ---")
    return qa_chain


def start_chat(qa_chain):
    """Starts an interactive console chat session."""
    print("\n\n--- Chacha Chaudhary is ready to talk! ---")
    print("Ask any question about the Namami Gange mission. Type 'exit' to end.")
    print("-" * 50)

    while True:
        user_input = input("You: ")

        if user_input.lower() in ['exit', 'quit']:
            print("Chacha Chaudhary: Goodbye! Remember to keep our rivers clean!")
            break

        response = qa_chain({'query': user_input})
        print(f"\nChacha Chaudhary: {response['result'].strip()}")

        # Show which PDF chunk answers were generated from
        print(f"\nSource Documents: {[doc.metadata.get('source', 'unknown') for doc in response['source_documents']]}\n")
        print("-" * 50)


if __name__ == "__main__":
    print("--- Chatbot script started. ---")
    chain = create_rag_chain()
    if chain:
        start_chat(chain)
    else:
        print("--- Chatbot setup failed. Please check the error messages above. ---")
