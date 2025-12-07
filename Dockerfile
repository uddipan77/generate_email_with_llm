# Dockerfile
# Location: generate_email_with_llm/Dockerfile

# Use a slim Python image
FROM python:3.11-slim

# Install system build tools (needed for packages like chromadb / hnswlib)
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential && \
    rm -rf /var/lib/apt/lists/*

# Workdir inside the container
WORKDIR /app

# Copy dependency list and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code (including app/, README, image, etc.)
COPY app ./app
COPY output_cold_email.png README.md ./

# Streamlit runs on port 8501 by default
EXPOSE 8501

# Environment defaults for Streamlit
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Start the Streamlit app
CMD ["streamlit", "run", "app/main.py"]
