# D&D Knowledge Worker

This project is a Dungeons & Dragons knowledge worker that uses a Retrieval-Augmented Generation (RAG) model to answer questions about the D&D rulebook.

## Project Overview

The project is a complete RAG application with a user-friendly interface for querying a D&D rulebook, designed for both local development and deployment. It consists of a FastAPI backend, a Gradio frontend, and data preparation scripts.

## Development Setup

### Prerequisites

*   Python 3.12+
*   `uv` (Python package installer)
*   Docker

### Installation

1.  Clone the repository.
2.  Install dependencies for both backend and frontend:
    ```bash
    cd backend
    uv sync
    cd ../frontend
    uv sync
    cd ..
    ```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
LLAMA_CLOUD_API_KEY="your_llamaparse_api_key_here"
LANGCHAIN_API_KEY="your_langchain_api_key_here"
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT="your_project_name"
```

## Data Preparation

1.  **Extract data from PDF:**
    ```bash
    cd backend
    python -m scripts.extract_data
    ```

2.  **Process and embed data:**
    ```bash
    python -m scripts.process_data
    ```

## Running the Application

### Local Development

1.  **Run the backend:**
    ```bash
    cd backend
    uvicorn backend:app --host 0.0.0.0 --port 8000
    ```

2.  **Run the frontend:**
    ```bash
    cd frontend
    python frontend.py
    ```

### Docker

To run the application with Docker Compose:
```bash
docker compose up
```

## CI/CD

The project uses a GitHub Actions workflow (`.github/workflows/ci.yml`) to lint the code with Ruff and to build and push Docker images for the backend and frontend.