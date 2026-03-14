from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI

def create_qa_chain(retriever):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )

    return qa_chain