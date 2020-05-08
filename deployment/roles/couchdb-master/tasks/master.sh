## Cluster setup
 
# The following instructions apply only to Linux-based systems; for MacOS please move to the `macos` directory and execute `run.sh`. 

# Set node IP addresses, electing the first as "master node"
# and admin credentials (make sure you have no other Docker containers running):

export declare -a nodes=(172.26.134.18 172.26.132.175 172.26.133.31)
export masternode=172.26.134.18
export declare -a othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=1
export user=couchdb
export pass=password
export VERSION='3.0.0'

docker rmi -f ibmcom/couchdb3:${VERSION}
docker pull ibmcom/couchdb3:${VERSION}


# Create Docker containers (stops and removes the current ones if existing):

if [ ! -z $(docker ps --all --filter "name=couchdb${masternode}" --quiet) ] 
  then
    docker stop $(docker ps --all --filter "name=couchdb${masternode}" --quiet) 
    docker rm $(docker ps --all --filter "name=couchdb${masternode}" --quiet)
fi 

docker create\
  --name couchdb${masternode}\
  --env COUCHDB_USER=${user}\
  --env COUCHDB_PASSWORD=${pass}\
  --env NODENAME=couchdb@${masternode}\
  ibmcom/couchdb3:${VERSION}


# Put in conts the Docker container IDs:

declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

docker exec "couchdb${masternode}" bash -c "echo \"-setcookie couchdb_cluster\" >> /opt/couchdb/etc/vm.args"

docker exec "couchdb${masternode}" bash -c "echo \"-name couchdb@${masternode}\" >> /opt/couchdb/etc/vm.args"

# Start the containers (and wait a bit while they boot):

docker start "couchdb${masternode}"



# Set up the CouchDB cluster:

for node in ${othernodes} 
do
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup" \
      --header "Content-Type: application/json"\
      --data "{\"action\": \"enable_cluster\", \"bind_address\":\"0.0.0.0\",\
             \"username\": \"${user}\", \"password\":\"${pass}\", \"port\": \"5984\",\
             \"remote_node\": \"${node}\", \"node_count\": \"$(echo ${nodes[@]} | wc -w)\",\
             \"remote_current_user\":\"${user}\", \"remote_current_password\":\"${pass}\"}"
done

for node in ${othernodes}
do
    curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup"\
      --header "Content-Type: application/json"\
      --data "{\"action\": \"add_node\", \"host\":\"${node}\",\
             \"port\": \"5984\", \"username\": \"${user}\", \"password\":\"${pass}\"}"
done

curl -XPOST "http://${user}:${pass}@${masternode}:5984/_cluster_setup"\
    --header "Content-Type: application/json" --data "{\"action\": \"finish_cluster\"}"


# Check wether the cluster configuration is correct:

for node in "${nodes[@]}"; do  curl -X GET "http://${user}:${pass}@${node}:5984/_membership"; done


# Adding a database to one node of the cluster makes it to be created on all other nodes as well:

curl -XPUT "http://${user}:${pass}@${masternode}:5984/twitter"
for node in "${nodes[@]}"; do  curl -X GET "http://${user}:${pass}@${node}:5984/_all_dbs"; done