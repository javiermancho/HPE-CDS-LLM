import chromadb
import requests
from flask import Flask, request, jsonify
import base64
import numpy as np
# from sentence_transformers import CrossEncoder


#from langchain_text_splitters import SpacyTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# model = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2', max_length=1024)


app = Flask("ChromaDB")

# Text splitter initialization
# text_splitter = SpacyTextSplitter(chunk_size=1024)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024,
    chunk_overlap=200,
    length_function=len,
    is_separator_regex=False,
    separators=[
        "\n\n",
        "\n",
        "\uff0e",  # Fullwidth full stop
        "\u3002"  # Ideographic full stop
    ],
)

# Client initialization for the database in path "files"
client = chromadb.PersistentClient(path="files")

# Collection loading
CDB = client.get_or_create_collection("ChromaDB")

# Class definition for the chunks
class Chunk:
    def __init__(self, id, date, content, embedding):
        self.id = id
        self.date = date
        self.content = content
        self.embedding = embedding

    def getEmbedding(self):
        return self.embedding
    def getContent(self):
        return self.content
    def getDate(self):
        return self.date
    def getId(self):
        return self.id
    def obtainEmbeddingFromRequest(self, request):
        return request.json()["embeddings"]


@app.route("/store", methods=["POST"])
def store():
    # Parameters validation
    id = request.json["id"]
    date = request.json["date"]
    content = request.json["content"]
    chunks = text_splitter.split_text(content)

    # Chunk processing 
    chunks_obj = list()
    i = 0
    for chunk in chunks:
        embeddings = requests.post("http://embeddings:5001/embeddings", json={"content": chunk}, timeout=30)
        embeddings = embeddings.json()["embeddings"]
        #print(embeddings)
        temp = Chunk(
            f"{id}-{i}", 
            date, 
            chunk, 
            embeddings
        )
        i = i + 1
        chunks_obj.append(temp)

    # Chunk storage in the database 
    for chunk in chunks_obj:
        CDB.add(
            ids=chunk.getId(),
            embeddings=chunk.getEmbedding(),
            documents = chunk.getContent(),
            metadatas=[
                {"date": int(chunk.getDate())}]
        )


    return jsonify({"status": "ok"})

@app.route("/getData", methods=["POST"])
def retrieve_by_date():    
    try:
        # Return all the data from the database 
        all_results = CDB.get(include=['embeddings', 'documents', 'metadatas'])  
        if not all_results:
            return jsonify({"status": "not found"}), 404

        # Response Format
        response = {
            "status": "ok",
            "data": all_results
        }
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }

    return jsonify(response)

# Database cleaning
@app.route("/cleanData", methods=["POST"])
def clean():
    all_results = CDB.get()["ids"]
    CDB.delete(ids=all_results)
    return jsonify({"status": "ok"})


@app.route("/query", methods=["POST"])
def query():
    # Parameters validation
    query_original = request.json["query"]
    if not query_original:
        return jsonify({"error": "Query parameter is required"}), 400
    try:
        # Obtain embeddings for the query
        query = requests.post("http://embeddings:5001/embeddings", json={"content": query_original}, timeout=30)
        query = query.json()["embeddings"]
        dateInit = request.json["dateInit"]
        dateEnd = request.json["dateEnd"]
        # Obtain the closest document to the query from the database
        dateInit = int(dateInit)
        dateEnd = int(dateEnd)
        query_result = CDB.query(
            query_embeddings=query, 
            n_results=3,
            where={
                "$and": [
                    {"date": {"$gte": dateInit}},
                    {"date": {"$lte": dateEnd}}
                ]
            }
         )
        if (not query_result.get("ids") or all(len(id_list) == 0 for id_list in query_result.get("ids"))):
            return jsonify({"status": "not found"}), 404
        # try:
        #     documents = query_result.get("documents")[0]
        #     if not documents:
        #         return jsonify({"status": "no documents to rerank"}), 404
            
        #     score = model.predict([query_original], documents[2])
        #     # scores = model.predict([([[query_original], doc]) for doc in documents])
        #     return score
        # except Exception as e:
        #     error_message = str(e)
        #     return jsonify({"status": "error", "message": error_message}), 500
        
        # Response format
        response = {
            "status": "ok",
            "ids" : query_result.get("ids"),
            "content": query_result.get("documents"),
            "date": query_result.get("metadatas")
        }

       

        # reranked = requests.post("http://reranking:5006/rerank", json=response)
        # 
        return jsonify(response), 200
    # Handle exceptions
    except Exception as e:
        response = {
            "status": "error",
            "message": str(e)
        }
        return jsonify(response), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)

