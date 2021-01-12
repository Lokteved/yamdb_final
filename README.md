# API Yamdb
This is a [Docker][] setup for a web application based on Django.

- The [Django][] application is served by [Gunicorn][] (WSGI application).
- [Postgres][] database is used.

[![CI Status](https://github.com/Lokteved/yamdb_final/workflows/Yamdb%20workflow/badge.svg)

## Requirements
You need to install [Docker][] and [Docker-Compose][].

## Build and run
`docker-compose up`

## Migrate database
`docker exec -it <CONTAINER ID> bash`
    then
`python manage.py loaddata fixtures.json`

[Docker]: https://www.docker.com/
[Django]: https://www.djangoproject.com/
[Gunicorn]: http://gunicorn.org/
[Postgres]: https://www.postgresql.org/
[Docker-Compose]: https://docs.docker.com/compose/
