from base import *

class GiftObject(BaseObject):

    # data storage
    name = String()
    blurb = String()
    email_address = String()
    postal_address = String()
    thank_you_sent = Bool()
    public = Bool()

    # relatives
    events = Relative()
    users = Relative()


