from formencode import validators
from lib.data_client import KawaiiDataClient as DataClient
import cherrypy
import hashlib
import time
import os

try:
    import json
except ImportError:
    import jsonify as json

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

class Bool(Attribute):
    pass

# right now just a string, later might
# want custom stuff in there
Hash = String



# objects define what data can be stored
# what type and provides helpers
class BaseObject(object):

    @classmethod
    def serialize_data(cls,data):
        # we need to clean the data before it goes in
        return json.dumps(data)

    @classmethod
    def deserialize_data(cls,data):
        return json.loads(data)


    @classmethod
    def _create_hash(cls,data):
        """
        returns the hash for the obj, can be based
        off some data in the obj. if the class specifies
        a key to hash from and it does not exist,
        an exception is raised
        """

        # pull our hash value from the data if we can
        if cls.hash_key and cls.hash_key in data:
            _key = data.get(cls.hash_key)

        # if we can't find the key exception time
        elif cls.hash_key:
            raise Exception('hash key not found: %s' % (cls.hash_key))

        # if there was no key specified just use the time
        else:
            _key = str(time.time())

        return cls._hash(_key)

    @classmethod
    def _hash(cls,_key):

        # create our hash from the key
        md5 = hashlib.md5()
        md5.update(_key)
        return str(int(md5.hexdigest(),16))

    @classmethod
    def _get_NS(cls):
        # if there isn't one defined
        if not getattr(cls,'NS',None):
            # it's our name lowercase
            return cls.__name__.lower()[:-6] # cut Object

        # if it is defined return it
        return self.NS

    @classmethod
    def storage_key(cls,_hash):
        """ returns the key for storage of obj """
        return (u'/%s/%s' % (cls._get_NS(),_hash)).encode('UTF-8')

    @classmethod
    def get_skeleton(cls):
        """
        returns back a dictionary with
        a key entry for each attribute
        """
        skel = {}
        for k in dir(cls):
            attr = getattr(cls,k,None)
            if isinstance(attr,Attribute):
                skel[k] = None

        return skel

    @classmethod
    def validate(cls,data):
        """
        removes extra keys, updates values
        to match type
        """

        to_remove = []
        valid = {}

        # go through all k/v pairs
        for k,v in data.iteritems():

            # the key needs to be an attribute
            attr = getattr(cls,k,None)
            if isinstance(attr,Attribute):
                # now validate the attr type
                valid[k] = attr.validate(v)

        return valid

    @classmethod
    def update_and_validate(cls,obj_data,update_dict):
        # we are going to validate the the new data
        valid_data = cls.validate(update_dict)

        # now uddate the data we were passed
        obj_data.update(valid_data)

        # return it for good measure
        return obj_data

    @classmethod
    def delete_data(cls,_hash):
        """
        delete's the objs data
        """

        # get our obj's key
        key = cls.storage_key(_hash)

        # delete that mother
        data_client = DataClient.instance()
        return data_client.delete(key)

    @classmethod
    def get_data(cls,_hash=None,key=None):
        """
        returns a skeleton of the obj data if no hash is passed,
        else returns the data for the obj
        """

        # get our data client
        data_client = DataClient.instance()

        # see if they gave us a key to hash
        if key:
            _hash = cls._hash(key)
        
        # first, if no hash was sent, return skeleton
        if not _hash:
            return cls.get_skeleton()

        # if they did pass a hash, get the obj's data
        key = cls.storage_key(_hash)

        # grab the data
        data = data_client.get(key)

        cherrypy.log('got data: %s %s' % (key,data))

        # if we didn't get anything return None
        if not data:
            return None

        # deserialize the data off the wire
        data = cls.deserialize_data(data)

        return data

    @classmethod
    def set_data(cls,data=None):
        """
        set's an objects data. if there is no hash in the data
        one will be added. the data's hash is returned
        """

        # get our data client
        data_client = DataClient.instance()
        
        # if the data doesn't have a hash, give it one
        if not data.get('_hash'):
            data['_hash'] = cls._create_hash(data)

        # push the data to storage
        key = cls.storage_key(data.get('_hash'))

        # serialize the data as it goes out the door
        s_data = cls.serialize_data(data)
        
        cherrypy.log('setting data: %s' % s_data)

        # and set it
        data_client.set(key,s_data)

        return data.get('_hash')

    @classmethod
    def iter_relatives_data(cls,obj_data):
        """
        see get_relatives_data + iter magic
        """

        cherrypy.log('iter obj data: %s' % obj_data)

        # check and see if there is a list of
        # FK hashes of our type on the object
        key = '_%s_hashes' % cls._get_NS()
        for _hash in obj_data.get(key) or []:
            yield cls.get_data(_hash)

        # also check the single side
        key = '_%s_hash' % cls._get_NS()
        _hash = obj_data.get(key)
        if _hash:
            yield cls.get_data(_hash)

    @classmethod
    def get_relatives_data(cls,obj_data,single=False):
        """
        pass it another obj type's data. we will return
        back a list (or single item if single=True) of
        the data for the obj's of this type who relate
        to the data passed.
        """
        
        to_return = []
        for data in cls.iter_relatives_data(obj_data):
            # if they only want a single value, give them the first
            if single:
                return data

            # if you want the whole list collect'm up
            to_return.append(data)

        # what if we didn't get anything ?
        if not to_return and single:
            return None

        return to_return

    @classmethod
    def set_relative(cls,obj_data,other_obj_data):
        """
        associates the obj with the other obj
        """

        # we are going to add a reference to the other obj
        ns = cls._get_NS()
        other_obj_data['_%s_hash' % ns] = obj_data.get('_hash')
        return other_obj_data

    @classmethod
    def get_image_path(cls,obj_data):
        """
        returns the relative image path for the obj
        """
        
        # the image path is going to be /type/hash
        return '%s%s%s' % (cls._get_NS(),os.sep,obj_data.get('_hash'))

