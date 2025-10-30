# Standard library imports
import os
import json

# Third-party imports
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelRequest,
    SummarizationMiddleware,
    dynamic_prompt,
)
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_core.runnables import RunnableConfig
from langchain_huggingface import HuggingFaceEmbeddings
from pydantic import BaseModel

from app import config

# Load environment variables from .env file
load_dotenv(override=True)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# --- Initialize components ---
print("Initializing components...")

# Initialize the chat model
if config.MODEL_URL:
    model = init_chat_model(f"{config.PROVIDER}:{config.MODEL}", model_url=config.MODEL_URL, temperature=0.2)
else:
    model = init_chat_model(f"{config.PROVIDER}:{config.MODEL}", temperature=0.2)
    
# Initialize the embeddings model
embeddings = HuggingFaceEmbeddings(model_name=config.EMBEDDING_MODEL)

# Initialize the Chroma vector store
vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory=config.CHROMA_DB_PERSIST_DIRECTORY,
)

print("Components initialized.")


# --- Dynamic Prompt Injection ---
@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """
    Injects relevant context from the vector store into the prompt.
    This function is decorated with @dynamic_prompt, which means it will be
    called before the model is invoked.
    """
    print("Entering prompt_with_context...")
    # Get the last user query from the state
    last_query = request.state["messages"][-1].text
    print(f"Searching for: {last_query}")

    # Perform a similarity search in the vector store
    retrieved_docs = vector_store.similarity_search(last_query, k=25)
    print(f"Found {len(retrieved_docs)} documents.")

    # Format the retrieved documents as a string
    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    # Create the system message with the context
    system_message = (
        "You are a helpful assistant. You have the following context which may be useful in answering the user:"
        f"\n\n{docs_content}"
    )
    print("Exiting prompt_with_context.")
    return system_message


# --- Create Agent ---
print("Creating agent...")
# Create the agent with the model, tools, and middleware
agent = create_agent(
    model,
    tools=[],
    middleware=[
        prompt_with_context,
        SummarizationMiddleware(model, max_tokens_before_summary=1000)
    ],
)
print("Agent created.")


# --- FastAPI App ---
app = FastAPI(
    title="D&D Rulebook LLM",
    description="A RAG application for querying the D&D rulebook.",
)

class QueryRequest(BaseModel):
    """Request model for the /invoke endpoint."""
    query: str
    thread_id: str


@app.post("/invoke")
async def invoke_agent(request: QueryRequest):
    """
    Invokes the agent with a query and streams the response.
    """
    print(f"Entering invoke_agent for thread: {request.thread_id}\n")

    # Create a RunnableConfig with the thread_id to maintain conversation history
    config = RunnableConfig(
        configurable={"thread_id": request.thread_id}
    )

    async def stream_response():
        """
        Streams the agent's response token by token.
        """
        print("Starting stream\n")
        try:
            # Stream the agent's response
            async for token, metadata in agent.astream(
                {"messages": [("user", request.query)]},
                config=config,
                stream_mode="messages"
            ):
                print(f"{token.content}", end="")
                if not token.content:
                    continue
                yield token.content

            print("\nStream finished.\n")
        except Exception as e:
            print(f"An error occurred during streaming: {e}\n")
            yield json.dumps({"error": str(e)}).encode("utf-8") + b"\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    print("Starting server...\n")
    # Run the FastAPI app with uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
