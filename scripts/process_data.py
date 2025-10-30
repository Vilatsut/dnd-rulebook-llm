import os
from dotenv import load_dotenv

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app import config

def process_and_store_data():
    """Processes the extracted markdown and stores it in ChromaDB."""
    print("Processing markdown and storing in ChromaDB...")
    
    load_dotenv()
    db_name = config.CHROMA_DB_PERSIST_DIRECTORY

    # Load the markdown file
    markdown_file_path = "data/dnd_rules_markdown.md"
    with open(markdown_file_path, "r", encoding="utf-8") as f:
        markdown_content = f.read()

    # Split the markdown into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.create_documents([markdown_content])
    print(f"Split markdown into {len(chunks)} chunks.")

    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if os.path.exists(db_name):
        Chroma(persist_directory=db_name, embedding_function=embeddings).delete_collection()

    # Store in ChromaDB
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=db_name
    )
    print("Data successfully stored in ChromaDB.")

def main():
    process_and_store_data()

if __name__ == "__main__":
    main()