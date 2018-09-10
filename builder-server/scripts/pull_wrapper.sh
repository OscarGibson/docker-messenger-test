if ./scripts/git_pull.sh $1; then
	echo "--- ALL REPOSITORIES DOWNLOADED SUCCESSFULLY ---"
else
	echo "ERROR WHEN DOWNLOADING REPOSITORIES"
	exit 1
fi