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



class MainHandler(Handler):
    def get(self):
    	entradas= dbEntradas.post_recientes()
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
	
			entrada= dbEntradas.guardar_post(titulo, post, topic, username)
			topicsCantidad.actualizar_topics()
			self.redirect('/%s' %entrada)


		else:
			error="We need a title, a topic and your post"
			self.renderizar(error, titulo, post)



class PostHandler(Handler):
	def get(self, postId):
		usuario= self.who_login()
		post= dbEntradas.get_post(postId)
		if post:
			if not post.status and usuario != post.user:
				self.render("404.html")
			self.render_post(post)
		
		self.render("404.html")

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
			lista_post= dbEntradas.post_recientes()

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
		posts= dbEntradas.usuario_post(usuario, "creacion")
		self.render("post_dashboard.html", username=usuario,
					posts= posts)

	def post(self):
		accion_a_tomar= self.request.get("accion")
		post_id= self.request.get("postid")
		estado= self.request.get("status")

		if accion_a_tomar=="cambiarEstado":
			if estado=="true":
				dbEntradas.status_post(post_id, True)
			else:
				dbEntradas.status_post(post_id, False)
		elif accion_a_tomar=="delete":
			dbEntradas.delete_post(post_id)

class EstadisticasHandler(Handler):
	def get(self):
		pagina= self.request.get("page")
		usuario= self.who_login()
		self.json_board(pagina, usuario)
		

	def json_board(self, page, user):
		posts= dbEntradas.usuario_post(user, "score")
		popularidad_topic = dict(Programing=0, Sports=0, Science=0, 
								Culture=0, Games=0, News=0, Technology=0)

		if page== "tables":
			for cadaPost in posts:
				popularidad_topic[cadaPost.topic]+=cadaPost.score
			
			t= self.render_string("tables_dashboard.html",
									popular_post=posts[:5], 
									popularidad_topic=popularidad_topic)
		elif page == "charts":

			for cadaPost in posts:
				popularidad_topic[cadaPost.topic]+=1
			
			t= self.render_string("charts_dashboard.html",
									popularidad_topic=popularidad_topic)
		elif page == "post":
			posts= dbEntradas.usuario_post(user, "creacion")
			t= self.render_string("post_ajax_dash.html", posts=posts)

		self.enviar_json(t)


class EditarPostHandler(Handler):
	def get(self, post_id):
		post= self.get_post(post_id)
		t= self.render_string("editar_post.html", post=post)
		self.enviar_json(t)

	def post(self, post_id):
		post= self.request.get("post")
		post_db= self.get_post(post_id)
		post_db.post= post
		post_db.put()
		dbEntradas.post_recientes(update=True)
		self.enviar_json("a")

	def get_post(self, post_id):
		post= dbEntradas.get_post(post_id)
		return post




app = webapp2.WSGIApplication([
    ('/?', MainHandler),
    ("/newpost", NewPostHandler),
    ("/([0-9]+)", PostHandler),
    ("/signup", SignUpHandler),
    ("/login", LoginHandler),
    ("/logout", LogoutHandler),
    ("/filter", FilterHandler),
    ("/dashboard", DashBoardHandler),
    ("/estadisticas", EstadisticasHandler),
    ("/edit/([0-9]+)", EditarPostHandler)
], debug=True)
