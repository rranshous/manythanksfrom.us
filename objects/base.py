from formencode import validators

# objects are kind of like models they describe
# the attributes an object can have as well as
# include helper / access methods

# class stands for a related data type
class Relative(object):
    pass

# attributes define the data that can be
# stored on an object
class Attribute(object):
    @classmethod
    def validate(cls,v):
        # we are going to map the name
        # of the Attribute child to formencode
        # validators
        name = cls.__name__
        validator = getattr(validators,name)
        if not validator:
            raise formencode.invalid('bad attribute type')
        return validator.to_python(v)

class String(Attribute):
    pass

class Boolean(Attribute):
    pass

# right now just a string, later might
# want custom stuff in there
Hash = String


# objects define what data can be stored
# what type and provides helpers
class BaseObject(object):
    
    # data storage
    _hash = Hash()

    @classmethod
    def _get_NS(cls):
        # if there isn't one defined
        if not getattr(cls,'NS'):
            # it's our name lowercase
            return cls.__name__.lower()[:-5] # cut Object

        # if it is defined return it
        return self.NS

    @classmethod
    def storage_key(cls,_hash):
        """ returns the key for storage of obj """
        return '/%s/%s' % (self.get_NS(),_hash)

    @classmethod
    def get_skeleton(cls):
        """
        returns back a dictionary with
        a key entry for each attribute
        """
        skel = {}
        for k in dirs(cls):
            attr = getattr(cls,k,None)
            if isinstance(attr,Attribute):
                skel[attr] = None

        return skel

    @classmethod
    def validate(cls,data):
        """
        removes extra keys, updates values
        to match type
        """

        to_remove = []

        # go through all k/v pairs
        for k,v in data.iteritems():

            # the key needs to be an attribute
            attr = getattr(cls,k,None)
            if isinstance(attr,Attribute):
                # now validate the attr type
                data[k] = attr.validate(v)
            else:
                to_remove.append(k)

        # remove keys that shouldn't be there
        for k in to_remove:
            del data[k]

        return data

    @classmethod
    def update_and_validate(cls,event_data,update_dict):
        # we are going to validate the the new data
        valid_data = cls.validate(update_dict)

        # now uddate the data we were passed
        event_data.update(valid_data)

        # return it for good measure
        return event_data
