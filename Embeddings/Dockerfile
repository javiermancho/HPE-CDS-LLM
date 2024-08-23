# Usar una imagen base de Python oficial
FROM python:3.10-slim

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar el archivo de requisitos (si existe) y el código fuente al contenedor
COPY requirements.txt requirements.txt
COPY . .

RUN apt-get update && apt-get install -y build-essential

# Instalar las dependencias necesarias
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

# Exponer el puerto 5001 para que Flask pueda ser accesible desde fuera del contenedor
EXPOSE 5001

# Comando para ejecutar la aplicación Flask
CMD ["python", "embeddings.py"]
