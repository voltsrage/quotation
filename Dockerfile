FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8010

CMD ["gunicorn", "--bind", "0.0.0.0:8010", "danaproject.wsgi"]