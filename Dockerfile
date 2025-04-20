FROM python:3.10-slim

WORKDIR /app

# Instale dependências do sistema
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    libsndfile1 \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Clone o repositório TTS
RUN git clone https://github.com/coqui-ai/TTS.git /app

# Instale o TTS com suporte a XTTS
RUN pip install -e ".[all,xtts]"
RUN pip install gradio

# Crie o diretório para modelos
RUN mkdir -p ~/.local/share/tts/

# Baixe os modelos pré-treinados
RUN wget https://huggingface.co/coqui/XTTS-v2/resolve/main/model.pth -P ~/.local/share/tts/
RUN wget https://huggingface.co/coqui/XTTS-v2/resolve/main/config.json -P ~/.local/share/tts/
RUN wget https://huggingface.co/coqui/XTTS-v2/resolve/main/vocab.json -P ~/.local/share/tts/

# Copie o arquivo server.py
COPY server.py /app/server.py

# Exponha a porta
EXPOSE 7860

# Comando para iniciar o servidor
CMD ["python", "server.py"]
