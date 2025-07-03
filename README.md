---

## 🧾 Tax-GPT – AI-Powered Tax Advisor with RAG 🔍

**Tax-GPT** is an intelligent RAG (Retrieval-Augmented Generation) application built with **LangChain**, **FAISS**, **Gemini/Ollama**, and **Streamlit**. It helps users upload tax documents and ask natural language questions to receive accurate, context-aware answers.

> 📌 Built for zero-token local testing & powerful cloud deployment – deploy it or run it entirely offline!

---

## 🚀 Features

* 📄 **Document Ingestion** – Upload PDFs of tax laws or filings
* 🔍 **Contextual QA** – Ask natural questions like *“What deductions can I claim as a freelancer?”*
* 🧠 **RAG Pipeline** – Uses FAISS + LangChain to fetch relevant context
* 💬 **LLM Response** – Powered by:

  * `Ollama (Mistral)` for local/offline
  * `Gemini Pro` for deployed mode
* 👥 **User Authentication** – Secure login before access
* 🌐 **Streamlit Frontend** – Clean, responsive UI

---

## 🛠️ Tech Stack

| Layer      | Tech                                                                         |
| ---------- | ---------------------------------------------------------------------------- |
| LLM        | [Ollama](https://ollama.com) (Mistral) / [Gemini Pro](https://ai.google.dev) |
| Embeddings | Google Generative AI Embeddings                                              |
| Vector DB  | FAISS                                                                        |
| Framework  | LangChain                                                                    |
| Frontend   | Streamlit                                                                    |
| Auth       | SQLite + hashed login                                                        |
| Deployment | Docker, Render                                                               |

---

## 🧪 Local Development (Ollama)

> ⚠️ Free, tokenless mode using Mistral LLM (you must install Ollama)

```bash
# 1. Run the LLM
ollama run mistral

# 2. Start the app
streamlit run streamlit_app.py --server.port=8000 --server.enableCORS false
```

✅ Upload your `taxdocs.pdf` in `/data`
✅ Then ask: *“List exemptions for salaried employees in India”*

---

## 🌍 Cloud Deployment (Gemini API)

> Uses `gemini-pro` for hosted apps on Render, Fly.io, etc.

1. Set your API key in `.env`:

```env
GOOGLE_API_KEY=your_gemini_key_here
```

2. Make sure your `qanda.py` uses:

```python
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-pro")
```

3. Build and deploy via Docker:

```bash
docker build -t tax-gpt .
docker run -p 8000:8000 tax-gpt
```

---

## 🔐 Authentication

* Simple username/password-based auth via `auth_utils.py`
* Pre-seeded user DB: `users.db`
* Modify credentials as needed in `auth_utils.py`

---

## 📁 Project Structure

```
tax-gpt/
│
├── data/                  # Upload your PDF docs here
├── core/
│   ├── pipeline.py        # Builds FAISS index
│   ├── qanda.py           # Loads vectorstore and answers queries
│   ├── auth_utils.py      # Auth logic
│
├── streamlit_app.py       # Main Streamlit UI
├── requirements.txt       # All dependencies
├── Dockerfile             # For deployment
├── .env                   # API keys (excluded from Git)
```

---

## 🧠 Sample Questions

* “Can I claim rent if I live with parents?”
* “What is Section 80C in Indian Tax?”
* “Explain capital gains tax after 3 years”

---

## 🧩 TODO & Enhancements

* [ ] Multi-doc upload & ingestion
* [ ] Semantic search filtering
* [ ] Chat history
* [ ] OpenAI / Together.ai integration
* [ ] Fine-tuned answer formatting

---

## 💡 Inspiration

Built to solve real-world tax document pain points with AI.
Inspired by OpenAI RAG demos, Ollama offline LLMs, and India’s chaotic tax filing season 💸

---

