import os
from langchain_community.document_loaders import PyMuPDFLoader, TextLoader, JSONLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

def load_and_split_data(file_path):
    # 1. Smart Selection of Loader
    if file_path.endswith('.pdf'):
        loader = PyMuPDFLoader(file_path)
    elif file_path.endswith('.json'):
        # Updated for common JSON list structures
        loader = JSONLoader(file_path, jq_schema=".[]", text_content=False)
    else:
        loader = TextLoader(file_path)

    docs = loader.load()

    # 2. NEW: Metadata Enrichment (Cleaning the filename)
    # This removes 'temp_' from the start of the name for a professional look
    original_filename = os.path.basename(file_path).replace("temp_", "")

    # 3. Industry-Level Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=100
    )
    chunks = text_splitter.split_documents(docs)

    # 4. NEW: Tagging every chunk with its source filename
    for chunk in chunks:
        chunk.metadata["filename"] = original_filename

    return chunks