
# Mind Map API

MindMap api service with FastAPI

For the API usage you can consult the swagger at `<HOST>/docs` (ie using the run.sh: `http://localhost:8080/docs`)

### How to run

You need docker and docker-compose

using the `run.sh`
```shell script
sh bin/run.sh
```

using the whole command :p
```shell script
docker-compose up --build
```

### How to run tests

Run the tests in the docker container
```shell script
docker-compose up --build -d
docker-compose exec api pytest --cov=. ./
```

### How to run linter

```shell script
flake8 src/
```


### How to access database

```shell script
docker-compose exec db psql --username=postgres_user --dbname=mindmap
```

### Setup dev env

1. Create venv  
This project uses pipenv for dependencies.

```shell script
pip install pipenv

pipenv --python 3.9
cd src/ && pipenv install & pipenv shell
```

* you can also use the generated requirements.txt * 
```shell script
cd src/
pip install -r requirements.txt
```

Generate requirements.txt

```shell script
pipenv lock --requirements > requirements.txt
```
