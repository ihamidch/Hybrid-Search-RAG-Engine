import os
import shutil
from fastapi import FastAPI, UploadFile, File
from dotenv import load_dotenv
from langchain_groq import ChatGroq
# Use the 'classic' path for retrieval and document chains in 2026
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from loader import load_and_split_data
from engine import create_hybrid_retriever

load_dotenv()

app = FastAPI(title="Advanced Hybrid RAG Engine")

# 1. Initialize LLM (Llama 3.3 via Groq)
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)

# Global variable to hold our retriever
retriever = None

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    global retriever
    file_path = f"temp_{file.filename}"
    
    # Save file temporarily
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())
    
    try:
        # Process data using the updated loader (which now adds filename to metadata)
        chunks = load_and_split_data(file_path)
        retriever = create_hybrid_retriever(chunks)
        
        # Cleanup the temp file
        os.remove(file_path)
        return {"message": f"File {file.filename} processed successfully into Hybrid Index."}
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        return {"error": f"Failed to process file: {str(e)}"}

@app.post("/ask")
async def ask_question(question: str):
    global retriever
    if not retriever:
        return {"error": "Please upload a document first or check if memory exists."}

    # Define the Professional System Prompt
    system_prompt = (
        "You are an expert assistant. Use the provided context to answer the question. "
        "If the answer isn't in the context, say you don't know. "
        "Context: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])

    # Build the RAG Chain
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)

    # Invoke the chain
    response = rag_chain.invoke({"input": question})
    
    # --- UPDATED: Extract Filename and Page from Metadata ---
    sources = []
    if "context" in response:
        for doc in response["context"]:
            # Get the filename we added in loader.py
            fname = doc.metadata.get("filename", "Unknown Source")
            # Get the page number (PyMuPDF is 0-indexed)
            page = doc.metadata.get("page", 0) + 1
            sources.append(f"{fname} (Page {page})")
    
    return {
        "answer": response["answer"],
        "sources": list(set(sources))  # Remove duplicates
    }

@app.delete("/reset-memory")
async def reset_memory():
    global retriever
    folder_path = "my_ai_memory"
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    
    retriever = None  # Clear active retriever from memory
    return {"message": "Memory folder deleted and retriever reset successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)