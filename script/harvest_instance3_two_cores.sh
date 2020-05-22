# Launch twitter harvester process
echo "Harvesting twitter data..."
time mpiexec -n 2 python3 ../harvest/tweet_harvester.py -a ../harvest/authenConfig.json -f ../harvest/filterConfig.json -d ../harvest/databaseConfig.json -m tweetid