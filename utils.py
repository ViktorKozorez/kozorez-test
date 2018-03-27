import hashlib
import random
import string


def random_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def MD5_generator(params, secret):
    hash = ':'.join(str(param) for param in params)
    hash += secret
    md5 = hashlib.md5(hash.encode()).hexdigest()
    return md5
