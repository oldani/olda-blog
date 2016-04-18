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

from basedatos.post_db import *
from basedatos.usuarios_db import dbUsuarios

from tools import cookies
from tools import validar_datos


from google.appengine.ext import ndb
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
		return cookie

	def who_login(self):
		user_id= self.is_login()
		if user_id:
			username= self.get_memcache(user_id)
			if username:
				return username
			else:
				usuario= dbUsuarios.get_by_id(int(user_id))
				self.set_memcache(user_id, usuario.username)
				return usuario.username


	def enviar_json(self, datos):
		data= json.dumps(datos)
		self.response.write(data)

	def set_memcache(self, key, value):
		return memcache.set(key, value)

	def get_memcache(self, key):
		return memcache.get(key)


	def cachFront(self, key="", update=False):
		entradas=memcache.get(key)
		if entradas is None or update:
			logging.error("DB QUERY")
			entradas=dbEntradas.post_recientes()
			memcache.set(key, entradas)
		return entradas




class MainHandler(Handler):
    def get(self):
    	entradas= self.cachFront(key="reciente")
    	topics= topicsCantidad.get_nTopics()
    	self.render("index.html", entradas=entradas, topics=topics,
    				 login=self.is_login(), username=self.who_login())
    	


class NewPostHandler(Handler):

	def renderizar(self, error="", titulo="", post=""):
		self.render("entradas.html", titulo=titulo, post=post, error=error, 
					login=self.is_login(), username=self.who_login())

	def get(self):
		if self.is_login():
			self.renderizar()
		else:
			self.render("404.html")

	def post(self):
		titulo= self.request.get("title")
		topic= self.request.get("topic")
		post= self.request.get("post")
		username= self.who_login()
		

		if titulo and post  and (topic!="Choose one.."):
			#entrada= dbEntradas(title=titulo, post=post, topic=topic, user=username)
			#entrada.put()
			entrada= dbEntradas.guardar_post(titulo, post, topic, username)
			postId= str(entrada.key.id())
			self.set_memcache(postId, entrada)
			#time.sleep(1)
			self.cachFront(key="reciente", update=True)
			topicsCantidad.actualizar_topics()
			self.redirect('/%s' %postId)


		else:
			error="We need a title, a topic and your post"
			self.renderizar(error, titulo, post)


		


class PostHandler(Handler):
	def get(self, postId):
		post=self.get_memcache(postId)

		if post:
			self.render_post(post)
		else:
			post= dbEntradas.get_post(postId)
			if not post:
				self.redirect('/')
			self.set_memcache(postId, post)
			self.render_post(post)

	def render_post(self, post):
		self.render("post.html", post=post, login=self.is_login(),
					username=self.who_login())

	def post(self, postId):
		usuario= self.who_login()
		asunto= self.request.get("subject")
		comentario= self.request.get("comentario")
		data=dict()

		if usuario and asunto!="" and (len(comentario)>10): 
			post= dbEntradas.guardar_comentario(postId, usuario,
												asunto, comentario)
		
			if post:
				comentarios= self.render_string("comentario.html", post=post)
				data["comentarios"]=comentarios
			else:
				error="Sorry, try again please!"
				data["error"]=error

		else:
			if len(comentario)<10:
				error="Your comment must have a least 10 characters!"
				data["error"]=error
			else:
				error="We need a subject and your comment, to save it!"
				data["error"]=error
		self.enviar_json(data)


	

		

class SignUpHandler(Handler):
	def post(self):
		usuario= self.request.get("username")
		contra= self.request.get("password")
		contra_verificada= self.request.get("verify")
		correo= self.request.get("correo")
		bad_data=False
		parametros=list()
		data=dict()

		usuario_existe= dbUsuarios.buscar_usuario(usuario)

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
				registrar= dbUsuarios.registrar(usuario, contra, correo)
				self.login(registrar.get("id"))
				data["username"]= registrar.get("username")
				self.enviar_json(data)

	
class LoginHandler(Handler):
	def post(self):
		username=self.request.get("username")
		password= self.request.get("password")
		data=dict()

		cuenta= dbUsuarios.logear(username, password)
		if cuenta:
			self.login(cuenta.get("id"))
			data["username"]= cuenta.get("username")
			self.enviar_json(data)
		else:
			data["error"]= "Username or Password not valid, try again"
			self.enviar_json(data)

class LogoutHandler(Handler):
	def get(self):
		self.logout()


class FilterHandler(Handler):
	def get(self):
		filtro= self.request.get("filtro")
		if filtro=="reciente" :
			lista_post= self.cachFront(key=filtro)

		elif filtro== "popular":
			lista_post= dbEntradas.mas_populares()
		else:
			lista_post= dbEntradas.post_by_filtro(filtro)
		post= self.render_string("postFiltro.html", entradas=lista_post)
		self.enviar_json(post)

class DashBoardHandler(Handler):
	def get(self):
		if self.is_login():
			self.dashboard()
		else:
			self.render("404.html")

	def dashboard(self):
		usuario= self.who_login()
		posts= dbEntradas.usuario_post(usuario)
		self.render("post_dashboard.html", username=usuario,
					posts= posts)

	def post(self):
		post_id= self.request.get("postid")
		estado= self.request.get("status")
		if estado=="true":
			dbEntradas.status_post(post_id, True)
		else:
			dbEntradas.status_post(post_id, False)



app = webapp2.WSGIApplication([
    ('/?', MainHandler),
    ("/newpost", NewPostHandler),
    ("/([0-9]+)", PostHandler),
    ("/signup", SignUpHandler),
    ("/login", LoginHandler),
    ("/logout", LogoutHandler),
    ("/filter", FilterHandler),
    ("/dashboard", DashBoardHandler)
], debug=True)
