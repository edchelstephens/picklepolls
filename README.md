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

## Project Structure

```text
PicklePolls/
├── assets/
│   └── images/
│       └── PicklePolls.png
├── polls/
│   ├── models/
│   ├── tests/
│   ├── views/
│   └── ...
├── picklepolls/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
├── pytest.ini
└── README.md
```

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
