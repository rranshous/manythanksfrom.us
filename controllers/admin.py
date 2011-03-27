import cherrypy

from helpers import get_event_data, get_gift_data

from event import EventController
from gift import GiftController
from base import BaseController

class AdminController(BaseController):
    """
    provides interfaces for managing account
    everything in this method requires you
    be logged in
    """

    event = EventController()
    gift = GiftController()

    @cherrypy.expose
    def index(self):
        # return back the admin home page
        return render('/admin/home.html')

