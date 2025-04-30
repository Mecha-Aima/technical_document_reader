
# 📘 Manual Mate

**Simplify Your Technical Manuals** — Parse, Extract, and Understand Complex Documentation with Ease.

Manual Mate is a Streamlit-powered AI assistant designed to process technical manuals and product guides. Using local LLMs and vector search, it allows users to upload PDFs and ask natural language questions to get accurate, contextual answers.

---

## 🚀 Features

- 📄 Upload and analyze PDF manuals
- 🧠 Semantic search using embeddings
- 💬 Chat-style Q&A based on manual contents
- 🤖 Local LLM support via [Ollama](https://ollama.com/)
- 💡 Clean and dark-themed UI with custom styling

---

## 🛠️ Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/)
- **Embedding Model**: `deepseek-r1:1.5b` via `Ollama`
- **LLM**: `deepseek-r1:1.5b` via `Ollama`
- **Vector Store**: In-memory vector search (`InMemoryVectorStore`)
- **PDF Parsing**: `PDFPlumberLoader`
- **Text Chunking**: `RecursiveCharacterTextSplitter`

---

## 📂 Folder Structure

```
document_store/
└── manuals/        # Stores uploaded PDF manuals
```

---

## 🧑‍💻 Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/manual-mate.git
cd manual-mate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install and run Ollama

```bash
ollama run deepseek-r1:1.5b
```

> Make sure Ollama is running locally and the `deepseek-r1:1.5b` model is downloaded.

### 4. Run the app

```bash
streamlit run app.py
```

---

## 📸 Screenshots

Coming soon...

---

## ❓ How it Works

1. Upload a technical manual PDF.
2. The document is parsed, chunked, and indexed using embeddings.
3. Ask a natural language question.
4. The app finds relevant chunks and sends them with your question to the LLM.
5. The LLM returns a concise and helpful answer.

---

## 🧩 TODOs

- Add support for multiple documents
- Improve document management
- Streamline embedding and indexing
- Option to select different LLMs or embeddings

---
