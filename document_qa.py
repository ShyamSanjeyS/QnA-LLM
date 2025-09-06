import os
import tempfile

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_community.llms import CTransformers

import chainlit as cl
from chainlit.types import AskFileResponse

# ✅ Local Embeddings using Sentence Transformers
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# ✅ Local LLM using CTransformers and .gguf model (like Mistral)
llm = CTransformers(
    model="models/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    model_type="mistral",  # or 'llama' if using LLaMA2
    config={
        "max_new_tokens": 512,
        "temperature": 0.7,
        "context_length": 2048
    }
)

# 🔪 Split documents into manageable chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)

# Welcome message shown in Chainlit UI
welcome_message = """📄 Welcome to the Offline Chainlit PDF QnA Bot!

1. Upload a PDF or text file 📑
2. Ask any question based on its content 🤖
"""

# 📄 Load and split uploaded file
def process_file(file):
    if file.type == "text/plain":
        loader = TextLoader(file.path)
    elif file.type == "application/pdf":
        loader = PyPDFLoader(file.path)
    else:
        raise ValueError("Unsupported file type")

    documents = loader.load()
    docs = text_splitter.split_documents(documents)

    for i, doc in enumerate(docs):
        doc.metadata["source"] = f"source_{i}"

    return docs

# 🧠 Build vector DB with local embeddings
def get_docsearch(file: AskFileResponse):
    docs = process_file(file)
    cl.user_session.set("docs", docs)

    return Chroma.from_documents(
        documents=docs,
        embedding=embeddings
    )

# 🟢 Chat session start
@cl.on_chat_start
async def start():
    await cl.Message(content="🟢 Ready to chat with your PDFs!").send()

    files = await cl.AskFileMessage(
        content=welcome_message,
        accept=["text/plain", "application/pdf"],
        max_size_mb=20,
        timeout=180
    ).send()

    file = files[0]
    msg = cl.Message(content=f"📥 Processing `{file.name}`...")
    await msg.send()

    docsearch = await cl.make_async(get_docsearch)(file)
    print("✅ Docsearch completed.")

    # Retrieval chain setup
    chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever()
    )

    cl.user_session.set("chain", chain)

    msg.content = f"✅ `{file.name}` is ready! Ask your question below."
    await msg.update()

# 💬 User message handling
@cl.on_message
async def main(message):
    try:
        chain = cl.user_session.get("chain")
        docs = cl.user_session.get("docs")

        response = await cl.make_async(chain.invoke)(message.content)

        answer = response["result"]
        sources = response.get("source_documents", [])
        source_elements = []

        if sources:
            for doc in sources:
                source_elements.append(
                    cl.Text(content=doc.page_content, name=doc.metadata.get("source", "source"))
                )

        await cl.Message(content=answer, elements=source_elements).send()

    except Exception as e:
        await cl.Message(content=f"❌ Error: {str(e)}").send()
