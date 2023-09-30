FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN pip install poetry==1.6.1 && poetry config virtualenvs.create false

WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install

COPY . .
RUN rm -r nginx
RUN mkdir media
RUN python manage.py collectstatic --no-input


EXPOSE 80

CMD export && python manage.py migrate && (gunicorn --log-level debug --bind 0.0.0.0:80 config.wsgi & celery -A config worker -l DEBUG)
