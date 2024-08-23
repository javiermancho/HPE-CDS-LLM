# Automated BOE Query Project

This project implements a microservices architecture to query the Spanish Official State Gazette (BOE) using natural language processing. The services are designed to interact with each other, providing a scalable and efficient solution for searching and querying official documents.

![chat image](chat.png)

## Index 
1. [Architecture](#architecture)
   - [1. BOE-Script](#1-boe-script)
   - [2. Database](#2-database)
   - [3. Embeddings](#3-embeddings)
   - [4. LLM (Large Language Model)](#4-llm-large-language-model)
   - [5. Server](#5-server)
   - [6. Client](#6-client)
2. [Installation and Configuration](#installation-and-configuration)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
   - [Configuration](#configuration)
3. [Usage](#usage)

## Architecture

The project architecture consists of the following microservices:

### 1. BOE-Script
- **Description**: This service is responsible for downloading BOE PDF files up to the current date and storing them in a database. It also saves the PDF files in a local directory called `/pdf`.
- **Technology**: Python
- **Functionality**:
  - Downloads the most recent BOEs.
  - Stores the PDFs in a database and the `/pdf` directory.
- **Endpoints**:
    - GET /update-pdf: Checks if the PDFs are up to date. If not, it downloads them up to the current date.
    - GET /last-date: Returns the date of the last downloaded day.

### 2. Database
- **Description**: This service manages the storage and retrieval of BOE documents in chunk format (text fragments). It receives the PDF files, divides them into chunks, and generates embeddings for storage. It also allows querying the most relevant chunks based on a query and a date range.
- **Technologies**: Python, ChromaDB, LangChain
- **Functionality**:
  - Divides PDFs into manageable chunks.
  - Generates embeddings for each chunk and stores them along with the ID, content, and date.
  - Allows queries to return the 3 most relevant chunks based on the provided query and date range.
- **Endpoints**:
    - POST /store: Handles receiving the PDF. It receives the following parameters in its body:
        ```JSON
        {
            "date": "01-01-2024",
            "id": "BOE-A-2024-1",
            "content": "PDF Content"
        }
        ```
    - POST /query: Receives the user's question and the dates for querying. It receives the following parameters in its body:
        ```JSON
        {
            "query": "User question",
            "dateInit": "01-01-2024",
            "dateEnd": "31-01-2024"
        }
        ```

### 3. Embeddings
- **Description**: Service responsible for receiving text chunks and returning their corresponding embeddings. Embeddings are numerical vectors that represent the semantic content of the text.
- **Technology**: Python, GPT4All
- **Functionality**:
  - Receives text chunks.
  - Generates embeddings corresponding to each chunk.

- **Endpoints**: 
    - POST /embeddings: Receives a text string to convert it into embeddings. 
        ```JSON
        {
            "content": "Chunk PDF"
        }
        ```

### 4. LLM (Large Language Model)
- **Description**: Service based on a large language model (LLM) that receives queries from the server and generates responses using the chunks provided by the database service. The core of the service is LLaMA 2.
- **Technology**: Python, llama-cpp-python, Llama2
- **Functionality**:
  - Receives queries and the relevant chunks.
  - Constructs responses based on the chunks.
- **Endpoints**:
    - POST /llama: Request to the LLM that contains the user's prompt and the maximum number of response tokens. The structure is as follows:
        ```JSON
        {
            "system_message": "System Message",
            "user_message": "User Prompt + Chunks",
            "max_tokens": "1024"
        }
        ```
> [!IMPORTANT]  
> You must download **llama-2-7b-chat.Q2_K.gguf** from [Huggingface](https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF). Once downloaded, save it in /LLM folder. 

### 5. Server
- **Description**: Central service that coordinates the interaction between the client and the other microservices. It receives queries from the client along with the dates and is responsible for requesting the relevant chunks from the database and generating a response with the help of the LLM.
- **Technology**: SpringBoot
- **Functionality**:
  - Coordinates communication between the client and backend services.
  - Manages query requests and returns responses to the client.
- **Endpoints**: 
    - POST /llama: Request that contains the user's question and the provided date range. The structure is as follows: 
        ```JSON
            {
                "message": "User Message",
                "dateStart": "Initial Date",
                "dateEnd": "End Date"
            }
        ```

### 6. Client
- **Description**: User interface that allows users to interact with the system through a chat. Users can make queries about the BOE.
- **Technologies**: React, NextJS
- **Functionality**:
  - Provides a chat interface for users to ask questions.
  - Sends the queries and dates to the server to get relevant responses.

## Installation and Configuration

To deploy this project, follow these steps:

### Prerequisites
- **Docker**

### Installation

1. **Clone the repository**:
    ```bash
    git clone git@github.com:javiermancho/HPE-CDS-LLM.git
    ```

3. **Build Docker Compose**:
    - **Build the containers**:
        ```bash
        cd HPE-CDS-LLM
        docker compose build --no-cache
        ```
    - **Run Docker Compose**:
        ```bash
        docker compose up
        ```

## Usage

1. **Start the microservices**: Ensure all microservices are running.
2. **Access the client**: Open the browser and navigate to `http://localhost:3000`.
3. **Query the BOE**: Use the chat interface to make queries about the BOE. The system will process the query and return the most relevant results. It includes the following features:
    - Update the database with the latest BOEs.
    - Set the date range for the query.
![Chat with guidelines](chat-with-guidelines.png)
