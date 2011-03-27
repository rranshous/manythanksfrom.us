import cherrypy

class BaseController(object):
    def strip_action(self,d):
        del d['action']
