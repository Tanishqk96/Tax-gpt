# core/pipeline.py

def build_index(doc_folder="docs", index_dir="faiss_index"):
    from langchain_community.document_loaders import PyPDFLoader, TextLoader
    from langchain.text_splitter import CharacterTextSplitter
    from langchain_community.embeddings import HuggingFaceEmbeddings
    from langchain_community.vectorstores import FAISS
    import os

    docs = []

    # Loop through files in doc_folder
    for filename in os.listdir(doc_folder):
        path = os.path.join(doc_folder, filename)
        if filename.endswith(".pdf"):
            loader = PyPDFLoader(path)
            docs.extend(loader.load())
        elif filename.endswith(".txt"):
            loader = TextLoader(path)
            docs.extend(loader.load())

    # Split, embed, store
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = FAISS.from_documents(chunks, embedder)
    db.save_local(index_dir)
