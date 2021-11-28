# General info

A private API to manage SoftDesk's issues tracking system. 

# Usage

Consume the API requires to be authenticated, except for signup and login endpoints.

Everyone can create an account.
Every user can create a project and add/remove contributors to their project.
Every project's contributor can list and read project's issues and comments, along with creating new ones.
Only project/issue/comment's owner can modify and delete related object.

# How to use

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

## Run server

After sourcing environment, simply run
```
python manage.py runserver
```

Server will start at [http://127.0.0.1:8000](http://127.0.0.1:8000).

Database has been populated with exemple superuser, simple user and project. 

Superuser email: marie@wizardsofthecoast.com
Superuser password: recruitemeplz
Simple user email: thomas@mojo.com
Simple user password: password-oc

Feel free to delete these objects or wiping your database if needed.

# API documentation 

API documentation can be found [here](here)

# Credits

This program uses the following packages:
- Djando Rest Framework
- Nested routers
- flake8
