from google.appengine.ext import ndb
import logging




class dbEntradas(ndb.Model):
	title= ndb.StringProperty(required=True)
	post= ndb.TextProperty(required=True)
	topic= ndb.StringProperty(required=True)
	user= ndb.StringProperty(required=True)
	fecha_creacion= ndb.DateTimeProperty(auto_now_add=True)


class topicsCantidad(ndb.Model):
	cantidad_topics= ndb.PickleProperty()
	created= ndb.DateTimeProperty(auto_now_add=True)
	last_modified= ndb.DateTimeProperty(auto_now=True)

	@classmethod
	def actualizar_topics(cls):
		topics= dbEntradas.query().fetch(projection=[dbEntradas.topic])
		cantidad=0
		total= dict(Programing=0, Sports=0, Science=0, Culture=0, Games=0,
				News=0, Technology=0)
		for cadaTopic in topics:
			cantidad+=1
			total[cadaTopic.topic]+=1
		topic= topicsCantidad.get_by_id(6158364627173376)
		#topicsCantidad(cantidad_topics=total).put()
		topic.cantidad_topics=total
		topic.put()
		
				