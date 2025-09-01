import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI # Changed import
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA

load_dotenv(dotenv_path='../.env')

if os.getenv("OPENROUTER_API_KEY") is None:
    raise ValueError("OPENROUTER_API_KEY is not set in the root .env file.")
if os.getenv("OPENROUTER_MODEL_NAME") is None: # New check
    raise ValueError("OPENROUTER_MODEL_NAME is not set in the root .env file.")

app = Flask(__name__)

qa_chain = None

def initialize_qa_chain():
    global qa_chain
    print("Initializing QA Chain...")
    
    loader = DirectoryLoader('./documents/', glob="**/*.txt")
    documents = loader.load()
    if not documents:
        print("WARNING: No documents found in ./documents/ folder.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    docs = text_splitter.split_documents(documents)

    print("Loading embedding model (this may take a moment on first run)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    print("Creating vector store...")
    vectorstore = FAISS.from_documents(docs, embeddings)

    # Initialize the Chat Model from OpenRouter using ChatOpenAI
    llm = ChatOpenAI(
        openai_api_base="https://openrouter.ai/api/v1", # OpenRouter base URL
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        model_name=os.getenv("OPENROUTER_MODEL_NAME") # Use model from .env
    )

    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    print("QA Chain Initialized Successfully!")


@app.route('/qa', methods=['POST'])
def query_document():
    if qa_chain is None:
        return jsonify({"error": "QA chain is not initialized. Ensure documents exist in the /documents folder."}), 500

    data = request.get_json()
    if not data or 'question' not in data:
        return jsonify({"error": "Missing 'question'"}), 400

    question = data['question']
    response = qa_chain.invoke({"query": question})
    
    return jsonify(response) # Keep as is, RetrievalQA often returns a dict

if __name__ == '__main__':
    initialize_qa_chain()
    app.run(host='0.0.0.0', port=5002)