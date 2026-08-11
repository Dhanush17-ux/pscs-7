# Namami Gange Chatbot (pscs-7)

An intelligent, domain-specific Retrieval-Augmented Generation (RAG) chatbot engineered to provide precise information regarding the **Namami Gange Mission**—an Integrated Conservation Mission launched by the Government of India to curb pollution, conserve, and rejuvenate the National River Ganga.

## 🚀 Key Architectural Features
* **Information Retrieval System:** Bounded domain architecture preventing hallucination by anchoring language model generation to authentic project documentation.
* **Vector Embeddings Pipeline:** Implements structural chunking and vector storage to optimize factual lookup speed and precision.
* **Custom Chat Interface:** Built with a user-friendly conversational interface to cleanly display structured data responses.

## 🛠️ File Structure & Ecosystem
* `build_database.py`: Orchestrates text loading, document parsing, processing, and vectorization pipelines.
* `vector_db/`: Local vector database directory housing indices and embeddings for context retrieval.
* `chat_ui.py`: Manages front-end application elements, custom background rendering, and conversation flows.
* `main.py` / `run_chatbot.py`: Application entry points initiating vector configuration, context injections, and execution loops.

## 💻 Tech Stack
* **Language:** Python
* **NLP & Knowledge Retrieval:** Vector Database Indexing, Similarity Search, Text Segmentation
* **Interface Layout:** UI components utilizing custom graphic assets (`avatar.png`, `background.png`)
