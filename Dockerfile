FROM python:3.13-slim-bookworm

WORKDIR /app

COPY _requirements ./_requirements

RUN pip install -r _requirements/dev.txt

COPY project ./project
COPY .env ./.env
COPY .gitignore ./.gitignore

CMD ["python", "project/manage.py", "runserver"]