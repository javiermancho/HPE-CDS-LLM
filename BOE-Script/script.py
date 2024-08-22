import requests
import os
import json
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
import pdfplumber

# Create flask app
app = Flask("BOE-Script")


# Configure path to save PDFs
output_folder = "pdfs"
os.makedirs(output_folder, exist_ok=True)

# Obtain actual date
global ACTUAL_DATE 
ACTUAL_DATE = datetime.now()
global LAST_DATE
# Obtain last date from config.json
with open('./pdfs/config.json') as json_file:
    data = json.load(json_file)
    LAST_DATE = data['last_pdf_date']
    LAST_DATE = datetime.strptime(LAST_DATE, "%Y%m%d")


# Function to save PDFs
def download_pdf(pdf_url, date_str, unique_id):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        date_folder = os.path.join(output_folder, date_str)
        os.makedirs(date_folder, exist_ok=True)
        pdf_filename = os.path.join(date_folder, f"{unique_id}.pdf")
        
        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(response.content)         

        texto_pdf = ''
        with pdfplumber.open(pdf_filename) as pdf:
            for pagina in pdf.pages:
                texto_pdf += pagina.extract_text() or ''  # Añade texto de cada página
        body = {
            "date": date_str,
            "id": unique_id,
            "content": texto_pdf
        }
        response = requests.post("http://chromadb:5000/store", json=body)

        print(f"PDF guardado: {pdf_filename}")
    else:
        print(f"Error al descargar el PDF {pdf_url}: {response.status_code}")

# Recursive function to find PDFs in JSON data
def find_pdfs_in_json(data, date_str):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == "texto" and isinstance(value, str) and value.endswith(".pdf"):
                unique_id = data.get('identificador', 'unknown')
                if unique_id == 'unknown':
                    unique_id = os.path.basename(value).replace(".pdf", "")
                download_pdf(value, date_str, unique_id)
            else:
                find_pdfs_in_json(value, date_str)
    elif isinstance(data, list):
        for item in data:
            find_pdfs_in_json(item, date_str)

# Function to fetch and save PDFs for a given date
def fetch_and_save_pdfs(date_str):
    url = f"https://boe.es/datosabiertos/api/boe/sumario/{date_str}"
    headers = {
        'Accept': 'application/json' 
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        find_pdfs_in_json(json_data, date_str)
    else:
        print(f"Error fetching data for {date_str}: {response.status_code}")
        print(response.text)

# Save PDFs into the database


@app.route("/last-date", methods=["GET"])
def get_last_date():
    return {"last_date": LAST_DATE.strftime("%Y%m%d")}  # Convert to string for response


# /update-pdf endpoint to update PDFs
@app.route("/update-pdf", methods=["GET"])
def update_pdf():
    global LAST_DATE
    global ACTUAL_DATE

    while LAST_DATE <= ACTUAL_DATE:
        fetch_and_save_pdfs(LAST_DATE.strftime("%Y%m%d"))
        LAST_DATE += timedelta(days=1)
    
    with open('config.json', 'w') as json_file:
        data = {
            "last_pdf_date": LAST_DATE.strftime("%Y%m%d")  # Save as string in the correct format
        }
        json.dump(data, json_file)

    return {"message": "Download Complete"}


# Main function
if __name__ == "__main__":
    app.run(host= "0.0.0.0", port=5002, debug=True)
