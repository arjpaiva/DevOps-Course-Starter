FROM python:3.8

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

WORKDIR /code
COPY . /code

ENV PATH="${PATH}:/root/.poetry/bin"

EXPOSE 8000

CMD /bin/bash start_project.sh
