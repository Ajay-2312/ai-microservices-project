import os
from flask import Flask, request, jsonify
from langchain_openai import ChatOpenAI # Changed import
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
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

prompt = PromptTemplate(
    input_variables=["topic"],
    template="""
    Create a detailed, step-by-step learning path for a beginner to learn about "{topic}".
    The learning path should include the following sections:
    1.  **Introduction**: A brief overview of the topic.
    2.  **Fundamentals**: The core concepts and prerequisites.
    3.  **Intermediate Topics**: More advanced concepts and skills.
    4.  **Advanced Topics**: Expert-level concepts and specializations.
    5.  **Practical Projects**: Ideas for projects to apply the learned skills.
    
    For each topic in the path, provide a brief explanation and suggest some resources.
    Structure the output in Markdown format.
    """
)

learning_path_chain = LLMChain(llm=llm, prompt=prompt)

@app.route('/learning-path', methods=['POST'])
def suggest_learning_path():
    data = request.get_json()
    if not data or 'topic' not in data:
        return jsonify({"error": "No topic provided"}), 400

    topic = data['topic']
    response = learning_path_chain.invoke({"topic": topic})
    
    return jsonify(response) # Keep as is, LLMChain often returns a dict

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)