import re

usuario= re.compile(r"^[\w\-\.]{4,12}$")
contra= re.compile(r"(?=\S*?[A-Z])(?=\S*?[a-z])(?=\S*?[0-9])\S{6,}$")
correo= re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def usuario_valido(user):
	return user and usuario.match(user)

def contra_valida(password):
	return password and contra.match(password)

def correo_valido(email):
	return email and correo.match(email)
	