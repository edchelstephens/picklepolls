FROM python:3.13-slim-bookworm

WORKDIR /app

COPY _requirements ./_requirements

RUN pip install -r _requirements/dev.txt

COPY project ./project



CMD ["python", "project/manage.py", "runserver", "0.0.0.0:8000"]