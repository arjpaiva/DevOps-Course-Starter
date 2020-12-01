FROM python:3.8

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /code
COPY poetry.lock pyproject.toml templates .env app.py card.py start_project.sh trello_service.py view_model.py /code/
COPY . /code

ENV PATH="${PATH}:/root/.poetry/bin"

EXPOSE 5000

CMD /bin/bash start_project.sh
