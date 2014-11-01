from rest_framework_mongoengine.serializers import MongoEngineModelSerializer
from mongoengine import *
from mongoengine.django.auth import User
from rest_framework import serializers
from home_func.models import *

class PostdetailsSerializer(MongoEngineModelSerializer):
    class Meta:
        model = Postdetails

class Userserializer(MongoEngineModelSerializer):
    class Meta:
        model = User
        
class UserpostSerializer(MongoEngineModelSerializer):
    class Meta:
        model = Userpost


class Friends_newSerializer(MongoEngineModelSerializer):
    class Meta:
        model = Friends_new

class user_picsSerializer(MongoEngineModelSerializer):
    class Meta:
        model = user_pics



