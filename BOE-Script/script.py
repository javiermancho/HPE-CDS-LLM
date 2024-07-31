import requests
import os
import json
from datetime import datetime, timedelta

# Configurar la carpeta de destino principal
output_folder = "pdfs"
os.makedirs(output_folder, exist_ok=True)

# Función para descargar y guardar PDFs
def download_pdf(pdf_url, date_str, unique_id):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        date_folder = os.path.join(output_folder, date_str)
        os.makedirs(date_folder, exist_ok=True)
        pdf_filename = os.path.join(date_folder, f"{unique_id}.pdf")
        with open(pdf_filename, 'wb') as pdf_file:
            pdf_file.write(response.content)
        print(f"PDF guardado: {pdf_filename}")
    else:
        print(f"Error al descargar el PDF {pdf_url}: {response.status_code}")

# Función para buscar recursivamente en el JSON todas las URLs de PDFs
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

# Función para obtener y guardar los PDFs de una fecha específica
def fetch_and_save_pdfs(date_str):
    url = f"https://boe.es/datosabiertos/api/boe/sumario/{date_str}"
    headers = {
        'Accept': 'application/json'  # Añadir la cabecera Accept
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        find_pdfs_in_json(json_data, date_str)
    else:
        print(f"Error fetching data for {date_str}: {response.status_code}")
        print(response.text)

# Fecha inicial y final para el año 2024
start_date = datetime.strptime("20240101", "%Y%m%d")
end_date = datetime.strptime("20240701", "%Y%m%d")

# Iterar sobre cada día del año 2024
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime("%Y%m%d")
    print(f"Fetching data for {date_str}")
    fetch_and_save_pdfs(date_str)
    current_date += timedelta(days=1)

print("Descarga completa.")
