from ingestion.pdf_loader import load_pdf
from ingestion.text_chunker import split_documents
from ingestion.embed_store import create_or_load_vector_store

from rag.retriever import get_retriever
from rag.qa_chain import create_qa_chain

from rag.comparison import group_chunks_by_paper, build_comparison_context, compare_papers

docs1 = load_pdf("data/papers/sample_paper1.pdf")
docs2 = load_pdf("data/papers/sample_paper2.pdf")

documents = docs1 + docs2

chunks = split_documents(documents)

from ingestion.embed_store import create_or_load_vector_store
vectorstore = create_or_load_vector_store(chunks)

retriever = get_retriever(vectorstore)

qa_chain = create_qa_chain(retriever)


question = input("Enter your question: ")

result = qa_chain.invoke({"query": question})

if any(word in question.lower() for word in ["compare", "difference", "contrast"]):

    papers = group_chunks_by_paper(result["source_documents"])
    context = build_comparison_context(papers)
    comparison_answer = compare_papers(context, question)

    print("\nComparison Answer:\n")
    print(comparison_answer)

else:

    answer = result["result"]
    print("\nAnswer:\n")
    print(result["result"])


print("\nSources:\n")

seen = set()

for doc in result["source_documents"]:
    
    page = doc.metadata.get("page", "unknown")
    paper = doc.metadata.get("paper", "unknown")

    key = (paper, page)

    if key not in seen:
        print(f"{paper} — Page {page + 1}")
        seen.add(key)

print("Total documents loaded:", len(documents))