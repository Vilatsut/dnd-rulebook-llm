# D&D Knowledge Worker

This project aims to create a Large Language Model (LLM) based knowledge worker to assist with Dungeons & Dragons campaigns and rules. It leverages Retrieval-Augmented Generation (RAG) to provide comprehensive answers based on a D&D rulebook PDF.

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.12+**
*   **uv**: A fast Python package installer and resolver.
*   **Docker**: For containerizing the application.
*   **Kubernetes Cluster (Optional)**: If you plan to deploy.

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

### Gradio UI

To run the Gradio web interface locally:

```bash
python gradio_app.py
```
The Gradio UI will typically be accessible at `http://localhost:7860` (or another port if 7860 is in use). You need to change the url to point to your backend, fe. `http://localhost:8000/engines/v1`. 

### Dockerization

To run the application with docker:

```bash
docker compose up
```
Gradio UI should be available at `http://localhost:7860`

### Kubernetes Deployment

Kubernetes manifests for this application were generated using `docker compose bridge convert`. These manifests can be found in the `k8s/` directory and can be applied to a Kubernetes cluster for deployment with `kubectl apply -f ./k8s/overlays/desktop`.

### Inference Engine with Docker Model Runner

This project utilizes a Docker Model Runner as the inference engine. To change the backend model just change the "model" attribute in the docker-compose.yml. If used with kubernetes, generate new files after with the `docker compose bridge convert` commmand.
