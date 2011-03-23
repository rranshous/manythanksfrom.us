import time

def get_event_data(_hash=None):
    """
    if passed a string will try and return
    an existing events data. if it can't find
    that data or it is not passed anything
    it will return a blank dict
    """

    # no identifier = new event
    if not _hash:
        return {}

    # try and pull the event data based on hash
    data = data_client.get('/event/%s' % _hash)

    # oh well, couldn't find it
    if not data:
        return {}

    # woot, return the goodies
    return data

def set_event_data(_hash=None,data=None):
    """
    sets an events data using the provided hash
    if no hash is provided a new one is created
    in either case the hash is returned.
    """

    if not _hash:
        _hash = create_event_hash()



def get_gift_data

def set_gift_data

def create_event_hash():
    """
    returns a new unique event hash
    """
    return hash(time.time())
