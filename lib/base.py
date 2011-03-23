import memcache
import cherrypy
from helpers import *


# the data client is going to be our api
# for getting / setting keys. for now
# we are just strait up using the memcache
# client, later this will probably become more
# versitale (as well as not just init itself on import)

# TODO read the address' from config
data_client = memcache.Client(['127.0.0.1:11211'])



