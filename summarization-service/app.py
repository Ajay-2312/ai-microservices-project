import os
from flask import Flask, request, jsonify
from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI # Changed import
from langchain.docstore.document import Document
from dotenv import load_dotenv

load_dotenv(dotenv_path='../.env')

if os.getenv("OPENROUTER_API_KEY") is None:
    raise ValueError("OPENROUTER_API_KEY is not set in the root .env file.")
if os.getenv("OPENROUTER_MODEL_NAME") is None: # New check
    raise ValueError("OPENROUTER_MODEL_NAME is not set in the root .env file.")

app = Flask(__name__)

# Initialize the Chat Model from OpenRouter using ChatOpenAI
llm = ChatOpenAI(
    openai_api_base="https://openrouter.ai/api/v1", # OpenRouter base URL
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    model_name=os.getenv("OPENROUTER_MODEL_NAME") # Use model from .env
)

summarize_chain = load_summarize_chain(llm, chain_type="stuff")

@app.route('/summarize', methods=['POST'])
def summarize_text():
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400

    doc = Document(page_content=data['text'])
    response = summarize_chain.invoke({'input_documents': [doc]})

    return jsonify({"summary": response.get('output_text')}) # Adjusted for ChatOpenAI response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)