from collections import defaultdict


def group_chunks_by_paper(source_documents):

    papers = defaultdict(list)

    for doc in source_documents:

        paper = doc.metadata.get("paper", "unknown")
        text = doc.page_content

        papers[paper].append(text)

    return papers

def build_comparison_context(papers):

    context = ""

    for paper, texts in papers.items():

        context += f"\nPaper: {paper}\n"

        for t in texts[:3]:
            context += t + "\n"

    return context

from langchain_openai import ChatOpenAI


def compare_papers(context, question):

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    prompt = f"""
You are an AI research assistant.

Based on the research papers below, answer the question.

Context:
{context}

Question:
{question}

Provide a comparison between the papers if relevant.
"""

    response = llm.invoke(prompt)

    return response.content