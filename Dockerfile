FROM python:3.12-slim-bullseye

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf var/lib/apt/lists/*

    COPY requierments.txt /app/

    RUN pip install --no-cache-dir -r requierments.txt

    COPY . /app/

   RUN python manage.py collectstatic --noinput

   EXPOSE 8000

  ENTRYPOINT ['gunicorn','dating_app.wsgi','-b','0.0.0.0:8000']