FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "crawler.py"]
