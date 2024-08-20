# Usa una imagen base oficial de PostgreSQL
FROM postgres:latest

# Instala las dependencias necesarias para construir pgvector
RUN apt-get update && \
    apt-get install -y \
    git \
    build-essential \
    postgresql-server-dev-all && \
    rm -rf /var/lib/apt/lists/*

# Clona el repositorio pgvector, construye e instala la extensión
RUN git clone https://github.com/pgvector/pgvector.git && \
    cd pgvector && \
    make && \
    make install
