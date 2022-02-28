#!/usr/bin/env bash

case $1 in
    up) docker-compose up -d --build --force-recreate;;
    up-log) docker-compose up --build --force-recreate;;
    down) docker-compose down;;
    *) echo "Invalid arg: $0 [up|down]"; exit 1;;
esac
