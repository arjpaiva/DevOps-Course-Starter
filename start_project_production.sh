#!/bin/bash

poetry run gunicorn --bind 0.0.0.0:${PORT:-8000} "app:create_app()"