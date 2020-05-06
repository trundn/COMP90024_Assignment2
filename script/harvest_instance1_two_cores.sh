# Launch twitter harvester process
echo "Harvesting twitter data..."
time mpiexec -n 2 python3 tweet_harvester.py -a authenConfig.json -f filterConfig.json -d databaseConfig.json -m stream