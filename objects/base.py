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
    def serialize_data(cls,data):
        return json.dumps(data)

    @classmethod
    def deserialize_data(cls,data):
        return json.loads(data)

    @classmethod
    def _create_hash(cls):
        """
        returns a new hash for an obj
        """
        # for now doing this sloppy / easy
        md5 = hashlib.md5()
        md5.update(time.time())
        i = int(md5.hexdigest(),16)
        return i

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


    @classmethod
    def get_data(cls,_hash=None):
        """
        returns a skeleton of the obj data if no hash is passed,
        else returns the data for the obj
        """
        
        # first, if no hash was sent, return skeleton
        if not _hash:
            return cls.get_skeleton()

        # if they did pass a hash, get the obj's data
        key = cls.storage_key(_hash)

        # deserialize the data off the wire
        data = cls.deserialize_data(data_client.get(key))

        return data

    @classmethod
    def set_data(cls,data=None):
        """
        set's an objects data. if there is no hash in the data
        one will be added. the data's hash is returned
        """
        
        # if the data doesn't have a hash, give it one
        if not data.get('_hash'):
            data['_hash'] = cls.create_hash()

        # push the data to storage
        key = cls.storage_key(data.get('_hash'))

        # serialize the data as it goes out the door
        data_client.set(key,cls.serialize_data(data))

        return data.get('_hash')



