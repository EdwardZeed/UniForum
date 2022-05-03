'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''
# from Crypto.Hash import MD5
from bottle import route, get, post, error, request, static_file

import model
import view
import rsa

from sql import SQLDatabase


# Initialise our views, all arguments are defaults for the template
page_view = view.View()
db = SQLDatabase(database_arg="identifier.sqlite")
db.database_setup()

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

# diplay regiter page
#-----------------------------------------------------------------------------
@get('/register')
def get_register_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.register_form()

# check register
#-----------------------------------------------------------------------------
@post('/register')
def post_register():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    public_key = request.forms.get('pubKey')
    print(username)
    print(password)
    print(public_key)

    # hash = MD5.new()
    # hash.update(password.encode())
    # password = hash.hexdigest()



    # Call the appropriate method
    return model.register_check(username, password, public_key)

#-----------------------------------------------------------------------------
# Send_message
#-----------------------------------------------------------------------------
@get('/send')
def get_send_controller():
    '''
        get_login

        Serves the login page
    '''
    return model.send_message_form();

@post('/send')
def send_message():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing

    sender = request.forms.get('sender')
    message = request.forms.get('message')
    receiver = request.forms.get('receiver')
    digital_signature = request.forms.get('digital_signature')

    print("ds:"+digital_signature)
    print(receiver)
    print(message)

    # print("This is sender: ",sender)
    # print("This is message",message)



    # pass the receiver and message to the model
    return model.send_success(sender,receiver, message, digital_signature)

#-----------------------------------------------------------------------------
# share_knowledge
#-----------------------------------------------------------------------------
@post('/share_knowledge')
def share_knowledge():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing

    # Call the appropriate method
    knowledge = request.forms.get('Knowledge')
    username = request.forms.get('username')

    return model.share_knowledge(username, knowledge)

@get('/get_message')
def get_message_controller():
    return model.get_message_form()

#-----------------------------------------------------------------------------
# Send_message
#-----------------------------------------------------------------------------
@post('/get_message')
def get_message():
    '''
        post_login

        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing

    # Call the appropriate method
    return model.get_message()


#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    public_key = request.forms.get('pk')

    # hash = MD5.new()
    # hash.update(password.encode())
    # password = hash.hexdigest()
    print(password)
    # Call the appropriate method
    return model.login_check(username, password)



#-----------------------------------------------------------------------------
#Admin_delete_user
#-----------------------------------------------------------------------------
@post('/admin_delete')
def admin_delete_user():
    '''

    '''

    # Handle the form processing
    username = request.forms.get('delete')

    # Call the appropriate method
    return model.admin_delete_user(username)

@post('/admin_mute')
def admin_delete_user():
    '''

    '''

    # Handle the form processing
    username = request.forms.get('mute')

    # Call the appropriate method
    return model.admin_mute_user(username)



@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()
#-----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)
