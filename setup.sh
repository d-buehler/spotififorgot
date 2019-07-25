#!/bin/bash

# Create a new virtualenv
virtualenv env --python=python3

# Activate the virtualenv
source env/bin/activate

# Install requirements
pip install -r requirements.txt
