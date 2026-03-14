import streamlit as st

from ingestion.pdf_loader import load_pdf
from ingestion.text_chunker import split_documents
from ingestion.embed_store import create_or_load_vector_store

from rag.retriever import get_retriever
from rag.qa_chain import create_qa_chain
from rag.comparison import group_chunks_by_paper, build_comparison_context, compare_papers


st.set_page_config(
    page_title="AI Research Paper Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Research Paper Assistant")


# ------------------------------
# SIDEBAR
# ------------------------------

st.sidebar.header("Upload Research Papers")

uploaded_files = st.sidebar.file_uploader(
    "Upload PDFs",
    type="pdf",
    accept_multiple_files=True
)


# ------------------------------
# SESSION STATE (Chat Memory)
# ------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# ------------------------------
# PROCESS PAPERS
# ------------------------------

if uploaded_files:

    documents = []

    for uploaded_file in uploaded_files:

        file_path = f"data/{uploaded_file.name}"

        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        docs = load_pdf(file_path)
        documents.extend(docs)

    chunks = split_documents(documents)

    vectorstore = create_or_load_vector_store(chunks)

    retriever = get_retriever(vectorstore)

    qa_chain = create_qa_chain(retriever)

else:
    st.info("Upload research papers to begin.")
    st.stop()


# ------------------------------
# CHAT HISTORY DISPLAY
# ------------------------------

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ------------------------------
# USER INPUT
# ------------------------------

prompt = st.chat_input("Ask a question about the papers")

if prompt:

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)

    result = qa_chain.invoke({"query": prompt})

    # Decide mode
    if any(word in prompt.lower() for word in ["compare", "difference", "contrast"]):

        papers = group_chunks_by_paper(result["source_documents"])
        context = build_comparison_context(papers)

        answer = compare_papers(context, prompt)

    else:
        answer = result["result"]

    # Display assistant message
    with st.chat_message("assistant"):
        st.markdown(answer)

        st.markdown("**Sources:**")

        seen = set()

        for doc in result["source_documents"]:

            page = doc.metadata.get("page", 0) + 1
            paper = doc.metadata.get("paper", "unknown")

            key = (paper, page)

            if key not in seen:
                st.markdown(f"- {paper} — Page {page}")
                seen.add(key)

    st.session_state.messages.append({"role": "assistant", "content": answer})