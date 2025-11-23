import os
from langchain.text_splitter import RecursiveCharacterTextSplitter
# UPDATED IMPORTS based on the warnings
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

# Define the folder containing PDFs and the persistent DB path
PDFS_FOLDER_PATH = "docs"
VECTOR_DB_PATH = "vector_db"

def build_vector_database():
    """
    Reads all PDFs from a folder, splits them into chunks,
    creates embeddings, and stores them in a persistent ChromaDB.
    """
    print("--- Starting to build the vector database from PDF files... ---")

    if not os.path.exists(PDFS_FOLDER_PATH):
        print(f"Error: The folder '{PDFS_FOLDER_PATH}' does not exist.")
        return

    documents = []
    for file in os.listdir(PDFS_FOLDER_PATH):
        if file.endswith('.pdf'):
            pdf_path = os.path.join(PDFS_FOLDER_PATH, file)
            print(f"LOADING FILE: {pdf_path}")
            try:
                loader = PyPDFLoader(pdf_path)
                documents.extend(loader.load())
            except Exception as e:
                print(f"  -> ERROR loading {pdf_path}: {e}")
                continue # Skip to the next file if one is broken

    if not documents:
        print("\n--- SCRIPT FINISHED ---")
        print("REASON: No PDF documents were found or successfully loaded in the 'docs' folder.")
        print("Please make sure your PDF files are placed inside the 'docs' folder.")
        return

    print(f"\n--- Found {len(documents)} pages. Splitting documents into chunks... ---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunked_documents = text_splitter.split_documents(documents)

    print(f"--- Created {len(chunked_documents)} chunks. Creating embeddings... (This might take a while) ---")
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"--- Storing chunks in the vector database at: {VECTOR_DB_PATH} ---")
    vector_db = Chroma.from_documents(
        documents=chunked_documents,
        embedding=embedding_function,
        persist_directory=VECTOR_DB_PATH
    )
    
    vector_db.persist()
    print("\n--- VECTOR DATABASE BUILT SUCCESSFULLY! ---")
    print("You can now run the '2_run_chatbot.py' script.")

if __name__ == "__main__":
    build_vector_database()