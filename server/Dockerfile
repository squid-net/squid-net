FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "-w", "1", "--threads", "100", "--bind", "0.0.0.0:6969", "app:app"]
