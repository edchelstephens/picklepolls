![PicklePolls](assets/images/PicklePolls.png)


# PicklePolls


A Django-based polling application built with Python.

## Features

* Create and manage polls
* Add questions and choices options
* Vote on polls
* View poll results
* Django-powered backend
* Automated testing with pytest
* Selenium-based functional tests
* CI/CD with GitHub Actions

## Tech Stack

* Python
* Django
* PostgreSQL
* HTML / CSS
* JavaScript
* pytest
* Selenium
* GitHub Actions



## Getting Started

### 1. Clone the repository

```bash
git clone <repository-url>
cd PicklePolls
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**macOS / Linux**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r _requirements/dev.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```
## Running with Docker

### Locally
1. Install Docker
2. Run this command to build docker image locally:
```
docker image build -t picklepolls .
```
3. Spawn a container of the image:
```
docker run --env-file .env -it  --rm -p 8080:8000 picklepolls
```
4. Visit the app at http://127.0.0.1:8080/


## Running with docker-compose

1. Build the containers and run with this command
```
sudo docker compose -f local.yml up --build
```
or run in daemon mode:
```
sudo docker compose -f local.yml up --build -d
```

### Deployment
### With Docker
1. Install Docker
2. Build the production image:
```
docker image build -f Dockerfile.prod -t picklepolls .
```
3. Spawn a container of the image in dameon mode:
```
docker run --env-file .env -it  --rm -d -p 8080:8000 picklepolls
```
4. Update ngix config to listen to proxy_pass http://127.0.0.1:8020

### With Docker Compose
1. Install docker-compose if not yet available, then check version
```
sudo apt update
sudo apt install docker-compose-v2

sudo docker compose version
```

2. Build and run the production.yml docker compose file
```
sudo docker compose -f production.yml up --build -d
```

## Testing

Run the test suite with pytest:

```bash
pytest
```

Run tests with coverage:

```bash
coverage run -m pytest
coverage report
```

## Development

The project uses Django's standard development workflow. After making model changes, create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## CI

The project includes GitHub Actions for automated testing.

The CI pipeline runs the test suite automatically to help ensure changes do not introduce regressions.

## License

This project is for educational and development purposes.
