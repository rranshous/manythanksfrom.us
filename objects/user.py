from base import *

class UserObject(BaseObject):
    
    # storage
    name = String()
    rel_image_path = String()

    # relations
    gifts = Relative()
    events = Relative()
