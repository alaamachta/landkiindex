# Dockerfile
FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "crawler.py"]
