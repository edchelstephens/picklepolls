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

3. With postgres on docker compose. Run the database first

for local

```
sudo docker compose -f local.yml up db
```

## for production on initialization
make sure 
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

```
sudo docker compose -f production.yml up db
```
Execute bash on the container

```
sudo docker exec -it <container_id> bash
```

Run psql
```
psql -U postgres
```

Create the database and the user, grant priviledges
```
CREATE USER <user_name>;

ALTER USER <user_name> WITH PASSWORD '<password>';

CREATE DATABASE <db_name>;

GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <user_name>;
\c <db_name>;
GRANT ALL ON SCHEMA public TO <user_name>;

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

Run full command with coverage report on chrome
```
coverage run -m pytest -sv && coverage report && coverage html && open -a 'Google Chrome' htmlcov/index.html
```

## Development

The project uses Django's standard development workflow. After making model changes, create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

## CI

The project includes GitHub Actions for automated testing and deployment.
The CI pipeline runs the test suite automatically to help ensure changes do not introduce regressions and automatically deploys on merge to production branch.

## License

This project is for educational and development purposes.
