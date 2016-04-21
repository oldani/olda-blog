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
		post_id= str(post.key.id())
		memcache.set(post_id, post)
		cls.post_recientes(update=True)
		return post_id

	@classmethod
	def query_post(cls):
		query= dbEntradas.query(ancestor=parent_post()).filter(
								dbEntradas.status== True)
		return query

	@classmethod
	def key_post(cls, post_id):
		key= ndb.Key("dbEntradas", int(post_id), parent=parent_post())
		return key

	@classmethod
	def post_recientes(cls, update=False):
		key="recientes"
		entradas= memcache.get(key)
		if entradas is None or update:
			posts= cls.query_post().order(-dbEntradas.fecha_creacion
											).fetch(10)
			entradas=list(posts)
			memcache.set(key, entradas)	
		return entradas

	@classmethod
	def mas_populares(cls):
		posts = cls.query_post().order(-dbEntradas.score).fetch()
		return list(posts)

	@classmethod
	def get_post(cls, post_id):
		post = memcache.get(post_id)

		if post is None:
			key= cls.key_post(post_id)
			post= key.get()
			memcache.set(post_id, post)
		return post

	@classmethod
	def post_by_filtro(cls, filtro):
		posts= cls.query_post().filter(dbEntradas.topic==filtro).order(
				-dbEntradas.fecha_creacion).fetch()
		return list(posts)

	@classmethod
	def usuario_post(cls, usuario, order_by):
		ordenar=None
		if order_by == "creacion":
			ordenar = -dbEntradas.fecha_creacion
		elif order_by == "score":
			ordenar= -dbEntradas.score
		posts= dbEntradas.query(ancestor= parent_post()).filter(
								dbEntradas.user == usuario).order(
								ordenar).fetch()
		return list(posts)

	@classmethod
	def status_post(cls, post_id, status):
		post= cls.get_post(post_id)
		if status:
			post.status= status
		else:
			post.status= status
		post.put()
		cls.post_recientes(update=True)
		topicsCantidad.actualizar_topics()

	@classmethod
	def guardar_comentario(cls, post_id, user, asunto, comentario):
		post= cls.get_post(post_id)
		post.score+=1
		post.comentarios.append(dbComentarios(usuario=user,
								asunto=asunto, comentario=comentario))
		post.put()
		memcache.set(post_id, post)
		return post

	@classmethod
	def delete_post(cls, post_id):
		key= cls.key_post(post_id)
		key.delete()
		cls.post_recientes(update=True)
		topicsCantidad.actualizar_topics()


id_entity=0
class topicsCantidad(ndb.Model):
	cantidad_topics= ndb.PickleProperty()
	created= ndb.DateTimeProperty(auto_now_add=True)
	last_modified= ndb.DateTimeProperty(auto_now=True)

	@classmethod
	def crear_entity(cls, cantidad):
		total= topicsCantidad(cantidad_topics=cantidad)
		total.put()
	
	@classmethod
	def recuperar_key(cls):
		key= topicsCantidad.query().fetch(1, keys_only=True)
		if key:
			return key[0].id()

	@classmethod
	def actualizar_topics(cls):
		topics= dbEntradas.query(ancestor=parent_post()).filter(
								dbEntradas.status== True).fetch(
									projection=[dbEntradas.topic])
		cantidad=0
		total= dict(Programing=0, Sports=0, Science=0, Culture=0, 
						Games=0, News=0, Technology=0)
		for cadaTopic in topics:
			cantidad+=1
			total[cadaTopic.topic]+=1
		key= cls.recuperar_key()
		if key:
			topic= topicsCantidad.get_by_id(key)
			topic.cantidad_topics=total
			topic.put()
		else:
			cls.crear_entity(total)

	@classmethod
	def get_nTopics(cls):
		key= cls.recuperar_key()
		if key:
			t= topicsCantidad.get_by_id(key)
			return t.cantidad_topics
		else:
			cls.actualizar_topics()
