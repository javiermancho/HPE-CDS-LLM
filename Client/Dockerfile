# Etapa 1: Construcción de la aplicación
FROM node:18-alpine AS builder

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar package.json y package-lock.json
COPY chat-app/package*.json ./

# Instalar las dependencias del proyecto
RUN npm install

# Copiar el código fuente de la aplicación
COPY chat-app/. .

# Construir la aplicación Next.js
RUN npm run build

# Instalar 'serve' para servir la aplicación en modo de producción
RUN npm install -g serve

# Etapa 2: Ejecución de la aplicación
FROM node:18-alpine AS runner

WORKDIR /app

# Copiar la carpeta .next generada en la etapa anterior
COPY --from=builder /app/.next .next

# Copiar la carpeta public y otros archivos necesarios
COPY --from=builder /app/public ./public
COPY --from=builder /app/package*.json ./

# Instalar solo las dependencias de producción
RUN npm install --only=production

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 3000

# Comando para ejecutar la aplicación en producción
CMD ["npm", "start"]
