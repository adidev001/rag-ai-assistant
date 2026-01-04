# RAG Personal AI Assistant

This is a Retrieval-Augmented Generation (RAG) Personal AI Assistant.
It allows you to upload PDF documents, indexes them using embeddings, and allows you to chat with the content using Google Gemini Pro.

## Projects Structure

- **frontend/**: Streamlit application for the UI.
- **backend/**: FastAPI application for the API and RAG logic.

## Setup & Run

1.  **Environment Variables**:
    Ensure you have a `.env` file in the root directory with your Google API Key:
    ```
    GEMINI_API_KEY=your_dummy_key_here
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r backend/requirements.txt
    pip install -r frontend/requirements.txt
    ```

3.  **Run Backend**:
    Open a terminal and run:
    ```bash
    cd backend
    uvicorn app.main:app --reload --port 8000
    ```
    The API will be available at `http://localhost:8000`.

4.  **Run Frontend**:
    Open another terminal and run:
    ```bash
    cd frontend
    streamlit run app.py
    ```
    The UI will open in your browser.

## 🐳 Docker Run
You can also run the entire application using Docker Compose.

1.  Make sure you have Docker Installed.
2.  Ensure your `.env` file is set up.
3.  Run:
    ```bash
    docker-compose up --build
    ```
4.  Open `http://localhost:8501` in your browser.

## Features

- **Upload PDF**: Automatically extracts text, chunks it, and creates vector embeddings.
- **Chat**: Semantic search over your documents + Gemini generation.
- **Persistent Database**: Uses ChromaDB to save your index locally.
