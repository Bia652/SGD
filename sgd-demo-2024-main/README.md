# Sistema de Gestão de Dados  - Trabalho Prático

The code and resources available in this repository are to be used only in the scope of the _SGD 2024_ course.

The main purpose of this repository is to provide examples on how to do the the initial setup of the database-centric REST API that must be developed for the assignment. 
In particular, the projects available are totally automated to be easily deployed in third-party setups with the help of a tool (in this case `docker` or maven, depending on the project).

_The contents of this repository do not replace the proper reading of the assignment description._


## Overview of the Contents

- [**`PostgreSQL`**](postgresql) - Database ready to run in a `docker` container with or without the help of the `docker-compose` tool;
- [**`Python`**](python) - Source code of web application template in python with `docker` container configured. Ready to run in `docker-compose` with PostgreSQL
  - [`app/`](python/app) folder is mounted to allow developing with container running
- [**`postman`**](postman) - A collection of requests exported of postman tool;


## Requirements

The requirements described here are needed if you want to run using Docker. If not, you can follow the instructions described [**`here`**](python).

To execute this project using Docker, it is required to have installed:

- `docker`
- `docker-compose`


## Demo [Python](python) REST API 


To start this demo with run the script (e.g. [`./docker-compose-python-psql.sh`](docker-compose-python-psql.sh)) to have both the server and the database running.
This script uses `docker-compose` and follows the configurations available in [`docker-compose-python-psql.yml`](docker-compose-python-psql.yml)).

The folder [`app`](python/app) is mapped into the container. 
You can modify the contents and the server will update the sources without requiring to rebuild or restart the container.

* Web browser access: http://localhost:8080


## Authors

* SGD 2024 Team
* University of Coimbra
