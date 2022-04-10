from Crypto.Cipher import AES

import model
from sql import SQLDatabase
import base64
import rsa
import os
db = SQLDatabase("identifier.sqlite")
db.database_setup()
model.register_check("Edward", "123")
model.register_check("Frank", "123")
model.login_check("Edward", "123")
model.send_success("Frank", "test")
model.login_check("Frank", "123")
model.get_message()


public_key, private_key = rsa.newkeys(512)
pub = public_key.save_pkcs1().decode()
priv = private_key.save_pkcs1().decode()
# db.add_user("test", "test", pub, priv)



print("-------------------------------------")
message = "haha"
symmetric_key = os.urandom(16)
cipher = AES.new(symmetric_key, AES.MODE_ECB)
message = bytes(message, 'utf-8')
while len(message) % 16 != 0:
    message += b'\0'
cipherText = cipher.encrypt(message)

signature = rsa.sign(cipherText, private_key, 'SHA-1')
print(base64.encodebytes(signature).decode())
print(rsa.verify(cipherText, signature, public_key))


# msg = "message"
# cipher = rsa.encrypt(msg.encode(), public_key)
# print(cipher)
# cipher = base64.encodebytes(cipher)
# print(cipher.decode())
# cipher = cipher.decode()
# cipher = base64.decodebytes(cipher.encode())
# print(cipher)
# print(private_key)
# plainText = rsa.decrypt(cipher, private_key)
# print(plainText)


# pubfile = open('public.pem','w+')
# pubfile.write(pub.decode())
# pubfile.close()
#
# with open('public.pem') as publickfile:
#     p = publickfile.read()
#     pubkey = rsa.PublicKey.load_pkcs1(p)

# db.add_user("frank", "frank")
# print(db.getUsername())


# db.add_user("edward", "edward")
# print(db.cur.fetchone())
# print(db.check_credentials('admin', 'edward'))


# from Crypto.Hash import MD5
# message = "password"
# # initialise our
# # hash
# hash = MD5.new()
# # pass the message we want to
# hash.update(message.encode())
# # printing the hash
# print(hash.hexdigest())