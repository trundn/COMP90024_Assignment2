from couchdb import Server

server_url = 'http://admin:gcsvn123@localhost:5984'
database_name = 'tweets'

couch = Server(server_url)
database = couch[database_name]
response = database.list('_design/tweets-per-hour', '_view/tweets-per-hour', **{'reduce': True, 'group': True})

print(response[1])
