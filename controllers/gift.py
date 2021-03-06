from lib.base import *
from base import BaseController
import objects as o
import mimetypes

class GiftController(BaseController):
    """
    provides interface for managing gifts
    """

    @cherrypy.expose
    def add(self,_event_hash=None,**kwargs):
        """
        no kwargs = get page
        kwargs = add gift
        """

        # get our event
        event_data = o.Event.get_data(_event_hash)

        # if we didn't get back our data ..
        if not event_data:
            # it was not found
            raise error(404)

        # push them to the page if they didn't give args
        if not kwargs:
            cherrypy.log('debug','returning add page')
            return render('/admin/gift/add.html',event_data=event_data)

        # if we got args than we want to add a new gift
        gift_data = o.Gift.get_data()

        # update the gift's event
        o.Event.set_relative(event_data,gift_data)

        # update it's data
        gift_data = o.Gift.update_and_validate(gift_data,kwargs)

        # push it back
        _hash = o.Gift.set_data(gift_data)

        # if we got an image set it
        if 'image' in kwargs:
            rel_path = save_object_image(o.Gift,gift_data,
                                         kwargs.get('image'))
            gift_data['rel_image_path'] = rel_path

        # TODO: not resend data (aka settup "commit" for data client)
        o.Gift.set_data(gift_data)

        # kick them to the edit page
        redirect('/admin/gift/update/%s' % _hash)

    @cherrypy.expose
    def update(self,_hash=None,**kwargs):
        # get the gifts data
        gift_data = o.Gift.get_data(_hash)

        # and the data for it's event
        event_data = o.Event.get_relatives_data(gift_data,single=True)

        # no data's ?
        if not gift_data or not event_data:
            raise error(404)

        # if we didn't get any args, they want the page
        if not kwargs:
            return render('/admin/gift/update.html',
                          event_data=event_data,gift_data=gift_data)

        # guess they want to update
        gift_data = o.Gift.update_and_validate(gift_data,kwargs)

        # if we got an image set it
        if 'image' in kwargs:
            rel_path = save_object_image(o.Gift,gift_data,
                                         kwargs.get('image'))
            gift_data['rel_image_path'] = rel_path

        # push our data back out
        _hash = o.Gift.set_data(gift_data)

        # redirect them to the update page
        redirect('/admin/gift/update/%s' % _hash)

    @cherrypy.expose
    def delete(self,_hash=None):
        # make sure we have our hash
        if not _hash:
            raise error(404)

        # delete that mother
        o.Gift.delete_data(_hash)

        # push them to admin page
        redirect('/admin/')

