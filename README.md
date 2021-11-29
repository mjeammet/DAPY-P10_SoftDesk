# General info

A private API to manage SoftDesk's issues tracking system. 

# Usage

## Installation

```
# Clone this repo
$ git clone https://github.com/mjeammet/DAPY-P10_SoftDesk.git

# Create environment
$ python -m venv env

# Activate environment
$ python -m pip install --upgrade pip

# Upgrade pip and install packages into the environment to ensure proper behaviour:
$ source env/bin/acivate
$ pip install -r requirements.txt
```

## Create database

In order to initialise database, use commands
```
# To write migrations files
$ python manage.py makemigrations issues_tracker

# Migrate
$ python manage.py migrate
```

Your database is now created but empty. You can use signup endpoint to create users or create superuser with:
```
$ python manage.py createsuperuser
```

## Run server

After sourcing environment, simply run
```
$ python manage.py runserver
```

Server will start at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Features and permissions

| Action | Permission |
|-|-|
| Create an account | Everyone |
| Login | Everyone |
| Create a project | Every authenticated user |
| Add/remove contributors to project | Project owner |
| Create issues and comments | Project contributor |
| List/read issues and comments | Project contributor |
| Modify or delete project, issue and comment | Project/Issue/Comment author |
| * | Superuser |

# API documentation 

API documentation can be found on [https://documenter.getpostman.com/view/17508081/UVJbJy2v](https://documenter.getpostman.com/view/17508081/UVJbJy2v)

# Credits

This program uses the following packages:
- Djando Rest Framework
- Nested routers
- flake8
