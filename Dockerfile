FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies including browser dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libxml2-dev \
    libxslt-dev \
    libffi-dev \
    libssl-dev \
    curl \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libatspi2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \
    libxtst6 \
    xvfb \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY ./vendor/cloudscrapper /app/vendor/cloudscrapper

RUN pip install /app/vendor/cloudscrapper

# Copy application code
COPY app.py .
COPY test.py .

# Install Playwright browsers (must be done as root)
RUN npm install playwright && npm install -g n && n stable

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

RUN npx playwright install
RUN npx playwright install chromium

# Expose port
EXPOSE 3002

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=5 \
    CMD curl -f http://localhost:3002/health || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:3002", "--workers", "4", "--timeout", "120", "app:app"]