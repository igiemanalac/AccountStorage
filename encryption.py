from Crypto import Random  # use to generate a random byte string of a length we decide
from Crypto.Cipher import AES
import hashlib
import base64
from hashlib import sha256

# Block size
BS = 16


@staticmethod
def pad(s):
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)


@staticmethod
def unpad(s):
    return s[0:-s[-1]]


class Encrypter:
    def __init__(self, key):
        self.key = sha256((key).encode('utf-8')).digest()

    def get_hexdigest(self, account_name, password):
        return sha256(account_name + password).hexdigest()

    def encrypt_text(self, raw):
        raw = pad.__func__(raw)
        init_vector = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, init_vector)
        return base64.b64encode(init_vector + cipher.encrypt(raw.encode('utf8')))

    def decrypt_text(self, enc):
        enc = base64.b64decode(enc)
        init_vector = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, init_vector)
        return unpad.__func__(cipher.decrypt(enc[16:]))


# cipher = Encrypter('m@st3r')
# encrypted = cipher.encrypt_text('A secret message!!!!')
# decrypted = cipher.decrypt_text(encrypted)
# print(encrypted)
# print(decrypted)
