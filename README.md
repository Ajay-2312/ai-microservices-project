# AI Microservices with LangChain and OpenRouter

This project demonstrates a modular, microservice-based architecture for deploying AI functionalities. It provides three distinct services, each with its own API endpoint, all powered by open-source large language models accessed via the OpenRouter API.

## Features

1.  **Text Summarization Service:** Provides a concise summary of any given text.
2.  **Q&A Over Documents Service:** Answers questions based on the content of text files placed in its `documents` directory.
3.  **Dynamic Learning Path Service:** Generates a detailed, step-by-step study guide for any user-specified topic.

##Setup and Installation

This project uses a Python virtual environment to manage dependencies and avoid conflicts.

1. **Clone the Repository & Navigate:**

   ```bash
   git clone https://github.com/Ajay-2312/ai-microservices-project.git
   cd ai-microservices-project
   ```

2. **Create the Virtual Environment:**

   ```bash
   py -m venv venv
   ```
   
3. **Activate the Environment:**

   ```bash
   .\venv\Scripts\Activate.ps1
   ```
   
4. **Create Your .env File:**

   Create a file named `.env` in the root of the project and add your OpenRouter API key and the desired model name:```
   OPENROUTER_API_KEY="your_api_key_here"
   OPENROUTER_MODEL_NAME="mistralai/mistral-7b-instruct"
   
5. **Install Dependencies:**

   ```bash
   py -m pip install -r .\summarization-service\requirements.txt
   py -m pip install -r .\qa-service\requirements.txt
   py -m pip install -r .\learning-path-service\requirements.txt
   ```
   
6. **Run the Services:**

   Open three separate terminals. In each terminal, activate the virtual environment (`.\venv\Scripts\Activate.ps1`) and run one of the following commands:
   
   - Terminal 1 (Summarization): `py .\summarization-service\app.py`
   - Terminal 2 (Q&A): `py .\qa-service\app.py`
   - Terminal 3 (Learning Path): `py .\learning-path-service\app.py`

## API Endpoint Documentation

A Postman collection (postman_collection.json) is included in this repository for easy testing. Import it into Postman to test the endpoints below.

1. **Summarize Text**
   
   **URL:** `http://localhost:5001/summarize`
   **Method:** `POST`
   **Body (JSON):**

   ```JSON
   {
    "text": "Your long text to summarize goes here..."
   }
   ```

2. **Ask a Question**
   
   **URL:** `http://localhost:5002/qa`
   **Method:** `POST`
   **Body (JSON):**

   ```JSON
   {
    "question": "What is the core idea of LangChain?"
   }
   ```

3. **Generate Learning Path**

   **URL:** `http://localhost:5003/learning-path`
   **Method:** `POST`
   **Body (JSON):**

   ```JSON
   {
    "topic": "Quantum Computing"
   }
   ```
