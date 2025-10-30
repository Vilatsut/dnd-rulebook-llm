import os
from dotenv import load_dotenv

from llama_cloud_services import LlamaParse


def main():
    """Extracts data from the PDF file using LlamaParse."""
    
    load_dotenv()
    LLAMA_CLOUD_API_KEY = os.getenv('LLAMA_CLOUD_API_KEY', 'your-key-if-not-using-env')

    print("Extracting data from PDF using LlamaParse...")
    parser = LlamaParse(
        api_key=LLAMA_CLOUD_API_KEY,
        verbose=True,
        language="en",       
        skip_diagonal_text=True,
        bounding_box="0,0,0.05,0",
        use_vendor_multimodal_model=True,
        vendor_multimodal_model_name="anthropic-sonnet-4.5",
        result_type="markdown"
    )
    
    documents = parser.load_data("G:\\dnd-rulebook-llm\\data\\dragons_of_stormwreck_isle.pdf")
    
    # Save the extracted markdown content to a file
    if documents:
        output_file_path = "data/dnd_rules_markdown.md"
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)
        with open(output_file_path, "w", encoding="utf-8") as f:
            for doc in documents:
                f.write(doc.text)
        print(f"Extracted markdown saved to {output_file_path}")

if __name__ == "__main__":
    main()
