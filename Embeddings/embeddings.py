from flask import Flask, request, jsonify
from langchain_community.embeddings import GPT4AllEmbeddings


app = Flask("Embeddings server")

gpt4all_embd = GPT4AllEmbeddings()

@app.route("/embeddings", methods=['POST'])
def get_embedding():
    text = request.json["content"]
    if not text:
        return ValueError("The 'text' parameter is required"), 400

    query_result = gpt4all_embd.embed_query(text)
    
    return jsonify({"embeddings": query_result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
