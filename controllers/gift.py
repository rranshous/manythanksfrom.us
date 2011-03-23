from helpers import get_gift_data, get_event_data
from lib.base import *

class GiftController:
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
        event_data = get_event_data(_event_hash)

        # if we didn't get back our data ..
        if not event_data:
            # it was not found
            raise error(404)

        # push them to the page if they didn't give args
        if not kwargs:
            return render('/admin/gift/add.html',event_data=event_data)

        # if we got args than we want to add a new gift
        gift_data = get_gift_data()

        # update the gift's event
        gift_data.set('_event_hash',event_data.get('_hash'))

        # update it's data
        gift_data.update(kwargs)

        # push it back
        _hash = set_gift_data(data=gift_data)

        # kick them to the edit page
        event_hash = event_data.get('_hash')
        return redirect('/admin/gift/update/%s' % _hash)

    @cherrypy.expose
    def update(self,_hash=None,**kwargs):
        # get the event and gift data
        gift_data = get_gift_data(_hash)
        event_data = get_event_data(gift_data.get('_event_hash'))

        # no data's ?
        if not gift_data:
            raise error(404)

        # if we didn't get any args, they want the page
        if not kwargs:
            return render('/admin/gift/update.html',
                          event_data=event_data,gift_data=gift_data)

        # guess they want to update
        gift_data.update(**kwargs)

        # push our data back out
        _hash = set_gift_data(_hash,gift_data)

        # redirect them to the update page
        return redirect('/admin/gift/update/%s' % _hash)


