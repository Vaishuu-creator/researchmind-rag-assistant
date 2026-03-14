import os
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()


def create_or_load_vector_store(chunks):

    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )

    index_path = "vectorstore/faiss_index"

    # If index already exists → load it
    if os.path.exists(index_path):

        print("Loading existing FAISS index...")

        vectorstore = FAISS.load_local(
            index_path,
            embeddings,
            allow_dangerous_deserialization=True
        )

    else:

        print("Creating new FAISS index...")

        vectorstore = FAISS.from_documents(
            chunks,
            embeddings
        )

        vectorstore.save_local(index_path)

        print("FAISS index saved!")

    return vectorstore