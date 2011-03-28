from base import *

class EventObject(BaseObject):

    # data storage attributes
    name = String()
    blurb = String()
    public = Boolean()
    
    # relational accessors
    gifts = Relative()
    users = Relative()

