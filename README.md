![PicklePolls](assets/images/PicklePolls.png)

# 🥒 PicklePolls

A Django-based polling application built with Python.

---

## ✨ Features

* 📊 Create and manage polls
* ❓ Add questions and choices options
* 🗳️ Vote on polls
* 📈 View poll results
* 🐍 Django-powered backend
* 🧪 Automated testing with pytest
* 🌐 Selenium-based functional tests
* 🚀 CI/CD with GitHub Actions

---

## 🛠️ Tech Stack

* 🐍 Python
* 🌐 Django
* 🐘 PostgreSQL
* 🎨 HTML / CSS , Tailwind CSS
* ⚡ JavaScript
* 🧪 pytest
* 🌐 Selenium
* 🚀 GitHub Actions

---

# 🚀 Getting Started

## 1. 📥 Clone the repository

```bash
git clone <repository-url>
cd PicklePolls
```

## 2. 🐍 Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

### 🍎 macOS / 🐧 Linux

```bash
source .venv/bin/activate
```

### 🪟 Windows

```bash
.venv\Scripts\activate
```

## 3. 📦 Install dependencies

```bash
pip install -r _requirements/dev.txt
```

## 4. 🗄️ Run migrations

```bash
python manage.py migrate
```

## 5. ▶️ Start the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

# 🐳 Running with Docker

## 💻 Locally

1. Install Docker.

2. Build the Docker image locally:

```bash
docker image build -t picklepolls .
```

3. Spawn a container of the image:

```bash
docker run --env-file .env -it --rm -p 8080:8000 picklepolls
```

4. Visit the app at:

```text
http://127.0.0.1:8080/
```

---

# 🐳 Running with Docker Compose

1. Build the containers and run:

```bash
sudo docker compose -f local.yml up --build
```

Or run in daemon mode:

```bash
sudo docker compose -f local.yml up --build -d
```

---

# 🚀 Deployment

## 🐳 With Docker

1. Install Docker.

2. Build the production image:

```bash
docker image build -f Dockerfile.prod -t picklepolls .
```

3. Spawn a container of the image in daemon mode:

```bash
docker run --env-file .env -it --rm -d -p 8080:8000 picklepolls
```

4. Update nginx config to listen to:

```text
proxy_pass http://127.0.0.1:8020
```

---

## 🐳 With Docker Compose

### 1. 📦 Install Docker Compose

Install docker-compose if not yet available, then check the version:

```bash
sudo apt update
sudo apt install docker-compose-v2

sudo docker compose version
```

### 2. 🚀 Build and run the production Docker Compose file

```bash
sudo docker compose -f production.yml up --build -d
```

---

# 🗄️ PostgreSQL with Docker Compose

## 💻 Local

Run the database first:

```bash
sudo docker compose -f local.yml up db
```

## 🚀 Production Initialization

Make sure:

```text
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

Then start the database:

```bash
sudo docker compose -f production.yml up db
```

### 🐚 Execute Bash on the Container

```bash
sudo docker exec -it <container_id> bash
```

### 🐘 Run psql

```bash
psql -U postgres
```

### 👤 Create the Database and User

Create the database and the user, then grant privileges:

```sql
CREATE USER <user_name>;

ALTER USER <user_name> WITH PASSWORD '<password>';

CREATE DATABASE <db_name>;

GRANT ALL PRIVILEGES ON DATABASE <db_name> TO <user_name>;

\c <db_name>;

GRANT ALL ON SCHEMA public TO <user_name>;
```

---

# 🧪 Testing

## ▶️ Run the Test Suite

Run the test suite with pytest:

```bash
pytest
```

## 📊 Run Tests with Coverage

# Important:
1. If running on local machine to spawn selenium browser test, you must export POSTGRES_HOST=localhost to use local postgresql database, instead of docker database.

2. Also, you must run collect static since now the engine is whitenoise

```bash
export LOCAL_UNIT_TESTS=True && export POSTGRES_HOST=localhost
coverage run -m pytest
coverage report
```

## 🌐 Run Full Coverage Report and Open in Chrome

```bash
coverage run -m pytest -sv && coverage report && coverage html && open -a 'Google Chrome' htmlcov/index.html
```

---

# 👨‍💻 Development

The project uses Django's standard development workflow.

After making model changes, create and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 🤖 CI/CD

The project includes GitHub Actions for automated testing and deployment.

The CI pipeline:

* 🧪 Runs the test suite automatically to help ensure changes do not introduce regressions.
* 🚀 Automatically deploys on merge to the production branch.

---

# 📄 License

This project is for educational and development purposes.
