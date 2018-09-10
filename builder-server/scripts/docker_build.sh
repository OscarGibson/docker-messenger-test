#!/bin/bash

if [[ $1 ]];then
	echo "--- Building single container ---"
	echo "...${1}"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build $1
else
	echo "--- Building all containers ---"
	echo "...users-db"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build users-db
	echo "...users-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build users-service
	echo "...projects-db"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build projects-db
	echo "...projects-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build projects-service
	echo "...sections-db"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build sections-db
	echo "...sections-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build sections-service
	echo "...sub-sections-db"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build sub-sections-db
	echo "...sub-sections-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build sub-sections-service
	echo "...ideas-db"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build ideas-db
	echo "...ideas-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build ideas-service
	echo "...upload-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build upload-service
	echo "...web-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build web-service
	echo "...swagger-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build swagger-service
	echo "...nginx-service"
	docker-compose -f $DOCKER_COMPOSE_FILE up -d --build nginx-service
fi