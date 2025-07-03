from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Ollama
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_core.runnables import RunnableLambda 

# === Step 1: Config ===
INDEX_DIR = "faiss_index"
EMBED_MODEL = "all-MiniLM-L6-v2"
LLM_MODEL = "mistral"
# === Step 1: Config ===
prompt = PromptTemplate.from_template("""
Answer the following question using the provided context.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question:
{question}

Answer in bullet points:
""")




def buildragchain():
    embeddings= HuggingFaceEmbeddings(model_name = EMBED_MODEL)
    llm = Ollama(model=LLM_MODEL)
    vectorstore = FAISS.load_local(
        INDEX_DIR,
        embeddings,
        allow_dangerous_deserialization=True 
    )
   
    retriever = vectorstore.as_retriever()
    llm = Ollama(model=LLM_MODEL)
    
    retrieval_chain = RunnableMap({
        "context": retriever,
        "question": RunnablePassthrough()
    })

    # Prompting + LLM step
    rag_chain = retrieval_chain | prompt | llm

    return rag_chain

if __name__ == "__main__":
    chain = buildragchain()
    print("🤖 Modern RAG system is ready using `.invoke()`! Type 'exit' to quit.")

    while True:
        query = input("\nAsk: ")
        if query.lower() in ["exit", "quit"]:
            print("👋 Exiting...")
            break

        answer = chain.invoke(query)
        print("\n🧠 Answer:\n", answer)
