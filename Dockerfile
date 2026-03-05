FROM mcr.microsoft.com/playwright/python:latest

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

CMD ["gunicorn", "app:app"]
