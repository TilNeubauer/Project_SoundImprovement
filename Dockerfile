# syntax=docker/dockerfile:1
FROM python:3.12-slim

# Optional: Systempakete
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# PDM installieren
RUN pip install --no-cache-dir pdm

# Nur Dependency-Files zuerst kopieren
COPY pyproject.toml pdm.lock ./

# PDM so konfigurieren, dass es NICHT in ein venv installiert, sondern ins System im Container
ENV PDM_VENV_IN_PROJECT=0
RUN pdm config python.use_venv false

# Dependencies installieren (ohne dein Projekt als Paket)
RUN pdm install --prod --no-editable --no-self

# Code kopieren
COPY . .

# run 
CMD ["pdm", "run", "python", "main_gui.py"]