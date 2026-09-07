FROM python:3.13-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY _requirements ./_requirements

RUN pip install -r _requirements/dev.txt

COPY project ./project

WORKDIR /app/project

EXPOSE 8000

COPY entrypoint.local.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT [ "/entrypoint.sh" ]