FROM python:3.12-slim

WORKDIR /app

# Install dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app and the pre-built vector store
COPY app.py .
COPY vector_db/ ./vector_db/

EXPOSE 7860

CMD ["python", "app.py"]