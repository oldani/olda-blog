import hmac
import hashlib

key="`1,2.3/4'5;6[]78=9-0<0>9:8}7{+6_54\3|2~1}lQodBDhelzlO-=Jd/H>Mdwt"

def hashear_cookie(valor):
	return "%s|%s"%(valor, hmac.new(key,valor, hashlib.sha256).hexdigest())

def cookie_valido(valor_hashed):
	valor= valor_hashed.split("|")[0]
	if valor_hashed== hashear_cookie(valor):
		return valor