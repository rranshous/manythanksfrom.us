from helpers import get_event_data, get_gift_data

from event import EventController

class AdminController:
    """
    provides interfaces for managing account
    everything in this method requires you
    be logged in
    """

    event = EventController()
