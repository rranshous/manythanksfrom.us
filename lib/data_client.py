import memcache
import cherrypy

# the data client is going to be our api
# for getting / setting keys. for now
# we are just strait up using the memcache
# client, later this will probably become more
# versitale (as well as not just init itself on import)

address = '127.0.0.1:11211'
data_client = memcache.Client([address])


# TODO: start using the DataClient obj

class DataClient:
    active_instance = None

    def __init__(self):
        # tracking the open instance using
        # the class attribute
        self.active_instance = self

    @classmethod
    def instance(cls):
        return self.active_instance

class KawaiiDataClient:
    def __init__(self):
        # we use the memcache client
        self.memcache_client = None
        
        # the address of our server
        self.memcached_address = None

    def _connected(self):
        # TODO: return true if memcache is connected
        # right now, we'll just always reset
        return False

    def _reset_connection(self):
        # TODO: reset memcached connection
        c = memcache.Client([self.memcached_address])
        self.memcache_client = c
        return self.memcache_client

    @classmethod
    def instance(cls):
        # we want to make sure we are connected
        self = cls.active_instance
        if not self._connected():
            self._reset_connection()
        return self

    def set_address(self,address):
        # set our clients address, reset the client
        self.memcached_address = address
        self._reset_connection()
        return address

    def set(self,*args):
        # just map to memcache
        return self.memcache_client.set(*args)

    def get(self,*args):
        # mapped to memcache
        return self.memcache_client.get(*args)

