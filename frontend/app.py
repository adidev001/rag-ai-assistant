import streamlit as st
import requests

BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Personal AI Knowledge Assistant")

st.title("📚 Personal AI Knowledge Assistant")

# --- SESSION STATE ---
if "uploaded" not in st.session_state:
    st.session_state.uploaded = False

# --- FILE UPLOAD ---
# --- FILE UPLOAD ---
uploaded_file = st.file_uploader(
    "Upload a document",
    type=["pdf"]
)

if uploaded_file:
    with st.form("upload_form"):
        st.write("Ready to upload...")
        submitted = st.form_submit_button("Upload to Backend")
        
        if submitted:
            st.info(f"DEBUG: Starting upload... Target: {BACKEND_URL}/upload/")
            try:
                # Use getvalue() to ensure we have the bytes
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
                
                res = requests.post(f"{BACKEND_URL}/upload/", files=files)
                
                st.write(f"DEBUG: Status Code: {res.status_code}")
                
                if res.status_code == 200:
                    st.session_state.uploaded = True
                    st.success(f"Success! {res.json()}")
                else:
                    st.error(f"Failed: {res.status_code} - {res.text}")
            except Exception as e:
                st.error(f"Connection Error: {e}")


# --- QUESTION ---
# --- ASK QUESTION ---
query = st.text_input("Ask a question")

if st.button("Ask"):
    if not st.session_state.get("uploaded", False):
        st.warning("Please upload a document first.")
    else:
        response = requests.post(
            f"{BACKEND_URL}/chat/",
            json={"query": query}
        )

        data = response.json()

        st.subheader("Answer")
        st.write(data.get("answer", "No answer returned"))

        sources = data.get("sources", [])
        if sources:
            st.subheader("Sources")
            st.json(sources)
