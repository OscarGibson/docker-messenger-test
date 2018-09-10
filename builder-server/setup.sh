#!/bin/bash

# setup all variables
export JAMES_SERVICE_DIR="james-service"
export NINA_SERVICE_DIR="nina-service"

export DOCKER_COMPOSE_FILE="scripts/docker-compose.yml"

if [[ $1 -eq "pull" ]] ; then
	./scripts/pull_wrapper.sh $2
elif [[ $1 -eq "build" ]]; then
	./scripts/build_wrapper.sh $2
elif [[ $1 -eq "recreate-db" ]]; then
	./scripts/docker_create_db.sh $2
else
	./scripts/pull_wrapper.sh
	./scripts/build_wrapper.sh
	./scripts/docker_create_db.sh
fi
