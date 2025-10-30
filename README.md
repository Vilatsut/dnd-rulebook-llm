# D&D Knowledge Worker

This project aims to create a Large Language Model (LLM) based knowledge worker to assist with Dungeons & Dragons campaigns and rules. It leverages Retrieval-Augmented Generation (RAG) to provide comprehensive answers based on a D&D rulebook PDF.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.12+**
*   **uv**: A fast Python package installer and resolver.
*   **Docker**: For containerizing the application.
*   **Kubernetes Cluster (Optional)**: If you plan to deploy with `llm-d`.
*   **llm-d (Optional)**: Framework for serving LLMs on Kubernetes.

## Setup Environment

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vilatsut/dnd-rulebook-llm.git
    cd dnd-rulebook-llm
    ```


2.  **Create the venv and install dependencies:**
    ```bash
    uv sync
    ```

## API Keys

This project requires API keys for services like LlamaParse. Create a `.env` file in the root directory of the project and add your API keys as follows:

```
LLAMAPARSE_API_KEY="your_llamaparse_api_key_here"
CHROMA_DB_PERSIST_DIRECTORY=chroma_db
```

## Data Preparation

The knowledge base is built from the `dragons_of_stormwreck_isle.pdf` file. Ensure you run these commands from the project's root directory.

1.  **Extract Data from PDF:**
    This step uses LlamaParse to extract text, images, and tables from the PDF into a markdown format.
    ```bash
    python -m scripts.extract_data
    ```
    This will generate `data/dnd_rules_markdown.md`.

2.  **Vector Embedding:**
    The extracted markdown content is then chunked, converted into vector embeddings, and stored in a ChromaDB vector store.
    ```bash
    python -m scripts.process_data
    ```
    This will create the `chroma_db` directory containing the vector database.

## Running the Application

### Local Development

To run the FastAPI application locally:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
The API will be accessible at `http://localhost:8000`.

### Dockerization

To build the Docker image for the application:

```bash
docker build -t dnd-knowledge-worker .
```

### Deployment to Kubernetes with llm-d (Advanced)

For deployment to a Kubernetes cluster using `llm-d`, refer to the `GEMINI.md` file for a high-level plan. This typically involves:

1.  Setting up a Kubernetes cluster with GPU nodes.
2.  Deploying `llm-d` to your cluster.
3.  Creating Kubernetes Deployment and Service manifests for your Dockerized RAG application.
4.  Configuring your RAG application to communicate with the `llm-d` service for LLM inference.
