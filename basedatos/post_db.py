from google.appengine.ext import ndb
from google.appengine.api import memcache
import logging


class dbComentarios(ndb.Model):
	usuario= ndb.StringProperty(required=True)
	asunto= ndb.StringProperty(required=True)
	comentario= ndb.TextProperty(required=True)
	creado= ndb.DateTimeProperty(auto_now_add=True)


def parent_post():
	return ndb.Key("Blog", "post")


class dbEntradas(ndb.Model):
	title= ndb.StringProperty(required=True)
	post= ndb.TextProperty(required=True)
	topic= ndb.StringProperty(required=True)
	user= ndb.StringProperty(required=True)
	fecha_creacion= ndb.DateTimeProperty(auto_now_add=True)
	fecha_modificacion= ndb.DateTimeProperty(auto_now=True)
	score= ndb.IntegerProperty(default=0)
	status= ndb.BooleanProperty(default=True)
	comentarios= ndb.StructuredProperty(dbComentarios, repeated=True)

	
		
	@classmethod
	def guardar_post(cls, titulo, post, topic, user):
		post= dbEntradas(parent=parent_post(), title=titulo, 
							post=post, topic=topic, user=user)
		post.put()
		return post

	@classmethod
	def query_post(cls):
		query= dbEntradas.query(ancestor=parent_post()).filter(
								dbEntradas.status== True)
		return query

	@classmethod
	def post_recientes(cls):
		posts= cls.query_post().order(-dbEntradas.fecha_creacion).fetch(10)	
		return list(posts)

	@classmethod
	def mas_populares(cls):
		posts = cls.query_post().order(-dbEntradas.score).fetch()
		return list(posts)

	@classmethod
	def get_post(cls, post_id):
		key= ndb.Key("dbEntradas", int(post_id), parent=parent_post())
		post= key.get()
		return post

	@classmethod
	def post_by_filtro(cls, filtro):
		posts= cls.query_post().filter(dbEntradas.topic==filtro).order(
				-dbEntradas.fecha_creacion).fetch()
		return list(posts)



class topicsCantidad(ndb.Model):
	cantidad_topics= ndb.PickleProperty()
	created= ndb.DateTimeProperty(auto_now_add=True)
	last_modified= ndb.DateTimeProperty(auto_now=True)

	@classmethod
	def actualizar_topics(cls):
		topics= dbEntradas.query(ancestor=parent_post()).fetch(
									projection=[dbEntradas.topic])
		cantidad=0
		total= dict(Programing=0, Sports=0, Science=0, Culture=0, 
						Games=0, News=0, Technology=0)
		for cadaTopic in topics:
			cantidad+=1
			total[cadaTopic.topic]+=1
		topic= topicsCantidad.get_by_id(6158364627173376)
		topic.cantidad_topics=total
		topic.put()

	@classmethod
	def get_nTopics(cls):
		t= topicsCantidad.get_by_id(6158364627173376)
		return t.cantidad_topics
		
