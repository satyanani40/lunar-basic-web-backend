from mongoengine import *
from weber.settings import DBNAME
connect(DBNAME)
from mongoengine.django.auth import User



class Imageupload1(Document):
    path = StringField()
    #image_field = FileField(upload_to="images")


class Userpost(Document):
    title = StringField(max_length=1200000,required=True)
    #image_path =
    publish_date = DateTimeField()
    username = StringField(max_length=120,required=True)
    permission_type=IntField()
    userid = ReferenceField(User)



    #auto_id = IntField(required=True)
    #user_id = StringField(max_length=200)
class myfriends(EmbeddedDocument):
    myfriends_ids = StringField()
    status = StringField()

class Friends(Document):
    friend1 = ReferenceField(User)
    myfriendslist = ListField(EmbeddedDocumentField(myfriends))
    #permission_type=StringField(max_length=120,required=True)
    #auto_id = IntField(required=True)
    #user_id = StringField(max_length=200)

class Postdetails(Document):
    postname = StringField()
    postdate = DateTimeField()

class user_pics(Document):
    docfile = FileField()

class Friends_new(Document):
    sender_frnd = ReferenceField(User)
    receiver_frnd = ReferenceField(User)
    status = StringField()
    request_date = DateTimeField()
    request_time = IntField()
    unseen = BooleanField(default=False)


