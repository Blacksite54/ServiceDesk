FROM python:3.11-slim-buster

WORKDIR /ServiceDesk

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["celery", "-A", "api.main.celery", "worker", "-l", "info", "--pool=prefork", "-Q", "default,notify_worker"]

ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=admin
ENV POSTGRES_DB=sakura

RUN apt-get update && apt-get install -y postgresql postgresql-contrib

COPY create_db.sql /docker-entrypoint-initdb.d/

EXPOSE 5432

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]