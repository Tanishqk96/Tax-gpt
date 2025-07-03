from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DOC_PATH="../data/taxdocs2.pdf"
INDX_PATH="faiss_index"

#-----TEXT LOADER-------#
loader= PyPDFLoader(DOC_PATH)
doc = loader.load()
#-----TEXT LOADER-------#

#-----BREAK INTO CHUNKS-------#
splitter = CharacterTextSplitter(
  chunk_size=500,
  chunk_overlap=100  
)
chunks = splitter.split_documents(doc)
#-----BREAK INTO CHUNKS-------#

#-----MAKING EMBEDDINGS-------#
embedder = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
#-----MAKING EMBEDDINGS-------#

#-----MAKING VECTOR STORE-------#
db= FAISS.from_documents(chunks,embedder)
#-----MAKING VECTOR STORE-------#

# === STEP 5: Save to Disk ===
db.save_local(INDX_PATH)
print(f"✅ Vector index saved to: {INDX_PATH}")
# === STEP 5: Save to Disk ===
