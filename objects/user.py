from base import *

class UserObject(BaseObject):
    
    # storage
    name = String()

    # relations
    gifts = Relative()
    events = Relative()
