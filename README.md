# Project
This is my final project for __SDAcademy__ course __Python from scratch__.
It runs on `Docker` and uses `Django` with `PostgreSQL`.

# Running this project
- First you need to install [Docker](https://docs.docker.com/get-docker/).
- You need to clone this repository: https://github.com/mihsim/django_project_management.git
- On terminal you need to cd into the main folder of this project. It has Dockerfile and docker-compose.yml
- You need to run following commands:
  ```
  $ docker-compose build
  $ docker-compose up
  $ docker-compose run web python3 manage.py migrate
  ```
- In your browser open: [http://localhost:8000/](http://localhost:8000/)
  
