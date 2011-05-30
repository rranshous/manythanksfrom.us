from base import *

class UserObject(BaseObject):
    SALT = 'fa0-sdfj'

    # storage
    username = String()

    # store the password as the digest
    # of a random string and their password
    _password = String()
    password = property(lambda s: self._password,
                        set_password)

    name = String()
    rel_image_path = String()

    # relations
    gifts = Relative()
    events = Relative()

    # we want the username's to be unique,
    # so we will hash by them
    hash_key = 'username'

    def set_password(self, password):
        # set our password hash
        self._password = self.create_password(password)

    def check_password(self, password):
        
        # we should be able to combine the given
        # password with our salt and come
        # up with the saved password

        if self._password != self.create_password(password):
            return False

        return True

    @classmethod
    def create_password(cls, password):
        md5 = hashlib.md5()
        md5.update(self.SALT)
        md5.update(_password)
        return md5.hexdigest()

