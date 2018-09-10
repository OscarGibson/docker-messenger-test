if [[ $1 ]]; then
	echo "Recreating ${1}"
	docker exec $1 python manage.py recreate_db
else
	echo "Recreating users-db"
	docker exec users-service python manage.py recreate_db
	echo "Recreating projects-db"
	docker exec projects-service python manage.py recreate_db
	echo "Recreating sections-db"
	docker exec sections-service python manage.py recreate_db
	echo "Recreating sub-sections-db"
	docker exec sub-sections-service python manage.py recreate_db
	echo "Recreating ideas-db"
	docker exec ideas-service python manage.py recreate_db
fi