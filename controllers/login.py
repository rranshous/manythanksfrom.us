from helpers import get_active_user_data, set_active_user
from lib.base import *
import objects as o
from base import BaseController

class LoginController(BaseController):
    """
    logs the user in if they are not yet logged in, else
    populates the active user
    """

    @cherrypy.expose
    def index(self):
        """
        if they are already logged in passes
        them through. else, gives them the login form
        """

        # try and pull the user's data
        user = get_active_user_data()

        if not user:
            # they are not logged in give them the login form
            return render('/login_form.html')

        # they are logged in, pass them to the home page
        redirect('/')

    @cherrypy.expose
    def set(self, username, password):
        """
        accepts form vars for username and password
        if all is well sets session info for ur login
        """

        # if there are no args, give them the form
        if not username and not password:
            return render('/login_form.html')

        # get the user by the username
        user_data = o.User.get_data(key=username)

        # no user data?
        if not user_data:
            add_flash('error','User not found')
            return render('/login_form.html')

        # check their password
        if not o.User.check_password(user_data,password):
            add_flash('error','Incorrect password')
            return render('/login_form.html')

        # set them as active user
        set_active_user(user_data.get('_hash'))


    @cherrypy.expose
    def create(self, username=None, password=None):
        """
        creates a new login, usernames must be unique
        """

        # if there are no args, return the form
        if not username and not password:
            return render('/login_form.html')

        # check and make sure they provided a username
        if not username:
            add_flash('error','Must provide username')
            return render('/create_login_form.html')

        # check the password
        if not password:
            add_flash('error','Must provide password')
            return render('/create_login_form.html')

        # figure out what the hash would be for the usernaem
        _hash = o.User._get_hash({'username':username})

        # see if there is already a user w/ the username
        user_data = o.User.get_data(_hash)

        # wwops, already exists
        if user_data:
            add_flash('error','User already exists')
            return render('/create_login_form.html')

        # now that we know it's unique, create the user
        user_data = o.User.get_data()

        # set the username and password
        user_data['username'] = username
        user_data['password'] = password

        # push our data out
        o.User.set_data(user_data)

        # set the new user as the active user
        set_active_user(user_data.get('_hash'))

        # now return them to their admin page
        redirect('/admin')
