
from cryptography.fernet import Fernet
from passlib.hash import argon2

class Hasher:
    def __init__(self, pepper_key: bytes):
        self.pepper = Fernet(pepper_key)

    def hash(self, pwd: str) -> bytes:
        # hash with argon2
        this_hash: str = argon2.using(rounds=10).hash(pwd)
        # convert this unicode hash string into bytes before encryption
        hashb: bytes = this_hash.encode('utf-8')
        # encrypt this hash using the global pepper
        pep_hash: bytes = self.pepper.encrypt(hashb)
        return pep_hash

    def check(self, pwd: str, pep_hash: bytes) -> bool:
        # decrypt the hash using the global pepper
        hashb: bytes = self.pepper.decrypt(pep_hash)
        # convert this hash back into a unicode string
        this_hash: str = hashb.decode('utf-8')
        # check if the given password matches this hash
        return argon2.verify(pwd, this_hash)

    @staticmethod
    def random_pepper() -> bytes:
        return Fernet.generate_key()

# To Run:
'''
# argon
    pepper = Hasher.random_pepper()
    hasher = Hasher(pepper)
    pwd_hash = hasher.hash(pwd)
    print(pwd_hash)

    pwd_hash2 = hasher.hash(pwd)
    print(pwd_hash2)

    print(hasher_AR.check(pwd, pwd_hash))
    print(hasher_AR.check(pwd_bad, pwd_hash))
'''