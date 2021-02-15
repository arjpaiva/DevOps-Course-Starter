#!/bin/bash

poetry install
poetry run gunicorn --bind 0.0.0.0:8000 "app:create_app()"