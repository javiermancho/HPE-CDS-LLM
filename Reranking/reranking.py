from flask import Flask, request, jsonify
from transformers import pipeline

app = Flask(__name__)

# Cargar el modelo de reranking
model_name = "bert-base-uncased"
rerank_model = pipeline("text-classification", model=model_name)

@app.route("/rerank", methods=["POST"])
def rerank():
    try:
        data = request.json

        query = data.get("query")
        documents = data.get("documents")
        ids = data.get("ids")
        dates = data.get("date")

        print(data)

        if not query or not documents or not ids or not dates:
            return jsonify({"status": "error", "message": "Missing required parameters"}), 400
        
        # Realiza el reranking usando la consulta y los documentos
        reranked_scores = [rerank_model({"text": query, "text_pair": doc})[0]['score'] for doc in documents]


        
        # Asociar las puntuaciones con los documentos
        scored_documents = list(zip(reranked_scores, ids, documents, dates))
        # Ordenar los documentos en base a las puntuaciones
        sorted_documents = sorted(scored_documents, key=lambda x: x[0], reverse=True)

        # Crear la respuesta con los documentos ordenados
        response = {
            "status": "ok",
            "documents": [doc for _, _, doc, _ in sorted_documents],
            "ids": [doc_id for _, doc_id, _, _ in sorted_documents],
            "dates": [date for _, _, _, date in sorted_documents]
        }

        return jsonify(response)

    except Exception as e:
        # Registro detallado del error
        app.logger.error(f"Error during reranking: {str(e)}")
        return jsonify({"status": "error", "message": "An error occurred during reranking"}), 500
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
