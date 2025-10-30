This folder is for a project to create a Large Language Model (LLM) to assist with Dungeons & Dragons campaigns and rules. The goal is to create a knowledge worker for D&D.

## Development Environment

The project uses a virtual environment located in the `.venv` directory. Packages are managed with `uv`. To install or update dependencies, run the following command:

```bash
uv sync
```

## Plan for Creating the D&D Knowledge Worker

Here is a high-level plan to create a dockerized knowledge worker for D&D and deploy it with Kubernetes and llm-d.

### Step 1: Data Preparation - The Knowledge Base

The first step is to extract the text, images, and tables from the "dragons_of_stormwreck_isle.pdf" file to create a comprehensive knowledge base. This has been completed using the following tools and process:

1.  **Extraction with LlamaParse:** The PDF was parsed using LlamaParse (a cloud-based service), which extracted text, images, and tables into a markdown format. The extracted content is saved in `data/dnd_rules_markdown.md`.
2.  **Chunking and Embedding:** The markdown content was then split into smaller, manageable chunks using `RecursiveCharacterTextSplitter` from LangChain. These chunks were then converted into vector embeddings using `SentenceTransformerEmbeddings`.
3.  **Vector Store:** The embeddings were stored in ChromaDB, located in the `chroma_langchain_db` directory.

This process ensures that all relevant information from the PDF is available in a searchable and retrievable format for the RAG application.

### Step 2: Create the RAG (Retrieval-Augmented Generation) Application

Instead of fine-tuning a model, a more efficient approach is to use RAG. Here's how it works:

1.  **Vector Embeddings:** You'll use a pre-trained model to generate vector embeddings for each chunk of your D&D rules text, image captions, and tables. These embeddings are numerical representations of the text.
2.  **Vector Store:** You'll store these embeddings in a vector database. This project uses ChromaDB, and the database is stored in the `chroma_langchain_db` directory. This allows for very fast searching of the most relevant text chunks based on a user's query.
3.  **API Server:** You'll create a simple API server. This project uses FastAPI, and the main application is in `app/main.py`. When a user sends a question to the API:
    *   The API will generate an embedding for the user's question.
    *   It will then search the vector database to find the most similar (i.e., relevant) text chunks from your D&D rulebook.
    *   Finally, it will pass the user's original question and the relevant text chunks to an LLM to generate a comprehensive answer.

### Step 3: Dockerize the Application

To make your application portable and scalable, you'll containerize it using Docker. This involves writing a `Dockerfile` that specifies the following:

*   The base Python image to use.
*   The necessary dependencies to install (FastAPI, a vector database library, etc.).
*   The application code to copy into the image.
*   The command to run when the container starts (e.g., `uvicorn main:app --host 0.0.0.0 --port 80`).

### Step 4: Deploy to Kubernetes with llm-d

`llm-d` is a framework for serving LLMs on Kubernetes. It's designed to handle the complexities of running large models in a distributed environment. Here's how it fits into your deployment:

1.  **Kubernetes Cluster:** You'll need a Kubernetes cluster with GPU nodes.
2.  **`llm-d` Installation:** You'll deploy `llm-d` to your cluster. It typically runs as a set of services that manage the LLM inference process.
3.  **Deployment Manifests:** You'll create Kubernetes `Deployment` and `Service` manifests for your RAG application container (from Step 3).
4.  **Connecting to `llm-d`:** Your RAG application will be configured to communicate with the `llm-d` service for the final step of generating an answer. Instead of calling a local LLM, it will make an API call to the `llm-d` endpoint, passing the prompt (which includes the user's question and the retrieved text chunks).

This setup allows you to scale your RAG application and the LLM inference service independently, and `llm-d` will handle the efficient utilization of the GPU resources in your cluster.