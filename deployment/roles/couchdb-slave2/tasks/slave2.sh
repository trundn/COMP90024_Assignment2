## Cluster setup
 
# The following instructions apply only to Linux-based systems; for MacOS please move to the `macos` directory and execute `run.sh`. 

# Set node IP addresses, electing the first as "master node"
# and admin credentials (make sure you have no other Docker containers running):

export declare -a nodes=(172.26.134.18)
export slavenode=172.26.134.18
export size=${#nodes[@]}
export user=couchdb
export pass=password
export VERSION='3.0.0'
export cookie='a192aeb9904e6590849337933b000c99'
export uuid='a192aeb9904e6590849337933b001159'



docker pull ibmcom/couchdb3:${VERSION}


# Create Docker containers (stops and removes the current ones if existing):


if [ ! -z $(docker ps --all --filter "name=couchdb${slavenode}" --quiet) ] 
  then
    docker stop $(docker ps --all --filter "name=couchdb${slavenode}" --quiet) 
    docker rm $(docker ps --all --filter "name=couchdb${slavenode}" --quiet)
fi 

docker create\
  --name couchdb${slavenode}\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env NODENAME=couchdb@${slavenode}\
  --env COUCHDB_SECRET=${cookie}\
  --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${slavenode}\""\
  ibmcom/couchdb3:${VERSION}


# Put in conts the Docker container IDs:

declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)


# Start the containers (and wait a bit while they boot):

for cont in "${conts[@]}"; do docker start ${cont}; done