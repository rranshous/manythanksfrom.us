#!/usr/bin/python

import cherrypy
from controllers import RootController
from lib.base import *
from lib.data_client import KawaiiDataClient as DataClient

if __name__ == '__main__':
    # setup config
    cherrypy.config.update('./cherryconfig.ini')

    # instantiate our data client
    DataClient(cherrypy.config.get('storage_address'))

    # setup our app
    app = cherrypy.Application(RootController(),
                               config='./cherryconfig.ini')
    cherrypy.quickstart(app)
