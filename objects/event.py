from base import *

class EventObject(BaseObject):

    # data storage attributes
    name = String()
    blurb = String()
    public = Bool()
    rel_image_path = String()
    
    # relational accessors
    gifts = Relative()
    users = Relative()

