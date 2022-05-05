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

        self.execute("DROP TABLE IF EXISTS Messages")

        self.execute("DROP TABLE IF EXISTS Knowledge")

        self.execute("DROP TABLE IF EXISTS Coursedetail")

        self.execute("DROP TABLE IF EXISTS Career")

        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0,
            pubkey TEXT,
            is_muted INTEGER DEFAULT 0
        );""")

        self.execute("""CREATE TABLE Messages(
                            sender TEXT,
                            receiver TEXT,
                            message TEXT,
                            signature TEXT
                        );""")

        self.execute("""CREATE TABLE Knowledge(
                                    sender TEXT,
                                    message TEXT
                    );""")

        self.execute("""Create TABLE Coursedetail(
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    course_name TEXT,
                                    coursedetail TEXT 
                    );""")

        self.execute("""Create TABLE Career(
                                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                                            career_name TEXT,
                                            careerdetail TEXT 
                    );""")
        self.commit()

        hash = MD5.new()
        hash.update(admin_password.encode())
        admin_password = hash.hexdigest()
        self.add_user("admin", admin_password)
        self.add_coursedetail("INFO2222", "This is a test course")
        self.add_coursedetail("INFO2223", "This is a test course")
        self.add_coursedetail("INFO2224", "This is a test course")
        self.add_coursedetail("INFO2225", "This is a test course")

        self.add_career("Software Engineering", "This is a test career. SE is a great career")
        self.add_career("Data Science", "This is a test career. DS is a great career")
        self.add_career("Computer Science", "This is a test caree. CS is a great career")
        self.add_career("Information System", "This is a test career. IS is a great career")

    # -----------------------------------------------------------------------------
    # share knowledge
    # -----------------------------------------------------------------------------
    def share_knowledge(self, sender, message):
        sql_cmd = """
                    INSERT INTO Knowledge
                    VALUES('{sender}', '{message}')
                """
        sql_cmd = sql_cmd.format(sender=sender, message=message)
        self.execute(sql_cmd)
        self.commit()
        return True


    # -----------------------------------------------------------------------------
    #send a message
    # -----------------------------------------------------------------------------
    def send_message(self, sender, receiver, message, signature):
        sql_cmd = """
                INSERT INTO Messages
                VALUES('{sender}', '{receiver}', '{message}', '{signature}')
            """
        sql_cmd = sql_cmd.format(sender=sender, receiver=receiver ,message=message, signature=signature)
        self.execute(sql_cmd)
        self.commit()
        return True

    # -----------------------------------------------------------------------------
    #get all messages
    # -----------------------------------------------------------------------------
    def get_messages(self, receiver):
        sql_query = """
                    select message, sender, receiver, signature
                    from Messages
                    where receiver = '{receiver}'
        """
        sql_query = sql_query.format(receiver=receiver)
        self.execute(sql_query)

        return self.cur.fetchall()

    def get_knowledge(self):
        sql_query = """
                    select sender, message
                    from Knowledge
        """
        sql_query = sql_query.format()
        self.execute(sql_query)

        return self.cur.fetchall()

    def get_sender(self):
        sql_query = """
                    select sender
                    from Messages
        """

        self.execute(sql_query)

        return self.cur.fetchall()

    # -----------------------------------------------------------------------------
    # User handling
    # -----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, pubkey=None, admin=0,is_muted=0):
        sql_cmd = """
                INSERT INTO Users
                VALUES({id}, '{username}', '{password}', {admin}, '{pubkey}', '{is_muted}')
            """

        sql_cmd = sql_cmd.format(id=self.id, username=username, password=password, admin=admin, pubkey=pubkey, is_muted=is_muted)
        self.id += 1
        self.execute(sql_cmd)
        self.commit()

        return True

    # -----------------------------------------------------------------------------

    # Check login credentials
    def check_credentials(self, username, password):
        print(username, password)
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


    def getSignature(self, username):
        sql_query = """
                    select signature
                    from Messages
                    where sender = '{username}'
                """

        self.execute(sql_query.format(username=username))
        return self.cur.fetchone()


    def Delete_User(self, username):
        sql_cmd = """
                    DELETE FROM Users WHERE username = '{username}'
                """

        self.execute(sql_cmd.format(username=username))
        self.execute(sql_cmd)
        self.commit()
        return True

    def Mute_User(self, username):
        sql_cmd = """
                    UPDATE Users SET is_muted = 1 WHERE username = '{username}'
                """

        self.execute(sql_cmd.format(username=username))
        self.execute(sql_cmd)
        self.commit()
        return True

    def check_user_mute(self, username):
        sql_query = """
                            SELECT is_muted 
                            FROM Users
                            WHERE username = '{username}'
                        """
        self.execute(sql_query.format(username=username))
        return self.cur.fetchone()

    def get_all_knowledge(self):
        sql_query = """
                            select *    
                            from Knowledge
                        """
        self.execute(sql_query)
        return self.cur.fetchall()

    def add_coursedetail(self, course_name,coursedetail):
        sql_cmd = """
                        INSERT INTO Coursedetail(course_name,coursedetail)
                        VALUES ('{course_name}','{coursedetail}')
                    """
        self.execute(sql_cmd.format(course_name=course_name, coursedetail=coursedetail))
        self.commit()

    def get_coursedetail(self):
        sql_query = """
                                    select *
                                    from Coursedetail
                                """
        self.execute(sql_query)
        return self.cur.fetchall()

    def Delete_Course_Guide(self, course_guide):
        sql_cmd = """
                            DELETE FROM Coursedetail WHERE course_name = '{course_guide}'
                        """
        self.execute(sql_cmd.format(course_guide=course_guide))
        self.execute(sql_cmd)
        self.commit()
        return True

    def add_career(self, career, careerdetail):
        sql_cmd = """
                                    INSERT INTO Career(career_name,careerdetail)
                                    VALUES ('{career}','{careerdetail}')
                                """
        self.execute(sql_cmd.format(career=career, careerdetail=careerdetail))
        self.commit()
        return True

    def get_all_career(self):
        sql_query = """
                                    select *
                                    from Career
                                """
        self.execute(sql_query)
        return self.cur.fetchall()

    def Delete_Career(self, id):
        sql_cmd = """
                                    DELETE FROM Career WHERE id = '{id}'
                                """
        self.execute(sql_cmd.format(id = id))
        self.execute(sql_cmd)
        self.commit()
        return True




