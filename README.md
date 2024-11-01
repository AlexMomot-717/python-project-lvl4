### Hexlet tests and linter status:

[![Actions Status](https://github.com/AlexMomot-717/python-project-lvl4/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/AlexMomot-717/python-project-lvl4/actions)
[![pre-commit hooks](https://github.com/AlexMomot-717/python-project-lvl4/actions/workflows/pre-commit.yml/badge.svg)](https://github.com/AlexMomot-717/python-project-lvl4/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/137fca5fc0b845953baf/maintainability)](https://codeclimate.com/github/AlexMomot-717/python-project-lvl4/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/137fca5fc0b845953baf/test_coverage)](https://codeclimate.com/github/AlexMomot-717/python-project-lvl4/test_coverage)

### Setup:

Install dependencies:

```
poetry install
```


Create .env file following .env.example file info.


Build and execute migrations:

```
make migrations
```

Create superuser for application administration:

```
python manage.py createsuperuser
```

Start the application with:

```
make run
```

The application will be available at http://127.0.0.1:8000.


### Setup with Docker:

Start the application with:

```
make up
```

The dockerized application will be available at http://127.0.0.1:8000.
