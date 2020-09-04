#!/bin/bash

# Create and enable a virtual environment
python3 -m venv --clear env

# Upgrade pip and install required packages
pip install --upgrade pip
pip install -r requirements.txt

# Create a .env file from the .env.template
cp -n .env.template .env
