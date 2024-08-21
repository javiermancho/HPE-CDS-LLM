# Usaremos una imagen oficial de Python como base
FROM python

# Fijamos el directorio de trabajo del contenedor
WORKDIR /app

# Copiamos dentro el script que hace que funcione como servidor
COPY ./llama_cpu_server.py /app/llama_cpu_server.py
COPY ./llama-2-7b-chat.Q4_K_M.gguf /app/llama-2-7b-chat.Q4_K_M.gguf

# Instalamos cualquier paquete necesario especificado en requirements.txt
RUN pip install llama-cpp-python
RUN pip install Flask

# Exponemos el puerto 5000 para conectarnos al contenedor
EXPOSE 5000

# Ejecutamos el servidor python cuando se inicie el contenedor
CMD ["python", "llama_cpu_server.py"]