from base import *

class EventObject(BaseObject):

    # data storage attributes
    name = String()
    blurb = String()
    public = Bool()
    
    # relational accessors
    gifts = Relative()
    users = Relative()

