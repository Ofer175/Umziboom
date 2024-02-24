from Cryptodome.Cipher import AES
from Cryptodome.Hash import SHA256
import base64
import hashlib
from Cryptodome import Random
from Cryptodome.Util.Padding import unpad


class Encrypt:
    """
    class to encrypt and decrypt messages
    """
    def __init__(self):
        """
        initializing keys dictionary and creating Encrypt object
        """
        self.encrypt_keys = {}  # dictionary of clients keys
        self.bs = AES.block_size    # block size

    def add_key(self, key, ip=None):
        """
        adds key to encrypt_keys
        :param key: key of client
        :param ip: ip of client
        :return: None
        """
        self.encrypt_keys[ip] = key

    def encrypt(self, raw, ip=None):
        """
        encrypting raw with client key
        :param raw: data to encrypt
        :param ip: ip of client to get key
        :return: returns the encrypted message
        """
        if ip:
            key = hashlib.sha256(self.encrypt_keys[ip].encode()).digest()
        else:
            key = hashlib.sha256(list(self.encrypt_keys.values())[0].encode()).digest()

        # change to bytes
        if type(raw) == str:
            raw = raw.encode()

        raw = self._pad(raw)

        iv = Random.new().read(self.bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc, ip=None):
        """
        decrypting raw with client key
        :param enc: encrypted data
        :param ip: ip of client to get key
        :return: returns the decrypted message
        """
        if ip:
            key = hashlib.sha256(self.encrypt_keys[ip].encode()).digest()
        else:
            key = hashlib.sha256(list(self.encrypt_keys.values())[0].encode()).digest()

        enc = base64.b64decode(enc)
        iv = enc[:self.bs]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt(enc[self.bs:]), self.bs)

    def _pad(self, s):
        """
        Internal method, pads bytes for encryption
        :param s: Bytes to pad
        :return: Padded bytes
        """
        s = (s + (self.bs - len(s) % self.bs) * bytes([self.bs - len(s) % self.bs]))
        return s

    @staticmethod
    def hash(message):
        h = SHA256.new()
        h.update(message.encode())
        return h.hexdigest()


if __name__ == '__main__':

    pass
