# Portfolio_Project — SICIP Job 2
## Setup (Windows)
```bat
py -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
py manage.py makemigrations Portfolio
py manage.py migrate
py manage.py createsuperuser
py manage.py runserver
```
Open http://127.0.0.1:8000/ . The superuser/staff account manages the portfolio at `/dashboard/`.
Includes registration, username/email login, logout, Profile, Skill, Project, Experience, Education, CRUD dashboard, CV/Resume, Crispy Forms with Bootstrap 5, static/media settings, profile/project images and multiple project attachments (any extension). Attachments download rather than display inline.
