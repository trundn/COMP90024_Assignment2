# Launch twitter harvester process
echo "Harvesting twitter data..."
time mpiexec python3 tweet_harvester.py -a authenConfig.json -f filterConfig.json