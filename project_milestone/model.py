'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import rsa

import view
import random
from Crypto.Cipher import AES
import base64, os
import bcrypt
from sql import SQLDatabase


# Initialise our views, all arguments are defaults for the template
page_view = view.View()
db = SQLDatabase(database_arg="identifier.sqlite")
db.database_setup()
user_name_global = "null"

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# register
#-----------------------------------------------------------------------------

def register_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("register")

def register_check(username, password):
    '''
        login_form
        Returns the view for the login_form
    '''
    register = db.getUsername()
    for name in register:
        if username == name[0]:
            return page_view("invalid", reason="username already exists")
    public_key, private_key = rsa.newkeys(1024)
    pub = public_key.save_pkcs1().decode()
    priv = private_key.save_pkcs1().decode()

    db.add_user(username, password,pub, priv)
    return (page_view("success"))


#-----------------------------------------------------------------------------
# Send Message
#-----------------------------------------------------------------------------
def send_message_form():
    '''
        send_message
        Sends a message to the database

        :: username :: The username
        :: message :: The message

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    return page_view("friend-list")

def set_user_name(username):
    global user_name_global
    user_name_global = username

def get_sender():
    '''
        send_message
        Sends a message to the database

        :: username :: The username
        :: message :: The message

        Returns either a view for valid credentials, or a view for invalid credentials
    '''
    return user_name_global

def send_success(receiver, message):

    #encrypt message with symmetric key
    public_key = db.getPublicKey(receiver)
    public_key = public_key[0]
    symmetric_key = os.urandom(16)
    cipher = AES.new(symmetric_key, AES.MODE_ECB)
    message = bytes(message, 'utf-8')
    while len(message) % 16 != 0:
        message += b'\0'
    cipherText = cipher.encrypt(message)

    # encrypt symmetric key with receiver's public key
    symmetric_key = rsa.encrypt(symmetric_key, rsa.PublicKey.load_pkcs1(public_key))
    str_ciperText = base64.encodebytes(cipherText).decode()
    str_symmetric_key = base64.encodebytes(symmetric_key).decode()

    #generate digital signature
    private_key = db.getPrivateKey(user_name_global)
    private_key = private_key[0]
    private_key = rsa.PrivateKey.load_pkcs1(private_key)
    signature = rsa.sign(cipherText, private_key, 'SHA-1')
    str_signature = base64.encodebytes(signature).decode()

    db.send_message(user_name_global,receiver, str_ciperText, str_symmetric_key, str_signature)

    return page_view("success_send")

#-----------------------------------------------------------------------------
# Get_message
#-----------------------------------------------------------------------------
def get_message():
    '''
        get_message
        Returns the view for the get_message
    '''
    if user_name_global == db.get_sender()[0]:
        return page_view("get-message", sender = "", message="You have no messages")
    else:
        try:
            # verify signature
            msg = db.get_messages()
            msg_text = msg[len(msg) - 1][0]
            symmetric_key = msg[len(msg) - 1][1]
            sender = msg[len(msg) - 1][2]

            signature = db.getSignature(sender)
            signature = signature[0]
            signature = base64.decodebytes(signature.encode())
            sender_public_key = db.getPublicKey(sender)[0]
            msg_bytes = base64.decodebytes(msg_text.encode())
            rsa.verify(msg_bytes, signature, rsa.PublicKey.load_pkcs1(sender_public_key))

            # decrypt message
            private_key = rsa.PrivateKey.load_pkcs1((db.getPrivateKey(user_name_global)[0]).encode())
            symmetric_key = rsa.decrypt(base64.decodebytes(symmetric_key.encode()), private_key)
            cipher = AES.new(symmetric_key, AES.MODE_ECB)
            msg_text = cipher.decrypt(msg_bytes).decode()
            msg_text = msg_text.rstrip('\0')
            return page_view("get_message", sender =db.get_sender()[0], message=msg_text)
        except:
            return page_view("get-message", sender = "", message="the message might be corrupted")

#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True
    # accountls = []
    # with open("account.txt", 'r') as f:
    #     for i in f.readlines():
    #         accountls.append(i.strip("\n"))

    # binary_password = password.encode()
    # hashed_password = bcrypt.hashpw(binary_password, bcrypt.gensalt())
    # print(hashed_password)

    # for i in accountls:
    #     if username != i.split(",")[0]:  # Wrong Username
    #         err_str = "Incorrect Username"
    #         login = False
    #
    #     print(i.split(",")[1])
    #     if not bcrypt.checkpw(password.encode(), i.split(",")[1].encode()):  # Wrong password
    #         err_str = "Incorrect Password"
    #         login = False
    #
    #     if login:
    #         return page_view("valid", name=username)
    #     else:
    #         return page_view("invalid", reason=err_str)

    login = db.check_credentials(username, password)
    err_str = "a"
    username_ls = db.getUsername()

    if login:
        for i in username_ls:
            if username != i[0]:
                name_l = i[0]
        set_user_name(username)
        if(name_l == None):
            name_l = "null"
        return page_view("friend-list", name=name_l)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)