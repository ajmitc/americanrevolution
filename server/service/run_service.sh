#!/bin/bash

# > run_service.sh [-d] user/userservice.py
setupDevEnv=0
while [ $# -gt 0 ]; do
    case $1 in
      -d) setupDevEnv=1
      ;;
      *) service="$1"
      ;;
    esac
    shift
done

export FLASK_APP=service/$service

# Enable this option to run in development mode
# 1) Activates debugger
# 2) Activates automatic reloader
# 3) Enables debug mode in Flash app
if [[ "$setupDevEnv" == "1" ]]; then
  export FLASK_ENV=development
fi

flask run
