FROM mcr.microsoft.com/playwright/python:1.45.0-jammy

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app"]
