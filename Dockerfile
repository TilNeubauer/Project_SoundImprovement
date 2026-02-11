FROM python:3.12-slim

#python3-tk tk | für GUI (Bib: tkinter)
#libportaudio2 portaudio19-dev | für Bib: sounddevice
#ffmpeg libsndfile1 | für Bib: pydub
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-tk tk \
    libportaudio2 portaudio19-dev \
    libasound2 libasound2-plugins \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir pdm

COPY pyproject.toml pdm.lock ./

ENV PDM_VENV_IN_PROJECT=0
RUN pdm config python.use_venv false
RUN pdm install --prod --no-editable --no-self

COPY . .

CMD ["pdm", "run", "python", "main_gui.py"]
