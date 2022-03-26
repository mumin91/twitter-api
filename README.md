# Prerequisits
**Docker** and **docker-compose** must be installed to run the project.

# How to run the project

1. Clone the project: `git clone https://github.com/mumin91/twitter-api.git`
2. Go to project root: `cd twitter-api`
3. Run: `docker-compose up`. The service will be up and can be accessed through `http://localhost:8000/`.
4. Access to container CMD where Django is running: `docker exec -it django_container bash`
5. Run migrations: `python manage.py migrate`
6. Run manage commnad for dummy users: `python manage.py create_users`. It will creates some users in the database. User data is printed after the commnad which can be used later for accessing the APIs.
7. Use `Postman` or anything else to access the API.
