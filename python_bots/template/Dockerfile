FROM python:3.11-slim

WORKDIR /app

# System-Abhängigkeiten für Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    ca-certificates \
    fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m playwright install --with-deps chromium

COPY . .

# Nicht als root laufen
RUN useradd --create-home botuser
USER botuser

CMD ["python", "main.py"]
