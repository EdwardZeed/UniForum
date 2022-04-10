import sqlite3
from Crypto.Hash import MD5


# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise
import bcrypt


class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()
        self.id = 0

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    # -----------------------------------------------------------------------------

    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")

        self.execute("DROP TABLE IF EXISTS Messanges")

        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0,
            pubkey TEXT,
            prikey TEXT
        );""")

        self.execute("""CREATE TABLE Messanges(
                            sender TEXT,
                            receiver TEXT,
                            message TEXT,
                            key TEXT, 
                            signature TEXT
                        );""")

        self.commit()
        # Add our admin user
        hash = MD5.new()
        hash.update(admin_password.encode())
        admin_password = hash.hexdigest()
        self.add_user('admin', admin_password)

    # -----------------------------------------------------------------------------
    #send a message
    # -----------------------------------------------------------------------------
    def send_message(self, sender, receiver, messange, key, signature):
        sql_cmd = """
                INSERT INTO Messanges
                VALUES('{sender}', '{receiver}', '{message}', '{key}', '{signature}')
            """
        sql_cmd = sql_cmd.format(sender=sender, receiver=receiver ,message=messange, key=key, signature=signature)
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    #get all messages
    # -----------------------------------------------------------------------------
    def get_messages(self):
        sql_query = """
                    select message, key, sender, receiver
                    from Messanges
        """

        self.execute(sql_query)

        return self.cur.fetchall()

    def get_sender(self):
        sql_query = """
                    select sender
                    from Messanges
        """

        self.execute(sql_query)

        return self.cur.fetchall()

    # -----------------------------------------------------------------------------
    # User handling
    # -----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, pubkey=None, prikey=None, admin=0):
        sql_cmd = """
                INSERT INTO Users
                VALUES({id}, '{username}', '{password}', {admin}, '{pubkey}', '{prikey}')
            """

        sql_cmd = sql_cmd.format(id=self.id, username=username, password=password, admin=admin, pubkey=pubkey, prikey=prikey)
        self.id += 1
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT 1
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)

        # If our query returns
        self.execute(sql_query)
        if self.cur.fetchone():
            return True
        else:
            return False

    def getUsername_Password(self):
        sql_query = """
                    select username, password
                    from Users
        """

        self.execute(sql_query)

        return self.cur.fetchall()

    def getUsername(self):
        sql_query = """
                    select username
                    from Users
        """

        self.execute(sql_query)

        return self.cur.fetchall()

    def getPublicKey(self, username):
        sql_query = """
                        select pubkey
                        from Users
                        where username = '{username}'
                    """

        self.execute(sql_query.format(username=username))
        return self.cur.fetchone()

    def getPrivateKey(self, username):
        sql_query = """
                    select prikey
                    from Users
                    where username = '{username}'
                """

        self.execute(sql_query.format(username=username))
        return self.cur.fetchone()

    def getSignature(self, username):
        sql_query = """
                    select signature
                    from Messanges
                    where sender = '{username}'
                """

        self.execute(sql_query.format(username=username))
        return self.cur.fetchone()


