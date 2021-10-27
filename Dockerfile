FROM python:3.9-buster

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    bash \
    build-essential \
    gcc \
    libffi-dev \
    musl-dev \
    openssl \
    postgresql \
    libpq-dev 

COPY requirements-dev.txt requirements-dev.txt
RUN pip3 install -r requirements-dev.txt

COPY manage.py ./manage.py
COPY . /app

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


