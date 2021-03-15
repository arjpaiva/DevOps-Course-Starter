# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses poetry for Python to create an isolated environment and manage package dependencies. To prepare your system, ensure you have an official distribution of Python version 3.7+ and install poetry using one of the following commands (as instructed by the [poetry documentation](https://safe.menlosecurity.com/https://python-poetry.org/docs/#system-requirements)):

### Poetry installation (Bash)
```bash
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
```
### Poetry installation (PowerShell)
```bash
$ (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python
```

### Dependencies
The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from your preferred shell:
```bash
$ poetry install
```

You'll also need to clone a new .env file from the .env.tempalate to store local configuration options. This is a one-time operation on first setup:
```bash
$ cp .env.template .env  # (first time only)
```

The .env file is used by flask to set environment variables when running flask run. This enables things like development mode (which also enables features like hot reloading when you make a file change). There's also a [SECRET_KEY](https://safe.menlosecurity.com/https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

### Running the App using Flask
Once the all dependencies have been installed, start the Flask app in development mode within the poetry environment by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```

Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Running the application using Gunicorn (only for Linux or Mac)

Start by exporting the properties defined on `.env` into your environment

```bash
$ export $(cat .env | grep '^[A-Z]' | xargs)
```

Then run the script:
```bash 
$ start_project_production.sh
```
Now visit [`0.0.0.0:5000/`](0.0.0.0:5000) in your web browser to view the app.

### Notes

The `.env` file is used by flask to set environment variables when running `flask run`. This enables things like developement mode (which also enables features like hot reloading when you make a file change).
* There's also a [SECRET_KEY](https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY) variable which is used to encrypt the flask session cookie.

### Troubleshooting
If the `.venv` gets corrupted, run the following command:
```bash
$ deactivate
``` 
Then remove the `.venv` directory.

### Integration with Trello

Update `.env` file to contain the relevant information to integrate with the Trello API.
Following is the mandatory fields that need to be specified:
```
# [TRELLO]
HOST=https://api.trello.com/1/boards
TRELLO_KEY=<trello_API_key>
TOKEN=<trello_API_token>
BOARD_ID=<trello_board_id> 
TODO_LIST_ID=<trello_todo_list_id>
DOING_LIST_ID=<trello_doing_list_id>
DONE_LIST_ID=<trello_donee_list_id>
```

## Vagrant
It's possible to run the application in a Virtual Machine, by using Vagrant. 

To start the the VM
```bash
$ Vagrant up
```

To ssh into the virtual machine

```bash
$ Vagrant ssh
```

To destroy the VM
```bash
$ Vagrant destroy
```

## Docker
The application can either be run using docker commands or docker-compose:

#### Docker - development environment
Build the development image:
```bash
$ docker build --target development --tag todo-app:dev .
```

or by using docker-compose: 
```bash
$ docker-compose -f docker-compose.dev.yml build
```

Run the development image:
```bash
$ docker run --mount type=bind,src="$(pwd)",target=/code -p 127.0.0.1:5000:5000 --env-file .env todo-app:dev
```

or by using docker-compose:
```bash
$ docker-compose -f docker-compose.dev.yml up
```

Both commands will bind the machines source code directory to the container and will enable to make changes in run time.

####Docker - production environment
Build the production image:
```bash
$ docker build --target production --tag todo-app:prod .
```

or by using docker-compose
```bash
$ docker-compose -f docker-compose.prod.yml build
```

Run the production image:
```bash
$ docker run -p 127.0.0.1:5000:8000 --env-file .env todo-app:prod
```

or by using docker-compose 
```bash
$ docker-compose -f docker-compose.prod.yml up
```

####Docker - test environment
Build the test image:
```bash
$ docker build --target test -t todo-app-test:test .
```

Run the test image - unit test:
```bash
$ docker run --env-file .env todo-app-test:test test/test_view_model.py
```

Run the test image - integration test:
```bash
$ docker run --env-file .env todo-app-test:test test/test_client.py
```

Run the test image - end to end test:
```bash
$ docker run --env-file .env todo-app-test:test test/test_app.py
```