#!/bin/bash

# Use this option to run the server outside development mode
#export FLASK_APP=server.py

# Enable this option to run in development mode
# 1) Activates debugger
# 2) Activates automatic reloader
# 3) Enables debug mode in Flash app
export FLASK_ENV=development

flask run
