import random
import hashlib
from string import letters

def random_key(size=16):
	return "".join(random.choice(letters) for n in xrange(size))

def hash_contra(name, pw, salt=None):
	if not salt:
		salt= random_key()
	pw_hashed= hashlib.sha512(name+pw+salt).hexdigest()
	return "%s,%s"(pw_hashed, salt)

def contra_valida(name, pw, pw_h):
	salt= pw_h.split(",")[1]
	return pw_h== hash_contra(name, pw, salt)