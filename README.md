# D&D Knowledge Worker

This project is a Dungeons & Dragons knowledge worker that uses a Retrieval-Augmented Generation (RAG) model to answer questions about the D&D rulebook.

## Project Overview

The project is a complete RAG application with a user-friendly interface for querying a D&D rulebook, designed for both local and remote development and deployment. It consists of the following main components:

### 1. Data Preparation

The knowledge base is built from the `dragons_of_stormwreck_isle.pdf` file. The process involves:

*   **Extraction:** Text, images, and tables are extracted from the PDF into a markdown file (`resources/dnd_rules_markdown.md`) using LlamaParse (`backend/scripts/extract_data.py`).
*   **Embedding:** The markdown content is chunked, converted into vector embeddings using a HuggingFace sentence transformer, and stored in a ChromaDB vector store (`backend/scripts/process_data.py`).

### 2. Backend (FastAPI)

The backend is a FastAPI application (`backend/backend.py`) that exposes an `/invoke` endpoint. When a user query is received, the backend:

1.  Generates an embedding for the query.
2.  Performs a similarity search in the ChromaDB vector store to find relevant context.
3.  Uses a Large Language Model (LLM) provided by a seperate inference endpoint to generate a response based on the query and the retrieved context.

The inference engine is powered by a Docker Model Runner, configured in `docker-compose.yml`.

### 3. Frontend (Gradio)

The user interface is a Gradio chat interface (`frontend/frontend.py`) that provides a simple chat window for users to ask questions. The Gradio app communicates with the FastAPI backend to get the answers and streams the response to the user.

### 4. Containerization and Deployment

The project is containerized using Docker for both local development and deployment:

*   `backend/Dockerfile` and `frontend/Dockerfile` are used to build the images for the FastAPI backend and Gradio frontend.
*   `docker-compose.yml` is used to orchestrate the local deployment of the application, including the `ai_runner` service for the LLM.
*   Kubernetes manifests, generated using `docker compose bridge convert`, are available in the `k8s/` directory for deployment to a Kubernetes cluster.

## Project Structure

```
dnd-rulebook-llm/
├── .github/workflows/ci.yml
├── backend/
│   ├── scripts/
│   │   ├── extract_data.py
│   │   └── process_data.py
│   ├── Dockerfile
│   ├── backend.py
│   └── pyproject.toml
├── frontend/
│   ├── Dockerfile
│   ├── frontend.py
│   └── pyproject.toml
├── resources/
│   ├── dragons_of_stormwreck_isle.pdf
│   └── dnd_rules_markdown.md
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

*   Python 3.12+
*   `uv` (Python package installer)
*   Docker with Docker Model Runner 
    (see https://docs.docker.com/ai/model-runner/)

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/vilatsut/dnd-rulebook-llm.git
    cd dnd-rulebook-llm
    ```

2.  **API Keys:**
    Create a `.env` file in the root directory and add your LlamaParse API key:
    ```
    LLAMA_CLOUD_API_KEY="your_llamaparse_api_key_here"
    ```

3.  **LangSmith for Logging:**
    This project uses [LangSmith](https://smith.langchain.com/) for logging and tracing. To enable it, add the following environment variables to your `.env` file:
    ```
    LANGCHAIN_API_KEY="your_langchain_api_key_here"
    LANGCHAIN_TRACING=true
    LANGSMITH_PROJECT="your_project_name"
    LANGSMITH_ENDPOINT=https://api.smith.langchain.com 
    ```

### Data Preparation

1.  **Extract data from PDF:**
    ```bash
    cd backend
    python -m scripts.extract_data
    ```

2.  **Process and embed data:**
    ```bash
    python -m scripts.process_data
    ```

## Usage

### Local Development

1.  **Install dependencies for backend and frontend:**
    ```bash
    cd backend
    uv sync
    cd ../frontend
    uv sync
    cd ..
    ```

2.  **Run the backend:**
    ```bash
    cd backend
    uvicorn backend:app --host 0.0.0.0 --port 8000
    ```

3.  **Run the frontend:**
    ```bash
    cd frontend
    python frontend.py
    ```
    The Gradio UI will be available at `http://localhost:7860`.

4. **Run the model**
    ```bash
    docker model run smollm2 -d  # Or the model of your choice
    ```

### Docker

To run the entire application with Docker Compose:
```bash
docker compose up
```
The Gradio UI will be available at `http://localhost:7860`.

### Kubernetes

The project includes Kubernetes manifests in the `k8s` directory. These can be used to deploy the application to a Kubernetes cluster.

## CI/CD

The project uses GitHub Actions for CI/CD. The workflow in `.github/workflows/ci.yml` performs the following:

*   Lints the code using Ruff.
*   Builds and pushes Docker images for the backend and frontend to a container registry.

## Limitations

The model used (ai/smollm2, 360 million parameters) does not have the context windows required for these kinds of task, but was used for the reason of running the model locally. As the code uses the OpenAi api endpoint, using another model is simply a drop-in replacement.

## A demo run of the knowledge worker with a 360 million ai/smollm2 model. You can see the context retrieved on the right.
https://github.com/user-attachments/assets/f34b1038-5027-4d13-a8c4-2a850b158a6f



