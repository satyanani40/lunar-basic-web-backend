from models import Usernote
from rest_framework_mongoengine.serializers import MongoEngineModelSerializer
from rest_framework import serializers

class UsernoteSerializer(MongoEngineModelSerializer):
    class Meta:
        model = Usernote