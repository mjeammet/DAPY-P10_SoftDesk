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
| Create project (user is author) | POST | /projects/
| Get projet's details | GET | /projects/{project_id}
| Update a project (author only) | PUT | /projects/{project_id}
| Delete project (author only) | DELETE | /projects/{project_id}
| Add a contributor to project | POST | /projects/{project_id}/users/
| Get a list of project's contributors | GET | /projects/{project_id}/users/
| Remove a user from project | DELETE | /projects/{project_id}/users/{contribution_id} (! not user_id !)
| Get list of project's issues |  GET | /projects/{project_id}/issues/
| Create an issue for the project | POST | /projects/{project_id}/issues/
| Update an issue | PUT | /projects/{project_id}/issues/{issue_id}
| Delete an issue | DELETE | /projects/{project_id}/issues/{issue_id}
| Create comments on an issue | POST | /projects/{project_id}/issues/{issue_id}/comments/
| Get list of issue's related comments | GET | /projects/{project_id}/issues/{issue_id}/comments/
| Update a comment | PUT | /projects/{project_id}/issues/{issue_id}/comments/{comment_id}
| Remove a comment | DELETE | /projects/{project_id}/issues/{issue_id}/comments/{comment_id}
| Retrieve a comment | GET | /projects/{project_id}/issues/{issue_id}/comments/{comment_id}
