FROM python:3.10-slim-buster
ENV PYTHONUNBUFFERED=1
ENV PATH = "/scripts:${PATH}"

RUN apt-get update && apt-get install -y postgresql-server-dev-all gcc python3-dev musl-dev


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN mkdir /app
COPY . /app
WORKDIR /app

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser appuser
RUN chown -R appuser:appuser /vol
RUN chmod -R 755 /vol/web
USER appuser

RUN python manage.py collectstatic --noinput

EXPOSE 8010

CMD ["gunicorn", "--bind", "0.0.0.0:8010", "danaproject.wsgi"]