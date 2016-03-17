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

from basedatos import post_db

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

CACHE={}
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
        self.render("index.html", entradas=entradas)


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
			entrada= post_db.dbEntradas(title=titulo, post=post, topic=topic)
			entrada.put()
			time.sleep(1)
			cachFront(True)
			self.redirect('/')


		else:
			error="We need a title, a topic and your post"
			self.renderizar(error, titulo, post)


app = webapp2.WSGIApplication([
    ('/?', MainHandler),
    ("/newpost", NewPostHandler)
], debug=True)
