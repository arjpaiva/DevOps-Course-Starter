FROM python:3.8 as base

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
WORKDIR /code

#production
FROM base as production

EXPOSE 8000
COPY . /code

CMD /bin/bash start_project_production.sh

#development
FROM base as development

EXPOSE 5000
COPY . /code

CMD /bin/bash start_project_development.sh