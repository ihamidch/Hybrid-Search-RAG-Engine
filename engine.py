import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

def create_hybrid_retriever(chunks):
    # 1. Setup the "Meaning" Search (Vector)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 2. Create the Search Index
    vectorstore = FAISS.from_documents(chunks, embeddings)
    
    # 3. NEW: Save the index to your E: drive so it's permanent
    # This creates a folder named 'my_ai_memory'
    vectorstore.save_local("my_ai_memory")
    print("✅ Memory saved to disk!")
    
    return vectorstore.as_retriever(search_kwargs={"k": 5})