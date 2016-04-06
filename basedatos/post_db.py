from google.appengine.ext import db





class dbEntradas(db.Model):
	title= db.StringProperty(required=True)
	post= db.TextProperty(required=True)
	topic= db.StringProperty(required=True)
	user= db.StringProperty(required=True)
	fecha_creacion= db.DateTimeProperty(auto_now_add=True)




