# Dockerfile - Proto-Tipo Frontend (Simple Dev Server)
FROM node:20-alpine

# Instalar pnpm
RUN npm install -g pnpm

WORKDIR /app

# Copiar package.json y pnpm-lock.yaml
COPY package.json pnpm-lock.yaml ./

# Instalar dependencias
RUN pnpm install --frozen-lockfile

# Copiar código fuente
COPY . .

# Exponer puerto 5173
EXPOSE 5173

# Ejecutar Vite dev server con --host para escuchar en todas las interfaces
CMD ["pnpm", "dev", "--host", "0.0.0.0"]
