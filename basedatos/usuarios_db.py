from google.appengine.ext import ndb
from tools.pw import *



class dbUsuarios(ndb.Model):
	username= ndb.StringProperty(required=True)
	password= ndb.StringProperty(required=True)
	correo= ndb.StringProperty(required=True)

	@classmethod
	def registrar(cls, name, pw, email):
		pw_hashed= hash_contra(name, pw)
		usuario= dbUsuarios(username=name, password=pw_hashed, correo=email)
		usuario.put()
		user_id= usuario.key.integer_id()
		return dict(id=user_id, username=name)

	@classmethod
	def buscar_usuario(cls, name):
		user_data= dbUsuarios.query().filter(dbUsuarios.username==name).get()
		return user_data

	@classmethod
	def logear(cls, name, pw):
		cuenta= cls.buscar_usuario(name)
		if cuenta and contra_valida(name, pw, cuenta.password):
			return dict(id=cuenta.key.integer_id(), username=name)



			
