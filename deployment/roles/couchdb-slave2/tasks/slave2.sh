## Cluster setup
 
# The following instructions apply only to Linux-based systems; for MacOS please move to the `macos` directory and execute `run.sh`. 

# Set node IP addresses, electing the first as "master node"
# and admin credentials (make sure you have no other Docker containers running):

export slavenode=172.26.133.31
export size=1
export user=couchdb
export pass=password
export VERSION='3.0.0'


if [ ! -z $(docker ps --all --filter "name=couchdb${slavenode}" --quiet) ] 
  then
    docker stop $(docker ps --all --filter "name=couchdb${slavenode}" --quiet) 
    docker rm $(docker ps --all --filter "name=couchdb${slavenode}" --quiet)
fi

docker rmi -f ibmcom/couchdb3:${VERSION}
docker pull ibmcom/couchdb3:${VERSION}

# Create Docker containers (stops and removes the current ones if existing): 

docker create\
  --name couchdb${slavenode}\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env NODENAME=couchdb${slavenode}\
  ibmcom/couchdb3:${VERSION}


# Put in conts the Docker container IDs:

declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

docker exec "couchdb${slavenode}" bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"

docker exec "couchdb${slavenode}" bash -c "echo \"-name couchdb@${slavenode}\" >> /opt/couchdb/etc/vm.args"

# Start the containers (and wait a bit while they boot):

docker start "couchdb${slavenode}"