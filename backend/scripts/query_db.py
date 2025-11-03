from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import config


def query_chroma_db(query: str):
    """Performs a similarity search on ChromaDB and prints the results."""
    print(f"Performing similarity search for query: '{query}'")

    load_dotenv()
    db_name = config.CHROMA_DB_PERSIST_DIRECTORY
    print(f"Loading ChromaDB from directory: {db_name}")

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

    # Load ChromaDB
    vectorstore = Chroma(persist_directory=db_name, embedding_function=embeddings)

    # Perform similarity search
    results = vectorstore.similarity_search(query)

    print("\n--- Search Results ---")
    for i, doc in enumerate(results):
        print(f"Result {i + 1}:\n{doc.page_content}\n")


def main():
    queries = [
        "What is a saving throw?",
    ]

    for q in queries:
        query_chroma_db(q)


if __name__ == "__main__":
    main()
