
from controllers import AuthController, AdminController
from helpers import get_gift, get_event


class Root:
    
    login = AuthController()

    admin = AdminController()

    @cherrypy.expose
    def default(self,event_hash,description,page=None)
        # we are going to assume that a default
        # is an attemp to view a page / list

        # the args should be:
        #  <event hash> <description> <page hash/name>

        # if we have a page than lets see if it exists
        if page:
            gift_data = get_gift_data(event_hash=event_hash,
                                      gift_info=page)
            
            # if we found it return the page
            # if not we'll let it fall through to event
            if gift_data:
                return render('/gift/basic.html',gift_data=gift_data)

        # find the event
        event_data = get_event_data(event_hash)

        # bad event =/
        if not event_data:
            return error('404')

        # the event may not use a home page
        if not event_data.get('home_page'):
            return error('404')

        # if they want the home page, we'll give it up
        return render('/event/basic.html',event_data=event_data)

