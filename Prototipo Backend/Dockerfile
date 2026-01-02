# backend/Dockerfile
FROM python:3.11

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar el pyproject.toml y setup.cfg (si lo hubiera)
COPY pyproject.toml ./

# Instalar dependencias del proyecto
RUN pip install --no-cache-dir bcrypt \
    && pip install --no-cache-dir -e .

# Copiar el código fuente
COPY . .

# Exponer el puerto del backend
EXPOSE 8000

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
