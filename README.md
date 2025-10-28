# 🧠 Source Code Analysis — LangChain + Chainlit + MistralAI

**Description**  
This project lets you *chat with a GitHub repository's source code*. Paste a repo URL into the chat UI and the system will clone, ingest, chunk, embed, and store the code in a vector database so you can query functions, architecture, and logic interactively.

---

## 🚀 Features
- Clone and ingest public GitHub repositories dynamically.  
- Chunk source files and embed with a configurable embedding model.  
- Store vectors in **ChromaDB** for fast semantic retrieval.  
- Multi-turn chatting with memory.  
- Interactive front-end using **Chainlit**.  
- Configurable LLM (Mistral) for answers and summarization.

---

## 🧩 Architecture (textual diagram)
```
GitHub Repo URL --> Repo Ingestion (GitPython) --> Text Loading & Splitting --> Embeddings (Mistral/OpenAI) --> Chroma Vector DB --> LangChain Retrieval + Prompting --> Chainlit UI
```

<!-- (You can add an image `assets/architecture.png` and reference it here if you want a visual diagram.) -->

---

## ⚙️ Requirements & Tech Stack
- Python 3.10+  
- LangChain  
- Chainlit  
- langchain_mistralai (or LLM integration)  
- chromadb / Chroma langchain integration  
- GitPython  
- python-dotenv

---

## 🔧 Quick Setup (local)

1. **Clone this repo** (if not already):
```bash
git clone https://github.com/Manvendra-SR/Langchain-repo-analyzer.git
cd Langchain-repo-analyzer
```

2. **Create environment** (conda example):
```bash
conda create -n source python=3.10 -y
conda activate source
pip install -r requirements.txt
```

3. **Create `.env`** in project root and add keys, for example:
```
MISTRAL_API_KEY=your_mistral_api_key
```

4. **Run Chainlit UI**:
```bash
chainlit run app.py -w
```
Open the URL printed (usually `http://localhost:8000`) and paste a GitHub repo URL to ingest.  

---

## 🧭 Typical Workflow
1. Paste GitHub repository URL into Chainlit chat.  
2. App clones repo into a unique folder (e.g., `repo_ab12cd`).  
3. `store_index.py` processes the repo: loads files, splits text, produces embeddings, and writes them to Chroma.  
4. Ask questions in the chat. LangChain retrieves relevant chunks and the LLM (Mistral) generates answers.  
5. Conversation history placed into memory to enable follow-ups.

---

## 🗂️ Project Structure (example)
```
├── app.py              # Chainlit entrypoint + chain and handlers
├── store_index.py      # Script to load repo and populate vector DB
├── src/
│   └── helper.py       # helpers: repo_ingestion, load_repo, text_splitter, embeddings
├── chroma_langchain_db/ # persisted Chroma DB (optional)
├── requirements.txt
├── .env
└── README.md
```

---

## 🔁 Re-ingestion / Fresh Indexing
By default, Chroma persists vectors in `./chroma_langchain_db`. To always start fresh on each ingestion, either:
- Delete the folder before indexing: `rm -rf ./chroma_langchain_db`, or
- Use a unique `persist_directory` per ingestion run (recommended for multi-repo).

When calling the ingestion pipeline, pass the repo folder path into `store_index.py` (example):
```bash
python store_index.py repo_ab12cd
```

---

## 🧪 Troubleshooting & Tips
- If you get `fatal: destination path 'repo' already exists`, ensure ingestion uses unique folders or remove the folder before cloning.  
- If embeddings are empty, verify `load_repo()` returns documents and `load_embedding()` is properly initialized.  
- If LLM responses truncate (e.g., only first token), try increasing `max_tokens` or switch to a different model temporarily.  
- Use `subprocess.run([...], check=True)` instead of `os.system(...)` when invoking scripts to avoid argument interpolation bugs.

---

## ✨ Future Improvements
- Multi-repo context switching and namespace isolation.  
- Background ingestion queue with progress updates.  
- Add repo summarization and codebase-level graphs.  
- Authentication and GitHub private repo support.

---

## 👤 Author
**Manvendra Singh** — IIT Indore.  
Project maintained by the author. Contributions welcome — open a PR or an issue.

---

## 📝 License
MIT License. See `LICENSE`.

