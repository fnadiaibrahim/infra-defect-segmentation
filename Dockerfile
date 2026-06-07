FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    nodejs \
    npm \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/requirements.txt

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

COPY frontend/package*.json /app/frontend/

WORKDIR /app/frontend
RUN npm install

COPY frontend /app/frontend
RUN npm run build

WORKDIR /app
COPY backend /app/backend
COPY weights /app/weights
COPY docs /app/docs
COPY README.md /app/README.md

EXPOSE 7860

WORKDIR /app/backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]