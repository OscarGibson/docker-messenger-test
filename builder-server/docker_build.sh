names_file="container-names"

declare -A container

while IFS=':' read -r container_name dir_name || [[ -n "$container_name" ]]; do
    if [[ ${container_name:0:1} != "#" ]] && [[ ${container_name:0:1} != "" ]]; then
    	container[${container_name}]=$dir_name
    fi
done < "$names_file"


export USER_CONTAINER_DIR=${container[users-service]}
export PROJECT_CONTAINER_DIR=${container[projects-service]}
export SECTION_CONTAINER_DIR=${container[sections-service]}
export IDEAS_CONTAINER_DIR=${container[ideas-service]}
export SUB_CONTAINER_DIR=${container[sub-sections-service]}
export WEB_CONTAINER_DIR=${container[web-service]}
export SWAGGER_CONTAINER_DIR=${container[swagger-service]}
export UPLOAD_CONTAINER_DIR=${container[upload-service]} 


if [[ $1 ]]; then
	docker-compose up -d --build $1
else
	docker-compose up -d --build users-db
	docker-compose up -d --build users-service
	echo "--- ${container[users-service]} ---"
	docker-compose up -d --build projects-db
	docker-compose up -d --build projects-service
	docker-compose up -d --build sections-db
	docker-compose up -d --build sections-service
	echo "--- ${container[sections-service]} ---"
	docker-compose up -d --build ideas-db
	docker-compose up -d --build ideas-service
	echo "--- ${container[ideas-service]} ---"
	docker-compose up -d --build sub-sections-db
	docker-compose up -d --build sub-sections-service
	echo "--- ${container[sub-sections-service]} ---"
	echo "--- ${container[upload-service]} ---"
	docker-compose up -d --build upload-service
	docker-compose up -d --build web-service
	echo "--- ${container[web-service]} ---"
	docker-compose up -d --build swagger-service
	echo "--- ${container[swagger-service]} ---"
	docker-compose up -d --build nginx-service
fi








