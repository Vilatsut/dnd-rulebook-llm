import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app import config

def query_chroma_db(query: str):
    """Performs a similarity search on ChromaDB and prints the results."""
    print(f"Performing similarity search for query: '{query}'")

    load_dotenv()
    db_name = os.getenv("CHROMA_DB_PERSIST_DIRECTORY", config.CHROMA_DB_PERSIST_DIRECTORY)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Load ChromaDB
    vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)

    # Perform similarity search
    results = vectorstore.similarity_search(query)

    print("\n--- Search Results ---")
    for i, doc in enumerate(results):
        print(f"Result {i+1}:\n{doc.page_content}\n")

def main():
    queries = [
        "What is a saving throw?",
    ]

    for q in queries:
        query_chroma_db(q)

if __name__ == "__main__":
    main()
