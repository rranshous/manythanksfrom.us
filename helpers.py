import time
from templates import render
from cherrypy import HTTPRedirect, HTTPError
import cherrypy
from lib.data_client import KawaiiDataClient as DataClient

try:
    import json
except ImportError:
    import simplejson as json

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

# TODO: make generic version

def iter_events_from_user(user_hash):
    user_data = get_user_data(user_hash)
    if users_data:
        for event_hash in user_data.get('_event_hashes',[]):
            yield get_event_data(event_hash)

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



def get_active_user_data():
    if not cherrypy.session.get('user_hash'):
        return False

    return get_user_data(cherrypy.session.get('user_hash'))


def set_active_user(_hash):
    cherrypy.session['user_hash'] = _hash
    return True

## Utils
def create_hash():
    """
    returns a new unique hash
    """
    # could do better ..
    return hash(time.time())

