#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import logging
import time
import json

from basedatos.post_db import dbEntradas
from basedatos.usuarios_db import usuarios

from tools import cookies
from tools import validar_datos


from google.appengine.ext import db
from google.appengine.api import memcache


plantillas_dir= os.path.join(os.path.dirname(__file__),"plantillas")
jinja_env= jinja2.Environment(loader=jinja2.FileSystemLoader(plantillas_dir),
	                          autoescape=True)


class Handler(webapp2.RequestHandler):

	def write(self, *a, **b):
		self.response.write(*a, **b)

	def render_string(self, template, **c):
		t=jinja_env.get_template(template)
		return t.render(**c)

	def render(self, template, **d):
		self.write(self.render_string(template, **d))

	def set_cookie(self, name, valor):
		cookie_hasheado= cookies.hashear_cookie(valor)
		self.response.headers.add_header("Set-Cookie",
								 "%s=%s; Path=/"%(name, cookie_hasheado))

	def cookie_valido(self, name):
		cookie= self.request.cookies.get(name)
		return cookie and cookies.cookie_valido(cookie)

	def login(self, user_id):
		self.set_cookie("sesion", str(user_id))

	def logout(self):
		self.response.headers.add_header("Set-Cookie", "sesion=; Path=/")

	def is_login(self):
		cookie= self.cookie_valido("sesion")

		if cookie:
			return True
		else:
			return False

	def enviar_json(self, datos):
		data= json.dumps(datos)
		self.response.write(data)


def cachFront(update=False):
	key="top"
	entradas=memcache.get(key)
	if entradas is None or update:
		logging.error("DB QUERY")
		post= db.GqlQuery("select * from dbEntradas order by fecha_creacion desc limit 10")
		entradas=list(post)
		memcache.set(key, entradas)
	return entradas




class MainHandler(Handler):
    def get(self):
    	entradas= cachFront()
    	self.render("index.html", entradas=entradas, login=self.is_login())
    	


class NewPostHandler(Handler):

	def renderizar(self, error="", titulo="", post=""):
		self.render("entradas.html", titulo=titulo, post=post, error=error)

	def get(self):
		self.render("entradas.html")

	def post(self):
		titulo= self.request.get("title")
		topic= self.request.get("topic")
		post= self.request.get("post")

		if titulo and post  and (topic!="Choose one.."):
			entrada= dbEntradas(title=titulo, post=post, topic=topic)
			entrada.put()
			postId= str(entrada.key().id())
			time.sleep(1)
 			# bug de consistencia el cache se actializa antes de
 			# que se complete la transacion
			memcache.set(postId, entrada)
			cachFront(True)
			self.redirect('/%s' %postId)


		else:
			error="We need a title, a topic and your post"
			self.renderizar(error, titulo, post)


class PostHandler(Handler):
	def get(self, postId):
		post=memcache.get(postId)

		if post:
			self.render_post(post)
		else:
			post= dbEntradas.get_by_id(int(postId))
			if not post:
				self.redirect('/')
			memcache.set(postId, post)
			self.render_post(post)

	def render_post(self, post):
		self.render("post.html", post=post)

		

class SignUpHandler(Handler):
	def post(self):
		usuario= self.request.get("username")
		contra= self.request.get("password")
		contra_verificada= self.request.get("verify")
		correo= self.request.get("correo")
		bad_data=False
		parametros=list()
		data=dict()

		usuario_existe= usuarios.buscar_usuario(usuario)

		if usuario_existe:
			data["user"]="This username already exist"
			self.enviar_json(data)

		else:

			if not validar_datos.usuario_valido(usuario):
				bad_data=True
				parametros.append("username")

			if not validar_datos.contra_valida(contra):
				bad_data=True
				parametros.append("a password")

			elif contra_verificada!= contra:
				bad_data=True
				parametros.append("a password that match")

			if not validar_datos.correo_valido(correo):
				bad_data=True
				parametros.append("an email")

			if bad_data:
				data["badData"]= True
				data["errores"]=parametros
				self.enviar_json(data)
			else:
				registrar= usuarios.registrar(usuario, contra, correo)
				self.login(registrar.get("id"))
				data["username"]= registrar.get("username")
				self.enviar_json(data)

	
class LoginHandler(Handler):
	def post(self):
		username=self.request.get("username")
		password= self.request.get("password")

		cuenta= usuarios.logear(username, password)
		if cuenta:
			self.login(cuenta.get("id"))
		else:
			data["error"]= "Username or Password not valid, try again"
			self.enviar_json(data)		




app = webapp2.WSGIApplication([
    ('/?', MainHandler),
    ("/newpost", NewPostHandler),
    ("/([0-9]+)", PostHandler),
    ("/signup", SignUpHandler),
    ("/login", LoginHandler)
], debug=True)
