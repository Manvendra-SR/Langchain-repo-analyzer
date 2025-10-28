import os
from git import Repo
from langchain_community.document_loaders.generic import GenericLoader
from langchain_community.document_loaders.parsers import LanguageParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_mistralai import MistralAIEmbeddings
from langchain_core.messages import HumanMessage, AIMessage
from langchain_mistralai.chat_models import ChatMistralAI
from uuid import uuid4
from git import Repo
from dotenv import load_dotenv

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0,
    max_retries=2,
    # other params...
)

# def repo_ingestion(repo_url):
#     os.makedirs("repo", exist_ok=True)
#     repo_path = "repo/"
#     Repo.clone_from(repo_url, to_path=repo_path)

def repo_ingestion(repo_url):
    folder_name = f"repo_{uuid4().hex[:6]}"
    Repo.clone_from(repo_url, folder_name)
    return folder_name

#Loading repositories as documents
def load_repo(repo_path):
    loader = GenericLoader.from_filesystem(repo_path,
                                        glob = "**/*",
                                       suffixes=[".py"],
                                       parser = LanguageParser(language="python", parser_threshold=500)
                                        )
    
    documents = loader.load()

    return documents

#Creating text chunks 
def text_splitter(documents):
    documents_splitter = RecursiveCharacterTextSplitter.from_language(language = "python",
                                                             chunk_size = 2000,
                                                             chunk_overlap = 200)
    
    text_chunks = documents_splitter.split_documents(documents)

    return text_chunks

#loading embeddings model
def load_embedding():
    embeddings = MistralAIEmbeddings(
            model="mistral-embed",
    )
    return embeddings

def load_history(memory_store):
    return memory_store

def save_message(user_input, ai_output):
    global memory_store
    history = memory_store
    history.extend([
        HumanMessage(content=user_input),
        AIMessage(content=ai_output)
    ])
    
    # If too long, summarize older parts
    if len(history) > 8:
        summarized = summarize_history(history[:-4])
        history = [AIMessage(content=f"Summary of previous conversation: {summarized}")] + history[-4:]
    
    memory_store = history


def summarize_history(messages):
    """Summarize older parts of the chat to reduce token load."""
    summary_text = "\n".join(
        [f"{m.type.upper()}: {m.content}" for m in messages]
    )
    
    summary_prompt = f"""
    Summarize the following conversation in 3-4 concise bullet points
    that capture all key facts and context needed to continue it later.

    Conversation:
    {summary_text}
    """

    summary = llm.invoke(summary_prompt)
    return summary.content.strip()