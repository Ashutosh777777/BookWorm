# 📚 BookWorm — RAG-Powered Book Chatbot

BookWorm is a Retrieval-Augmented Generation (RAG) chatbot that lets you have a conversation with your own books. Ask any question and get precise, context-aware answers drawn directly from the source material — no more manually flipping through hundreds of pages.

---

## 🧠 The Problem It Solves

While studying technical subjects like **Network Security** and **Web Application Security**, revisiting specific techniques buried deep in a book you've already read is tedious and time-consuming. General-purpose AI assistants aren't a reliable alternative either — most don't support uploading entire books, and they can't always reference those exact sources.

BookWorm solves this by indexing your books locally and letting you query them conversationally, grounded entirely in your own material.

---

## ✨ Features

- 💬 **Conversational Q&A** — Ask questions in natural language and get answers sourced directly from the book
- 🔍 **Semantic Search** — Uses vector embeddings to find the most relevant passages, not just keyword matches
- 🧩 **RAG Pipeline** — Retrieves context before generating a response, keeping answers grounded and accurate
- 📊 **Embedding Visualization** — 3D t-SNE plot of the vector store to visually explore how concepts are clustered
- 🖥️ **Gradio UI** — Clean chat interface that runs locally in your browser
- 🔌 **Flexible Deployment** — Can be adapted as an AI assistant or chatbot on various platforms

---

## 🛠️ Tech Stack

| Component | Tool |
|---|---|
| LLM | Llama 3.2 via [Ollama](https://ollama.com/) |
| Orchestration | LangChain |
| Vector Store | ChromaDB |
| Embeddings | HuggingFace `all-MiniLM-L6-v2` |
| PDF Loading | PyPDF + LangChain DirectoryLoader |
| Tokenization | Tiktoken (`cl100k_base`) |
| Visualization | Plotly + scikit-learn (t-SNE) |
| Chat UI | Gradio |

---

## 📁 Project Structure

```
BookWorm/
│
├── knowledge-base/         # Place your PDF books here
│   └── book.pdf
│
├── vector_db/              # Auto-generated ChromaDB vector store
│
├── worm.ipynb              # Main notebook (pipeline + chatbot)
│
├── .env                    # Environment variables (not committed)
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- [Ollama](https://ollama.com/) installed and running locally
- Llama 3.2 model pulled: `ollama pull llama3.2`

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ashutosh777777/BookWorm.git
   cd BookWorm
   ```

2. **Install dependencies**
   ```bash
   pip install langchain langchain-community langchain-chroma langchain-huggingface langchain-ollama chromadb pypdf tiktoken gradio plotly scikit-learn python-dotenv
   ```

3. **Add your book**

   Place your PDF file inside the `knowledge-base/` folder and name it `book.pdf` (or update the path in the notebook).

4. **Run the notebook**

   Open `worm.ipynb` in Jupyter and run all cells. The final cell launches the Gradio chat interface at `http://127.0.0.1:7860`.

---

## 💡 How It Works

1. **Load** — PDFs are loaded from the `knowledge-base/` directory using LangChain's `PyPDFLoader`
2. **Chunk** — Text is split into overlapping chunks (1000 chars, 200 overlap) using `RecursiveCharacterTextSplitter`
3. **Embed** — Chunks are embedded using `all-MiniLM-L6-v2` and stored in a ChromaDB vector store
4. **Retrieve** — At query time, the top relevant chunks are retrieved via semantic similarity search
5. **Generate** — Retrieved context is passed to Llama 3.2 along with the user's question to produce a grounded answer
6. **Chat** — The full pipeline is wrapped in a Gradio `ChatInterface` for easy interaction

---

## 📸 Embedding Visualization

The notebook includes a **3D t-SNE visualization** of the vector store, allowing you to explore how the book's concepts are semantically clustered in embedding space.

---

## 📖 Example Use Case

The initial knowledge base used in this project is *Real-World Bug Hunting* by Peter Yaworski — a field guide to web application hacking. BookWorm can answer questions like:

- *"What is HTTP Parameter Pollution?"*
- *"How does CSRF work?"*
- *"What are common techniques for finding XSS vulnerabilities?"*

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to open an issue or submit a pull request.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
