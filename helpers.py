import time
from templates import render
from cherrypy import HTTPRedirect, HTTPError
import cherrypy
from lib.data_client import KawaiiDataClient as DataClient
import objects as o
import os.path, os
import mimetypes

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
def get_extension_from_upload(upload):
    # guess the extension from the mimetype
    extension = mimetypes.guess_extension(str(upload.content_type))

    # wtf mate
    if not extension:
        extension = '.jpg' # what the hell

    return extension

def save_object_image(obj,obj_data,upload):
    # where we savin' it ?
    path = obj.get_image_path(obj_data)

    # get the uploads extension
    extension = get_extension_from_upload(upload)

    # concat that bitch to the path
    path += extension or ''

    # grab our data
    data = upload.file.read()
    if data:
        cherrypy.log('saving image: %s %s' % (len(data),path))
        path = save_image_data(path,data)
    else:
        cherrypy.log('no data')

    return path



def save_image_data(rel_path,data):
    """
    given relative path and image data
    saves the image to the correct place
    """


    base_path = cherrypy.config.get('save_root')
    path = os.path.join(base_path,rel_path)

    # we don't need ./
    if path.startswith('./'):
        path = path[2:]

    # make sure it exists
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        # create that motha
        os.makedirs(dir_path)

    # and out we go
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
