import cherrypy
from lib.base import *
from base import BaseController

from admin import AdminController

class RootController(BaseController):
    
    # admin section of the site
    admin = AdminController()

    @cherrypy.expose
    def index(self):
        # render back the home page of the site
        return render('/home.html')

    @cherrypy.expose
    def default(self,event_hash,description,
                     gift_hash=None,gift_name=None):
        # we are going to assume that a default
        # is an attemp to view a page / list

        # the args should be:
        #  <event hash> <description> <gift hash> <gift name>

        # if we have a page than lets see if it exists
        if gift_hash:
            gift_data = get_gift_data(gift_hash)
            
            # if we found it return the page
            # if not we'll let it fall through to event
            if gift_data:
                event_data = get_event_data(gift_data.get('_event_hash'))

                return render('/gift/basic.html',gift_data=gift_data,
                                                 event_data=event_data)

        # find the event
        event_data = get_event_data(event_hash)

        # bad event =/
        if not event_data:
            raise error('404')

        # the event may not use a home page
        if not event_data.get('public'):
            raise error('404')

        # if they want the home page, we'll give it up
        r = render('/event/basic.html',event_data=event_data)
        return r

