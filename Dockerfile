FROM python:latest

WORKDIR /app

RUN apt-get update

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt && pip install gunicorn

COPY . .
WORKDIR /app/src

CMD ["gunicorn", "referal_system.wsgi:application", "--bind", "0.0.0.0:8000"]
