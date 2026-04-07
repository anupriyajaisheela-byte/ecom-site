FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# 1. Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Upgrade core tools and install Gunicorn/Setuptools in one go
# Adding setuptools here ensures it's available for the Gunicorn install
RUN pip install --no-cache-dir --upgrade pip setuptools wheel gunicorn

# 3. Install requirements
COPY requirements.txt requirements-extra.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements-extra.txt

# 4. Copy application code
COPY . .

# 5. Setup Entrypoint
RUN chmod +x /app/scripts/entrypoint.sh

# 6. Port configuration
ENV PORT 10000
EXPOSE 10000

ENTRYPOINT ["/app/scripts/entrypoint.sh"]

# 7. Fixed Gunicorn command
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "2", "ecom_site.wsgi:application"]