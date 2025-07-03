from core.auth_utils import init_user_db, signup_user, login_user
from core.pipeline import build_index
from core.qanda import load_chain
import os, shutil, streamlit as st

# Initialize user DB
init_user_db()

# -- Auth UI --
st.set_page_config(page_title="TaxGPT - AI Tax Advisor", layout="wide")
st.title("🔐 Welcome to TaxGPT – AI Tax Advisor")

auth_mode = st.radio("Choose Action:", ["Login", "Sign Up"], horizontal=True)

if auth_mode == "Sign Up":
    new_user = st.text_input("Create Username")
    new_pass = st.text_input("Create Password", type="password")
    if st.button("🔐 Create Account"):
        success = signup_user(new_user, new_pass)
        if success:
            st.success("✅ Account created. You can now log in.")
        else:
            st.error("⚠️ Username already exists.")

elif auth_mode == "Login":
    user = st.text_input("Username")
    passwd = st.text_input("Password", type="password")
    if st.button("🔓 Login"):
        if login_user(user, passwd):
            st.success(f"✅ Welcome, {user}!")
            st.session_state.logged_in = True
            st.session_state.username = user
        else:
            st.error("❌ Invalid credentials")

# -- ✅ MAIN APP LOGIC (Wrapped) --
if st.session_state.get("logged_in"):
    st.subheader(f"👋 Hello, {st.session_state.username}! Let's analyze some tax files.")
    
    DOCS_FOLDER = "docs"
    INDEX_FOLDER = "faiss_index"

    st.sidebar.title("📁 Upload Tax Docs")
    uploaded_files = st.sidebar.file_uploader("Upload PDF/TXT", type=["pdf", "txt"], accept_multiple_files=True)

    if uploaded_files:
        # Save files
        if os.path.exists(DOCS_FOLDER):
            shutil.rmtree(DOCS_FOLDER)
        os.makedirs(DOCS_FOLDER, exist_ok=True)

        for f in uploaded_files:
            with open(os.path.join(DOCS_FOLDER, f.name), "wb") as out:
                out.write(f.getbuffer())
        st.sidebar.success("✅ Files uploaded.")

        with st.spinner("⚙️ Building vector index..."):
            build_index(DOCS_FOLDER, INDEX_FOLDER)
        st.sidebar.success("📦 Index ready!")

    if not os.path.exists(INDEX_FOLDER):
        st.warning("⚠️ Please upload and index documents first.")
        st.stop()

    @st.cache_resource
    def get_chain():
        return load_chain(index_dir=INDEX_FOLDER)

    chain = get_chain()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_query = st.text_input("💬 Ask a tax question:")

    if st.button("Ask") and user_query:
        with st.spinner("🤖 Thinking..."):
            answer = chain.invoke(user_query)
            st.session_state.chat_history.append(("You", user_query))
            st.session_state.chat_history.append(("TaxGPT", answer))

    for sender, msg in st.session_state.chat_history:
        if sender == "You":
            st.markdown(f"**🧑‍💼 You:** {msg}")
        else:
            st.markdown(f"**🤖 TaxGPT:** {msg}")
