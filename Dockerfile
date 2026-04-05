FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libc-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn
COPY . .
EXPOSE 8080
CMD ["gunicorn", "--bind", ":8080", "--workers", "2", "ecom_site.wsgi:application"]
# Add this line to run our admin script
RUN python manage.py shell < create_admin.py