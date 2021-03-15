#!/bin/bash

poetry install
echo $1
poetry run pytest $1