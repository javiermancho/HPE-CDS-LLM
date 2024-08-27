from flask import Flask, request, jsonify
#from langchain_community.embeddings.spacy_embeddings import SpacyEmbeddings
from sentence_transformers import SentenceTransformer

import torch



app = Flask("Embeddings server")

#embedder = SpacyEmbeddings(model_name="en_core_web_sm")
model = SentenceTransformer("jinaai/jina-embeddings-v2-base-es")
model.max_seq_length = 1024



@app.route("/embeddings", methods=['POST'])
def get_embedding():
    text = request.json["content"]
    if not text:
        return ValueError("The 'text' parameter is required"), 400

    # query_result = embedder.embed_query(text)
    
    embeddings = model.encode(text)
    return jsonify({"embeddings": embeddings.tolist()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
