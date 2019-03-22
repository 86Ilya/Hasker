#!/usr/bin/env bash

docker-compose -f docker-compose.yml build
docker-compose -f docker-compose.yml up -d db
# TODO
sleep 5
docker-compose -f docker-compose.yml up web
docker-compose -f docker-compose.yml stop db
