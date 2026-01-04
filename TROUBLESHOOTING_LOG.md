# 🛠️ RAG AI Assistant - Troubleshooting Log & Learning Resources

This log documents the technical challenges faced during the development of this RAG (Retrieval-Augmented Generation) application and how they were solved.
Use this as a learning reference for building similar applications.

---

## 1. 🐍 Backend & Environment

### ❌ Issue: Missing Dependencies (`ModuleNotFoundError`)
- **Problem**: Code referenced `pdfplumber` but `requirements.txt` listed `PyPDF2`.
- **Root Cause**: Implementation details changed but the dependency list wasn't updated.
- **Solution**: Updated `requirements.txt` to include `pdfplumber` and ran `pip install -r ...`.

### ❌ Issue: Environment Variables Not Loading
- **Problem**: Services like `llm.py` failed to find `GEMINI_API_KEY`.
- **Root Cause**: `.env` files are not automatically loaded by Python scripts.
- **Solution**: Added `python-dotenv` and called `load_dotenv()` explicitly at the entry point (`main.py`) before importing other modules.

### ❌ Issue: Import Errors (`ModuleNotFoundError: No module named 'services'`)
- **Problem**: `from app.services import ...` failed inside the backend.
- **Root Cause**: Python path resolution issues when running scripts from different directories.
- **Solution**: Used absolute imports (`from services...`) and ensured `sys.path` was correctly set in `main.py`.

---

## 2. 📄 File Upload & Processing

### ❌ Issue: Upload Hanging / "Internal Server Error"
- **Problem**: Uploads would fail silently or return generic 500 errors.
- **Root Cause**: Hidden exceptions (like dependencies missing) and `SpooledTemporaryFile` issues with `pdfplumber`.
- **Solution**: 
    1.  Added **Middleware** in `main.py` to catch and print *all* exceptions.
    2.  Modified `document_loader.py` to read the file into `BytesIO` memory buffer before processing.

---

## 3. 🧠 Vector Database (ChromaDB)

### ❌ Issue: Data Not Persisting
- **Problem**: Uploaded documents disappeared after server restart.
- **Root Cause**: Using `chromadb.Client()` creates an in-memory (RAM) database.
- **Solution**: Switched to `chromadb.PersistentClient(path="chroma_db")` to save the index to disk.

### ❌ Issue: ID Generation Errors
- **Problem**: Error regarding invalid or duplicate IDs.
- **Root Cause**: Using simple strings or auto-generation that conflicted.
- **Solution**: Used `uuid.uuid4()` to generate a unique string ID for every document chunk.

---

## 4. 🤖 AI Model (Google Gemini)

### ❌ Issue: Model Not Found (`404 models/gemini-1.5-pro`)
- **Problem**: API rejected requests for `gemini-1.5-pro`.
- **Root Cause**: The specific model version was deprecated or restricted for the API key type.
- **Solution**:
    1.  Wrote a script `check_models.py` to list available models.
    2.  Switched code to use the newer, available `gemini-2.0-flash`.

---

## 5. 🌐 Server & Ports

### ❌ Issue: "Address already in use"
- **Problem**: Unable to start the backend because port 8000 was busy.
- **Root Cause**: Zombie Python processes from failed reload attempts holding onto the port.
- **Solution**: Used CLI commands to identify (`netstat`) and kill (`Stop-Process`) the specific processes.

---

## 6. 🐙 Git Version Control

### ❌ Issue: Push Rejected (Large Files)
- **Problem**: Git rejected push due to files >100MB (`venv/.../torch_cpu.dll`).
- **Root Cause**: The `venv` directory was accidentally committed before adding it to `.gitignore`.
- **Solution**:
    1.  Created a `.gitignore` file to exclude `venv/` and `chroma_db/`.
    2.  Performed a **Git History Reset** (orphan branch) to completely remove the large files from the commit history.
    3.  Force pushed the clean state.


---

## 7. ?? Log - Jan 4, 2026 (Major UI & Windows Compatibility Update)

### ? Issue: Windows vs Docker Networking
- **Problem**: Attempted to Dockerize the app, but encountered heavy download sizes (>2GB) and complexity. User opted to revert to local Python execution.
- **Solution**: 
    1.  Reverted all Docker-related files (Dockerfile, docker-compose.yml).
    2.  Restored pp.py to run natively on Windows.

### ? Issue: Connection Refused (IPv4/IPv6)
- **Problem**: Frontend failed to connect to Backend (ConnectionRefusedError: [WinError 10061]).
- **Root Cause**: Windows creates ambiguity between localhost (often resolving to IPv6 ::1) and 127.0.0.1 (IPv4). The FastAPI backend was listening on IPv4.
- **Solution**: Explicitly hardcoded BACKEND_URL = "http://127.0.0.1:8000" in rontend/app.py.

### ? Issue: Backend Crash on Printing Special Characters
- **Problem**: Backend crashed during vector search with UnicodeEncodeError: 'charmap' codec can't encode character.
- **Root Cause**: Windows Console (cmd/powershell) often defaults to legacy encodings (cp1252) that cannot print certain PDF symbols (like mathematical minus signs).
- **Solution**: Removed the print() statement in ector_store.py that was trying to log the raw search results to the console.

### ? Enhancement: Complete UI Overhaul (P-RAG-DF)
- **Visuals**: Implemented "Deep Cosmos" theme (Dark mode with Neon Violet/Indigo accents).
- **Layout**: Switched to a **Split View** (Left: Upload, Right: Chat) for better usability.
- **UX**: 
    - Moved Answer Block **above** the Input field for a more natural "Chat Log" feel.
    - Added background particle effects (particles.js).
    - Added "Glassmorphism" styling to containers.
