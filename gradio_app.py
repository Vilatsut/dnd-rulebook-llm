import gradio as gr
import requests
import uuid

# The URL of the FastAPI application
URL = "http://app:8000/invoke"

def predict(message, history):
    """
    Invokes the response from the LLM and streams it.
    Note: A new thread_id is generated for each conversation turn, so conversation history is not maintained.
    """
    thread_id = str(uuid.uuid4())
    print(f"Received message: {message}")
    print(f"Generated thread_id: {thread_id}")
    
    payload = {"query": message, "thread_id": thread_id}
    print(f"Sending payload to FastAPI: {payload}")

    try:
        with requests.post(URL, json=payload, stream=True) as response:
            response.raise_for_status()
            full_response = ""
            for chunk in response.iter_content(chunk_size=None):
                if chunk:
                    full_response += chunk.decode('utf-8')
                    print(f"Current full_response: {full_response}")
                    yield full_response
    except requests.exceptions.RequestException as e:
        yield f"An error occurred: {e}"

# Create the Gradio ChatInterface
print("Creating Gradio ChatInterface...")
chat_interface = gr.ChatInterface(
    predict,
    title="D&D Rulebook LLM",
    description="Ask me any question about the D&D Stormwreck Isles rules or campaign.",
    type="messages"
)
print("Gradio ChatInterface created.")

if __name__ == "__main__":
    print("Launching Gradio app...")
    chat_interface.launch(server_name="0.0.0.0", server_port=7860)
