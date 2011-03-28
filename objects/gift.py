from base import *

class GiftObject(BaseObject):

    # data storage
    name = String()
    blurb = String()

    # relatives
    events = Relative()
    users = Relative()
