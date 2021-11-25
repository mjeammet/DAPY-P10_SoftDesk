# SoftDesk

A private API to manage SoftDesk's issues tracking system. 

## Installation

### Clone from repo

```git clone https://github.com/mjeammet/DAPY-P10_SoftDesk.git```

### Preping the environment

```python -m venv env```
```source env/bin/acivate```
```pip install -r requirements.txt```

## Start server

(Source environment with: `source env/bin/activate`)

Launch server with command:
```python manage.py runserver```

Server will start at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Endpoints 

| Endpoint | HTTP method | URI | 
|-----|-----|-----|
| User sign up | POST | /signup/
| User log in | POST | /login/
| Get list of all projects linked to the connected user | GET | /projects/
| Create project (user is author) | POST | /projects/{id}
| Get proj