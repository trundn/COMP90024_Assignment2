## Cluster setup
 
# The following instructions apply only to Linux-based systems; for MacOS please move to the `macos` directory and execute `run.sh`. 

# Set node IP addresses, electing the first as "master node"
# and admin credentials (make sure you have no other Docker containers running):

export slavenode=172.26.133.31
export size=1
export user=couchdb
export pass=password
export VERSION='3.0.0'

echo="here 1"
docker pull ibmcom/couchdb3:${VERSION}

sleep 2m

# Create Docker containers (stops and removes the current ones if existing):

echo="here 2"

docker create\
  --name couchdb${slavenode}\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env NODENAME=couchdb@${slavenode}\
  ibmcom/couchdb3:${VERSION}


# Put in conts the Docker container IDs:

echo="here 3"

declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

docker exec "couchdb${slavenode}" bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"

sleep 2m

docker exec "couchdb${slavenode}" bash -c "echo \"-name couchdb@${slavenode}\" >> /opt/couchdb/etc/vm.args"

sleep 2m

# Start the containers (and wait a bit while they boot):

docker start "couchdb${slavenode}"