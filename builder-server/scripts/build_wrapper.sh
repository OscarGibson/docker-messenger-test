if ./scripts/docker_build.sh $1; then
	echo "--- ALL CONTAINERS BUILD SUCCESSFULLY"
else
	echo "ERROR WHEN BUILDING CONTAINERS"
	exit 1
fi