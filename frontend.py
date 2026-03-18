import streamlit as st
import requests

# Page Styling
st.set_page_config(page_title="Omer's AI Engine", page_icon="🚀", layout="wide")
st.title("🤖 Advanced Hybrid RAG Engine")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📁 Document Center")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if st.button("Process Document", use_container_width=True):
        if uploaded_file:
            with st.spinner("Creating Memory..."):
                files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
                response = requests.post("http://localhost:8000/upload", files=files)
                if response.status_code == 200:
                    st.success("Ready to Chat!")
                else:
                    st.error("Upload failed.")
        else:
            st.warning("Select a PDF first.")

    st.markdown("---")
    if st.button("🗑️ Reset All Memory", type="secondary", use_container_width=True):
        requests.delete("http://localhost:8000/reset-memory")
        st.session_state.messages = []
        st.rerun()

# Initialize Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "sources" in message:
            with st.expander("📚 Sources"):
                st.write(f"Cited from: {', '.join(message['sources'])}")

# User Input
if prompt := st.chat_input("Ask about your document..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Searching..."):
            # Talking to the Backend
            res = requests.post(f"http://localhost:8000/ask?question={prompt}")
            
            if res.status_code == 200:
                data = res.json()
                answer = data.get("answer")
                sources = data.get("sources", [])
                
                st.markdown(answer)
                if sources:
                    with st.expander("📚 Sources"):
                        st.write(f"Cited from: {', '.join(sources)}")
                
                # Save to history
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": answer, 
                    "sources": sources
                })
            else:
                st.error("Brain is offline. Check Terminal 1.")