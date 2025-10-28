from dotenv import load_dotenv
import os
from src.prompt import *
from src.helper import *
import chainlit as cl
from uuid import uuid4
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.runnables import RunnableMap, RunnablePassthrough
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import shutil

if os.path.exists("./chroma_langchain_db"):
    shutil.rmtree("./chroma_langchain_db")

load_dotenv()

embeddings = load_embedding()

memory_store = []

llm = ChatMistralAI(
    model="mistral-large-latest",
    temperature=0.7,
    max_retries=2,
    # other params...
)

vector_store = Chroma(
    collection_name="example_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_langchain_db",
)

retriever = vector_store.as_retriever()

prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant that answers using both chat history and provided documents."),
        MessagesPlaceholder("history"),
        ("human", "Context:\n{context}\n\nQuestion: {question}")
    ])

chain = (
    RunnableMap({
        "history": lambda _: load_history(memory_store),
        "context": lambda x: retriever.invoke(x["question"]),
        "question": RunnablePassthrough(),
    })
    | prompt
    | llm
    | StrOutputParser()
)

@cl.on_chat_start
async def start():
    await cl.Message(content="Welcome! Send a GitHub repo link to ingest or ask a question.").send()

@cl.on_message
async def handle_message(message: cl.Message):
    user_input = message.content.strip()

    # Handle "clear"
    if user_input.lower() == "clear":
        os.system("rm -rf repo")
        await cl.Message(content="🧹 Repository folder cleared!").send()
        return

    # If it looks like a GitHub link -> treat as repo ingestion
    if "github.com" in user_input:
        await cl.Message(content="🔄 Ingesting repository...").send()
        try:
            repo_path = repo_ingestion(user_input)
            os.system(f"python store_index.py {repo_path}")
            await cl.Message(content="✅ Repository ingested successfully!").send()
        except Exception as e:
            await cl.Message(content=f"❌ Error during ingestion: {e}").send()
        return

    # Otherwise, treat as normal chat
    await cl.Message(content="🤔 Thinking...").send()
    try:
        result = response = chain.invoke({"question": user_input})
        print("Response:\n", response)
        await cl.Message(content=str(result)).send()
    except Exception as e:
        await cl.Message(content=f"❌ Error during QA: {e}").send()


