import memcache
import cherrypy
import logging

# the data client is going to be our api
# for getting / setting keys.

# the currently being used DataClient instance
active_instance = None

class DataClient(object):

    def __init__(self):
        # tracking the open instance using
        # the class attribute
        cherrypy.log('debug','setting active: %s' % self)
        global active_instance
        active_instance = self

    @classmethod
    def instance(cls):
        global active_instance
        return active_instance

class KawaiiDataClient(DataClient):
    # TODO: reattack this client
    #       w/ a custom version of the memcache
    #       client that doesn't expect to fail some times
    def __init__(self,memcached_address='127.0.0.1:11211'):
        super(KawaiiDataClient,self).__init__()

        # we use the memcache client
        self.memcache_client = None
        
        # the address of our server
        self.memcached_address = memcached_address

        # if we already know the address than
        # setup the connection
        if self.memcached_address:
            self._reset_connection()


    def _connected(self):
        # TODO: return true if memcache is connected
        # right now, we'll just always reset
        return False

    def _reset_connection(self):
        # TODO: reset memcached connection
        if self.memcache_client:
            self.memcache_client.forget_dead_hosts()
        else:
            c = memcache.Client([self.memcached_address])
            self.memcache_client = c
        return self.memcache_client

    @classmethod
    def instance(cls):
        # we want to make sure we are connected
        global active_instance
        self = active_instance
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

    def delete(self,*args):
        return self.memcache_client.delete(*args)
