#!/usr/bin/env bash

docker build -t webserver_docker docker_web
docker run  webserver_docker

# docker ps
# docker images 
