#!/bin/bash

ROOT_DIR="$(pwd)"

if [[ $1 ]]; then
	ssh-add -D
	# clone users-service
	if [ -d $2 ]; then
		echo "Pull ${1}..."
		ssh-add ".ssh/${1}"
		cd "../${1}"
		git pull
		echo "...done"
	fi
else
	# remove all identies
	ssh-add -D
	ssh-add .ssh/$USERS_SERVICE_DIR
	# clone users-service
	if [ ! -d "../${USERS_SERVICE_DIR}" ]; then
		echo "Cloning users-service..."
		git clone git@bitbucket.org:squiber/squibler-be.git "../${USERS_SERVICE_DIR}"
		echo "...done"
	else
		echo "Pull users-service..."
		cd "../${USERS_SERVICE_DIR}"
		git pull
		cd $ROOT_DIR
		echo "...done"
	fi

	# clone projects-service
	ssh-add -D
	ssh-add .ssh/$PROJECTS_SERVICE_DIR
	if [ ! -d "../${PROJECTS_SERVICE_DIR}" ]; then
		echo "Cloning projects-service..."
		git clone git@bitbucket.org:squiber/squibler-be-book.git "../${PROJECTS_SERVICE_DIR}"
		echo "...done"
	else
		echo "Pull projects-service..."
		cd "../${PROJECTS_SERVICE_DIR}"
		git pull
		cd $ROOT_DIR
		echo "...done"
	fi

	ssh-add -D
	ssh-add .ssh/$SECTIONS_SERVICE_DIR
	# clone sections-service
	if [ ! -d "../${SECTIONS_SERVICE_DIR}" ]; then
		echo "Cloning sections-service..."
		git clone git@bitbucket.org:squiber/squibler-be-section.git "../${SECTIONS_SERVICE_DIR}"
		echo "...done"
	else
		echo "Pull sections-service..."
		cd "../${SECTIONS_SERVICE_DIR}"
		git pull
		cd $ROOT_DIR
		echo "...done"
	fi

	ssh-add -D
	ssh-add .ssh/$SUB_SECTIONS_SERVICE_DIR
	# clone sub-sections-service
	if [ ! -d "../${SUB_SECTIONS_SERVICE_DIR}" ]; then
		echo "Cloning sub-sections-service..."
		git clone git@bitbucket.org:squiber/squibler-be-sub-sections.git "../${SUB_SECTIONS_SERVICE_DIR}"
		echo "...done"
	else
		echo "Pull sub-sections-service..."
		cd "../${SUB_SECTIONS_SERVICE_DIR}"
		git pull
		cd $ROOT_DIR
		echo "...done"
	fi

	ssh-add -D
	ssh-add .ssh/$IDEAS_SERVICE_DIR
	# clone ideas-service
	if [ ! -d "../${IDEAS_SERVICE_DIR}" ]; then
		echo "Cloning ideas-service..."
		git clone git@bitbucket.org:squiber/squibler-be-ideas.git "../${IDEAS_SERVICE_DIR}"
		echo "...done"
	else
		echo "Pull ideas-service..."
		cd "../${IDEAS_SERVICE_DIR}"
		git pull
		cd $ROOT_DIR
		echo "...done"
	fi

	ssh-add -D
	ssh-add .ssh/$UPLOAD_SERVICE_DIR
	# clone upload-service
	if [ ! -d "../${UPLOAD_SERVICE_DIR}" ]; then
		echo "Cloning upload-service..."
		git clone git@bitbucket.org:squiber/squibler-upload.git "../${UPLOAD_SERVICE_DIR}"
		echo "...done"
	else
		echo "Pull upload-service..."
		cd "../${UPLOAD_SERVICE_DIR}"
		git pull
		cd $ROOT_DIR
		echo "...done"
	fi

	ssh-add -D
	ssh-add .ssh/$WEB_SERVICE_DIR
	# clone web-service
	if [ ! -d "../${WEB_SERVICE_DIR}" ]; then
		echo "Cloning web-service..."
		git clone git@bitbucket.org:squiber/squiber-fe.git --single-branch -b refactor "../${WEB_SERVICE_DIR}"
		echo "...done"
	else
		echo "Pull web-service..."
		cd "../${WEB_SERVICE_DIR}"
		git pull
		cd $ROOT_DIR
		echo "...done"
	fi

	ssh-add -D
	ssh-add .ssh/$SWAGGER_SERVICE_DIR
	# clone swagger-service
	if [ ! -d "../${SWAGGER_SERVICE_DIR}" ]; then
		echo "Cloning swagger-service"
		git clone git@bitbucket.org:squiber/squibler-be-swagger.git "../${SWAGGER_SERVICE_DIR}"
		echo "...done"
	else
		echo "Pull swagger-service"
		cd "../${SWAGGER_SERVICE_DIR}"
		git pull
		cd $ROOT_DIR
		echo "...done"
	fi
fi