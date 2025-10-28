from src.helper import *
import sys
from dotenv import load_dotenv
from langchain_chroma import Chroma
import os
from uuid import uuid4

load_dotenv()


# url = "https://github.com/entbappy/End-to-end-Medical-Chatbot-Generative-AI"

# repo_ingestion(url)

if len(sys.argv) < 2:
    raise ValueError("Usage: python store_index.py <repo_folder_path>")

repo_path = sys.argv[1]
print(f"Ingesting repo from: {repo_path}")

documents = load_repo(repo_path)
text_chunks = text_splitter(documents)
embeddings = load_embedding()



vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)
uuids = [str(uuid4()) for _ in range(len(text_chunks))]

vector_store.add_documents(documents=text_chunks, ids=uuids)