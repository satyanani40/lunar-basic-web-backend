from mongoengine import *
connect('test')

class User1(Document):
    username = StringField(max_length=120, required=True)
    password = StringField(max_length=500, required=True)