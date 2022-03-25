from sql import SQLDatabase
db = SQLDatabase("identifier.sqlite")
db.database_setup()
db.add_user("frank", "frank")
print(db.getUsername_Password())
# db.add_user("edward", "edward")
# print(db.cur.fetchone())
# print(db.check_credentials('admin', 'edward'))


from Crypto.Hash import MD5
message = "password"
# initialise our
# hash
hash = MD5.new()
# pass the message we want to
hash.update(message.encode())
# printing the hash
print(hash.hexdigest())