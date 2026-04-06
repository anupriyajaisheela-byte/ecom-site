FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app

# Install build tools and libraries required by some Python packages (eg. Pillow)
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY requirements-extra.txt .
RUN pip install --no-cache-dir -r requirements.txt -r requirements-extra.txt

# Copy app
COPY . .

# Add entrypoint (runs migrations, collectstatic, creates admin) and make executable
COPY scripts/entrypoint.sh /app/scripts/entrypoint.sh
RUN chmod +x /app/scripts/entrypoint.sh

ENV PORT 8080
EXPOSE 8080

# Entrypoint handles DB migrations and collectstatic at container start
ENTRYPOINT ["/app/scripts/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "ecom_site.wsgi:application"]
