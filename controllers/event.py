from lib.base import *
from base import BaseController
import objects as o

class EventController(BaseController):
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
        """
        if no kwargs are passed returns the add page.
        if kwargs are passed than assumes ur posting data
        and creates a new event
        """
        # if we don't get any args it's a request for the page
        if not kwargs:
            return render('/admin/event/add.html')

        # if we got kwargs than lets create a new event
        event_data = o.Event.get_data()

        # associate to us
        o.User.set_relative(get_active_user_data(),event_data)

        # update our data w/ the passed values
        event_data = o.Event.update_and_validate(event_data,kwargs)

        # push it to the server
        _hash = o.Event.set_data(event_data)

        # if they passed in any images, save them
        if 'image' in kwargs:
            rel_path = save_object_image(o.Event,kwargs.get('image'))
            event_data['rel_image_path'] = rel_path

        # and kick them to the edit page
        redirect('/admin/event/update/%s' % _hash)

    @cherrypy.expose
    def update(self,_hash=None,**kwargs):
        # find our event
        event_data = o.Event.get_data(_hash)

        # if they didn't pass an event ..
        if not event_data:
            raise error(404)

        # if they only passed in the hash is a request for the page
        if _hash and not kwargs:
            return render('/admin/event/update.html',
                          event_data=event_data)

        # update the data
        #  right now we are taking the args at face value,
        #  later something will be smarter
        event_data = o.Event.update_and_validate(event_data,kwargs)

        # push it back
        o.Event.set_data(event_data)

        # if they gave us a new image save it
        if 'image' in kwargs:
            rel_path = save_object_image(o.Event,kwargs.get('image'))
            event_data['rel_image_path'] = rel_path

        # kick them to back to the update page
        redirect('/admin/event/update/%s' % _hash)

    @cherrypy.expose
    def delete(self,_hash=None):
        # make sure we have our hash
        if not _hash:
            raise error(404)

        # delete that mother
        o.Event.delete_data(_hash)

        # push them to admin page
        redirect('/admin/')
