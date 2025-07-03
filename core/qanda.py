# core/qanda.py

from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough

def load_chain(index_dir="faiss_index"):
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.load_local(index_dir, embedder, allow_dangerous_deserialization=True)
    retriever = vectorstore.as_retriever()
    llm = Ollama(model="mistral")

    prompt = PromptTemplate.from_template("""
    Use the following context to answer the question.
    Context:
    {context}
    Question: {question}
    """)

    chain = RunnableMap({
        "context": retriever,
        "question": RunnablePassthrough()
    }) | prompt | llm

    return chain
