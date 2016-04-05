from google.appengine.ext import db
from tools.pw import *



class usuarios(db.Model):
	username= db.StringProperty(required=True)
	password= db.StringProperty(required=True)
	correo= db.StringProperty(required=True)

	@classmethod
	def registrar(cls, name, pw, email):
		pw_hashed= hash_contra(name, pw)
		usuario= usuarios(username=name, password=pw_hashed, correo=email)
		usuario.put()
		user_id= usuario.key().id()
		return dict(id=user_id, username=name)

	@classmethod
	def buscar_usuario(cls, name):
		user_data= usuarios.all().filter('username =', name).get()
		return user_data

	@classmethod
	def logear(cls, name, pw):
		cuenta= cls.buscar_usuario(name)
		if cuenta and contra_valida(name, pw, cuenta.password):
			return dict(id=cuenta.key().id(), username=name)



			
