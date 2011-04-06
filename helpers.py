import time
from templates import render
from cherrypy import HTTPRedirect, HTTPError
import cherrypy
from lib.data_client import KawaiiDataClient as DataClient
import objects as o

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



## Image functions

def save_image_data(rel_path,data):
    """
    given relative path and image data
    saves the image to the correct place
    """
    base_path = cherrypy.config.get('save_root')
    path = os.path.join(base_path,_type,_hash)
    with file(path,'wb') as fh:
        fh.write(data)
    return path

def get_active_user_data():
    if not cherrypy.session.get('user_hash'):
        return False

    return o.User.get_data(cherrypy.session.get('user_hash'))

def set_active_user(_hash):
    cherrypy.session['user_hash'] = _hash
    return True
