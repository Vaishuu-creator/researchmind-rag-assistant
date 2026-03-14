from langchain_community.document_loaders import PyPDFLoader
import os

def load_pdf(file_path):
    
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    paper_name = os.path.basename(file_path)

    for doc in documents:
        doc.metadata["paper"] = paper_name
        
    return documents