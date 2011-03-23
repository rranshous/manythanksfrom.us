from helpers import get_event_data, get_gift_data

class EventController:
    """
    provides interface for managing events
    """
    
    @cherrypy.expose
    def index(self):
        """
        returns the home event page, lists events
        buttons to add events, delete events etc
        """
        return render('/admin/event/home.html')

    @cherrypy.expose
    def add(self,**kwargs):
        # if we don't get any args it's a request for the page
        if not kwargs:
            return render('/admin/event/add.html')

        # if we got kwargs than lets create a new event
        event_data = get_event_data()

        # update our data w/ the passed values
        event_data.update(**kwargs)

        # push it to the server
        _hash = set_event_data(data=event_data)

        # and kick them to the edit page
        return redirect('admin/event/update/%s' % _hash)

    @cherrypy.expose
    def update(self,_hash=None,**kwargs):
        # find our event
        event_data = get_event_data(_hash)

        # if they didn't pass an event ..
        if not event_data:
            return error('404')

        # if they only passed in the hash is a request for the page
        if _hash and not kwargs:
            return render('/admin/event/update',

        # update the data
        #  right now we are taking the args at face value,
        #  later something will be smarter
        event_data.update(**kwargs)

        # push it back
        set_event_data(data=event_data)

        # kick them to back to the update page
        return redirect('/admin/event/update/%s' % _hash)

class AdminController:
    """
    provides interfaces for managing account
    everything in this method requires you
    be logged in
    """

    event = EventController()
