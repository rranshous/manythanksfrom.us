import time
from templates import render
from cherrypy import HTTPRedirect, HTTPError
import cherrypy

try:
    import json
except ImportError:
    import simplejson as json

from lib.data_client import data_client

def add_flash(msg_type,msg=None):
    if not msg:
        msg = msg_type
        msg_type = 'info'

    cherrypy.session.setdefault(msg_type,[]).append(msg)

def redirect(*args):
    url = '/'.join((str(x) for x in args))
    raise HTTPRedirect(url)

def error(*args):
    return HTTPError(*args)


## FK functions
def iter_gifts_from_event(event_hash):
    # we are going to yield up the data
    # for each of the gifts associated w/ the event
    event_data = get_event_data(event_hash)
    if event_data:
        for gift_hash in event_data.get('_gift_hashes',[]):
            yield get_gift_data(gift_hash)


## Image functions
def _set_image(_type,_hash,data):
    """
    save the obj's image to the drive using
    the type as the namespace
    """
    # right now the way we are saving limits each
    # type to a single image
    base_path = cherrypy.config.get('save_root')
    path = os.path.join(base_path,_type,_hash)
    with file(path,'wb') as fh:
        fh.write(data)
    return True

def _get_image(_type,_hash):
    base_path = cherrypy.config.get('save_root')
    path = os.path.join(base_path,_type,_hash)
    with file(path,'rb') as fh:
        return fh.read()

def set_event_image(_hash,data):
    _set_image('event',_hash,data)

def get_event_image(_hash):
    _get_image('event',_hash)


## Obj functions
def _get_data(obj_type,_hash=None):
    """
    if passed a string will try and return
    an existing obj data. if it can't find
    that data or it is not passed anything
    it will return a blank dict
    """

    # no identifier = new obj
    if not _hash:
        return {}

    # hash must be a string
    _hash = str(_hash)

    # try and pull the event data based on hash
    key = '/%s/%s' % (obj_type,_hash)
    json_data = data_client.get(key)

    cherrypy.log('debug','%s got data: %s' % (key,json_data))

    if not json_data:
        return None

    # get the obj from the json
    data = json.loads(json_data)

    # oh well, couldn't find it
    if not data:
        return {'_hash':_hash}

    # woot, return the goodies
    return data

def _set_data(obj_type,_hash=None,data={}):
    """
    sets an obj data using the provided hash
    if no hash is provided a new one is created
    in either case the hash is returned.
    """

    # generate a hash if they didn't pass one
    if not _hash:
        _hash = create_hash()

    # hash must be a string
    _hash = str(_hash)

    # set the hash in the data
    data['_hash'] = _hash

    # turn our data into JSON
    json_data = json.dumps(data)

    cherrypy.log('debug','setting data: %s' % json_data)

    # set our data
    data_client.set('/%s/%s' % (obj_type,_hash), json_data)

    # give them back the hash
    return _hash


def get_event_data(_hash=None):
    """
    if passed a string will try and return
    an existing events data. if it can't find
    that data or it is not passed anything
    it will return a blank dict
    """
    return _get_data('event',_hash)

def set_event_data(_hash=None,data={}):
    """
    sets an events data using the provided hash
    if no hash is provided a new one is created
    in either case the hash is returned.
    """
    return _set_data('event',_hash,data)

def get_gift_data(_hash=None):
    """
    if passed a string will try and return
    an existing gift data. if it can't find
    that data or it is not passed anything
    it will return a blank dict
    """
    return _get_data('gift',_hash)

def set_gift_data(_hash=None,data={}):
    """
    sets an gift data using the provided hash
    if no hash is provided a new one is created
    in either case the hash is returned.
    """
    return _set_data('gift',_hash,data)

def create_hash():
    """
    returns a new unique hash
    """
    # could do better ..
    return hash(time.time())

