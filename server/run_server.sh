#!/bin/bash

#services="user/user-service.py"
services="user/user-service.py location/location-service.py game/game-service.py gameuser/game-user-service.py lobby/lobby-service.py"

devflag="-d"

for service in $services; do
  echo "Starting $service"
  (./service/run_service.sh $devflag $service &)
done
