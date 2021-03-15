FROM python:3.8 as base

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"
WORKDIR /app

#production
FROM base as production

EXPOSE 8000
COPY . /app

ENTRYPOINT ["/bin/bash", "start_project_production.sh"]

#development
FROM base as development

EXPOSE 5000

ENTRYPOINT ["/bin/bash", "start_project_development.sh"]

#test
FROM base as test
COPY . /app

RUN apt-get -y update
RUN curl -sSL https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o chrome.deb && apt-get install ./chrome.deb -y && rm ./chrome.deb

# Install Chromium WebDriver
RUN LATEST=`curl -sSL https://chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    echo "Installing chromium webdriver version ${LATEST}" && \
    curl -sSL https://chromedriver.storage.googleapis.com/${LATEST}/chromedriver_linux64.zip -o chromedriver_linux64.zip && \
    apt-get install unzip -y && \
    unzip ./chromedriver_linux64.zip

RUN poetry install

ENTRYPOINT ["poetry", "run", "pytest"]
