# D&D Knowledge Worker

This project is a Dungeons & Dragons knowledge worker that uses a Retrieval-Augmented Generation (RAG) model to answer questions about the D&D rulebook.

## Project Overview

The project is a complete RAG application with a user-friendly interface for querying a D&D rulebook, designed for both local development and deployment. It consists of the following main components:

### 1. Data Preparation

The knowledge base is built from the `dragons_of_stormwreck_isle.pdf` file. The process involves:

*   **Extraction:** Text, images, and tables are extracted from the PDF into a markdown file (`data/dnd_rules_markdown.md`) using LlamaParse (`scripts/extract_data.py`).
*   **Embedding:** The markdown content is chunked, converted into vector embeddings using a HuggingFace sentence transformer, and stored in a ChromaDB vector store (`scripts/process_data.py`).

### 2. Backend (FastAPI)

The backend is a FastAPI application (`app/main.py`) that exposes an `/invoke` endpoint. When a user query is received, the backend:

1.  Generates an embedding for the query.
2.  Performs a similarity search in the ChromaDB vector store to find relevant context.
3.  Uses a Large Language Model (LLM) to generate a response based on the query and the retrieved context.

The inference engine is powered by a Docker Model Runner, configured in `docker-compose.yml`.

### 3. Frontend (Gradio)

The user interface is a Gradio chat interface (`gradio_app.py`) that provides a simple chat window for users to ask questions. The Gradio app communicates with the FastAPI backend to get the answers and streams the response to the user.

### 4. Containerization and Deployment

The project is containerized using Docker for both local development and deployment:

*   `Dockerfile` and `gradio.Dockerfile` are used to build the images for the FastAPI backend and Gradio frontend.
*   `docker-compose.yml` is used to orchestrate the local deployment of the application, including the `ai_runner` service for the LLM.
*   Kubernetes manifests, generated using `docker compose bridge convert`, are available in the `k8s/` directory for deployment to a Kubernetes cluster.
