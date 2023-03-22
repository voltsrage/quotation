FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

