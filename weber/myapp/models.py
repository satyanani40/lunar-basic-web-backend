from mongoengine import *
connect('test')

class Usernote(Document):
    title = StringField()


