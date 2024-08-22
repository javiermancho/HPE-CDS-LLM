# Usa una imagen base oficial de Python
FROM python:3.9-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el archivo de requerimientos en el contenedor
COPY requirements.txt .

# Instala las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt
# Instala el modelo de spaCy
RUN python -m spacy download en_core_web_sm

# Copia el código fuente de la aplicación al directorio de trabajo
COPY . .

# Expone el puerto en el que la aplicación Flask estará disponible
EXPOSE 5000

# Comando para ejecutar la aplicación Flask
CMD ["python", "database.py"]
