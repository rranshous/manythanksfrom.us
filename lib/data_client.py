import memcache
import cherrypy

# the data client is going to be our api
# for getting / setting keys. for now
# we are just strait up using the memcache
# client, later this will probably become more
# versitale (as well as not just init itself on import)

# TODO read the address' from config
address = cherrypy.config.get('storage_address')
data_client = memcache.Client([address])



