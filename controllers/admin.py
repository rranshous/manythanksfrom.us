import cherrypy
from helpers import get_active_user_data, set_active_user
from lib.base import *
import logging
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

        # for now set the user to me
        set_active_user('237823077639407214003259210226144395600')

        # get our user's data
        user_data = get_active_user_data()

        cherrypy.log('active_user: %s %s' % 
                     (cherrypy.session.get('user_hash'),user_data))

        # we need to get the user's events
        event_datas = o.Event.get_relatives_data(user_data)
        return render('/admin/home.html',
                      event_datas=event_datas)

