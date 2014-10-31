from django.shortcuts import render
from django.shortcuts import *
from django.http import HttpResponse
from models import Userpost
#from django.contrib.auth import User
from mongoengine.django.auth import User
from mongoengine.queryset import Q

import json
from django_sse.redisqueue import RedisQueueView
from django_sse.redisqueue import send_event
from myapp.utils import redis_connection, emit_to_channel

from serializers import *
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseRedirect
from models import Friends,Postdetails
from models import myfriends
from django import template
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.views.decorators.csrf import csrf_exempt
from myapp.views import *
from django.contrib.auth.hashers import make_password,check_password

from models import *
from forms import  DocumentForm

import datetime
import time

intial_time =  time.mktime(datetime.datetime(1990, 1, 1, 1, 1,1,1).timetuple())
intial_time2 =  time.mktime(datetime.datetime(1990, 1, 1, 1, 1,1,1).timetuple())

class SSE(RedisQueueView):
    def get_redis_channel(self):
       return "sse_%s" % self.request.user.id

#check friends request and notifications

def frnd_notifications(request):
    global intial_time
    global intial_time2
    intial_time=  time.mktime(datetime.datetime(1990, 1, 1, 1, 1,1,1).timetuple())
    intial_time2 =  time.mktime(datetime.datetime(1990, 1, 1, 1, 1,1,1).timetuple())

    while(1):
        data = check_newnotifications(request.user.id, intial_time, intial_time2)
        time.sleep(10)

def check_newnotifications(userid, it1, it2):
    #new friend request came or not

    new_frnd_reqsts  = Friends_new.objects(receiver_frnd = userid, status='1', request_time__gt= it1).order_by('request_time','-request_time')
    new_accept_reqsts= Friends_new.objects(sender_frnd = userid, status='2', request_time__gt= it2).order_by('request_time','-request_time')


    if new_frnd_reqsts:
        global intial_time
        intial_time = new_frnd_reqsts[0].request_time
        serialize_data1 = Friends_newSerializer(new_frnd_reqsts)
        data = json.dumps({'new_frnd_requests': serialize_data1.data}, cls= DjangoJSONEncoder)
        send_event("frnd_notifications",data, 'sse_%s' % userid)


    elif new_accept_reqsts:
        global inital_time2
        inital_time2 = new_accept_reqsts[0].request_time
        serialize_data2 = Friends_newSerializer(new_accept_reqst)
        data = json.dumps({'new_accept_notifications': serialize_data2.data}, cls= DjangoJSONEncoder)
        send_event("frnd_notifications",data, 'sse_%s' % userid)

    else:
        data = 'nothing to display'
    return data


def delete_post(request):
    if request.method =='POST':
        try:
            del_doc = Userpost.objects.get(id=request.POST['deletepostid'],userid=Userpost.objects.first().userid.id)
            if del_doc:
                del_doc.delete()
                return HttpResponse(request.POST['deletepostid'])
        except Exception as e:
            return HttpResponse(e)


@csrf_exempt
def post_status(request):
    try:
        store_postdata = json.loads(request.body)
        new_post = Userpost.objects.create(title=store_postdata['post_text'],
                                           username=request.user.username,
                                           publish_date=datetime.datetime.now(),
                                           permission_type=store_postdata['permission_type'],
                                           userid = User(id=request.user.id))
        d = UserpostSerializer(new_post)
        data =  json.dumps({'newpost':1,'data':d.data}, cls = DjangoJSONEncoder)
        r = redis_connection()
        #send_event("myevent",data, 'sse_%s' % request.user.username)
        send_event("myevent",data)
        return HttpResponse(1)
    except Exception as e:
        return HttpResponse(e)

def load_scroll_posts(request):
    if request.method == 'POST':
        post_id = request.POST['post_id']
        loaded_posts = Userpost.objects.filter(id__lt = post_id,permission_type=1).limit(2).order_by('-publish_date')
        return render(request,'ajax_out.html',{'load_remain_posts':loaded_posts,'action' : 'loadscrollposts'})


@login_required(login_url='/theweber.in/login')
def search_titles(request):
    #search_text = ''
    if request.method == "POST":
        data = json.loads(request.body)
        search_text = data['search_text']
        names = User.objects.filter(username__contains=search_text)
        dd = Userserializer(names)
        return HttpResponse(json.dumps(dd.data,cls = DjangoJSONEncoder))


# every thing ok upto here
@csrf_exempt
def get_profile_info(request,username):
    friends_list = "no friends"
    details = get_userbasic_info(username)
    userposts = getuserposts(username)

    fs = get_userfriends(details['id'])
    if fs:
        friends_listSerilizer = Friends_newSerializer(fs)
        friends_list = friends_listSerilizer.data

    #check selected user is same as logged user
    if(details['id'] == str(request.user.id)):
        friend_status = 'ownaccount'
        data =  json.dumps({'basicinfo':details,
                        'userposts':userposts,
                        'friendstatus':friend_status,
                        'friends':friends_list}, cls = DjangoJSONEncoder)

    elif(details['id'] != str(request.user.id)):
            friend_status = get_friend_status(request.user.id,details['id'])
            data =  json.dumps({'basicinfo':details,
                        'userposts':userposts,
                        'friendstatus':friend_status,
                        'friends':friends_list
                               }, cls = DjangoJSONEncoder)
    else:
        data = ""
    return HttpResponse(data)

    #return HttpResponse(serialize_data.data)
def get_userfriends(user_id):
    friends = Friends_new.objects(
            (
                (Q(sender_frnd = user_id) | Q(receiver_frnd = user_id)) & Q(status = '2')
            )
        )
    return friends


def get_userbasic_info(username):
    user_details = User.objects.get(username=username)
    info = Userserializer(user_details)
    return (info.data)

def getuserposts(username):
    uposts = Userpost.objects.filter(username=username).order_by('-publish_date').limit(1)
    posts = UserpostSerializer(uposts)
    return (posts.data)


def is_friend(friend1,friend2):
    status= 0
    frnd = Friends_new.objects(
        (
            (Q(sender_frnd = friend1) & Q(receiver_frnd= friend2) & Q(status='2')) |
            (Q(sender_frnd = friend2) & Q(receiver_frnd= friend1) & Q(status='2'))
        )
    )
    if frnd:
        status = 1
    return status

def is_alredysent(friend1,friend2):
    status= 0
    frnd = Friends_new.objects(
        (
            (Q(sender_frnd = friend1) & Q(receiver_frnd= friend2) & Q(status='1')) |
            (Q(sender_frnd = friend2) & Q(receiver_frnd= friend1) & Q(status='1'))
        )
    )
    if frnd:
        status = 1
    return status


def is_addfriend(friend1,friend2):
    status= ''
    frnd = Friends_new.objects(
        (
            (Q(sender_frnd = friend1) & Q(receiver_frnd = friend2)) |
            (Q(sender_frnd = friend2) & Q(receiver_frnd = friend1) )
        )
    )
    if frnd:
        status = 0
    else:
        status = 1
    return status

def get_friend_status(friend1,friend2):
    friend_status = 0

    if is_friend(friend1,friend2):
        friend_status = 'friends'
        return friend_status

    elif is_alredysent(friend1,friend2):
        friend_status = 'alredysent'
        return friend_status

    elif is_addfriend(friend1,friend2):
        friend_status = 'addfriend'

    else:
        friend_status = 'somthing went wrong'
    return friend_status



def add_friend(request):
    status = 0
    if request.method=='POST':
        post_data = json.loads(request.body)
        rs = is_addfriend(request.user.id, post_data['addfriendid'])
        if rs:
            status = add_newfriend(request.user.id, post_data['addfriendid'])
        else:
            status = 0

    return HttpResponse(status)

def add_newfriend(friend1, friend2):
    status = 0
    new_friend = Friends_new.objects.create(sender_frnd=friend1,
                                            receiver_frnd= friend2,status='1',
                                            request_date=datetime.datetime.now,
                                            request_time=time.mktime((datetime.datetime.now()).timetuple()))
    if new_friend:
        status =  1

    return status
@csrf_exempt
def cancelrequest(request):
    status = 0
    if request.method=='POST':
        post_data = json.loads(request.body)
        if is_alredysent(request.user.id, post_data['cancelid']) or is_friend(request.user.id, post_data['cancelid']):
            d = del_document(request.user.id, post_data['cancelid'])
            if d:
                status = 1
    return HttpResponse(status)


def del_document(friend1, friend2):
    status = 0
    d = Friends_new.objects(sender_frnd= friend1, receiver_frnd= friend2)
    if d:
        d[0].delete()
        status = 1
    else:
        d = Friends_new.objects(sender_frnd= friend2, receiver_frnd= friend1)
        d[0].delete()
        status = 1
    return status
@csrf_exempt

def accept_friend(request):
    done_accept = 0
    if request.method == "POST":
        sender_id = request.POST['senderid']
        status = is_alredysent(request.user.id,sender_id)
        if status:
            rs = Friends_new.objects.filter(sender_frnd=sender_id).update(
                set__status='2',
                set__request_date=datetime.datetime.now,
                set__request_time=time.mktime((datetime.datetime.now()).timetuple())
                )
            if rs:
                done_accept = 1
    return done_accept

def change_password(request):
    if request.method=='POST':
        status = 0
        requested_data = json.loads(request.body)
        enc_pass = make_password(requested_data['password'])
        rs = User.objects(id=request.user.id).update(set__password=enc_pass)
        if rs:
            status = 1
        return HttpResponse(status)

def change_gender(request):
    if request.method=='POST':
        status = 0
        requested_data = json.loads(request.body)
        rs = User.objects(id=request.user.id).update(set__gender=requested_data['gender'])
        if rs:
            status = 1
        return HttpResponse(status)



def update_birthdate(request):
    if request.method=="POST":
        requested_data = json.loads(request.body)
        rs = User.objects(id=request.user.id).update(set__birth_date=datetime.datetime(requested_data['year'],
                                                                                       requested_data['month'],
                                                                                       requested_data['day']))
        if rs:
            status = 1
        return HttpResponse(status)


#==========new editing upto this mark
def get_selected_user_info(request,username):
    f_status = 'addfriend'
    user_details = User.objects.get(username=username)
    friendslist = Friends.objects(friend1=request.user.id,myfriendslist__myfriends_ids=str(user_details.id))
    logged_user_friends = Friends.objects(friend1=user_details.id)
    post_details = getuserposts(username)

    if logged_user_friends:
        friends_details = my_frnds(logged_user_friends)
        final_friends_list = User.objects(id__in=friends_details)
    else:
        final_friends_list = ""

    selected_udi = user_details.id
    loggeduserid = request.user.id
    if selected_udi==loggeduserid:
        f_status = 'selectedmyself'

    else:
        if friendslist:
            f_status = sel_frnd_status(user_details,selected_udi,friendslist)
    return render(request,'profile.html',{'f_status':f_status,'user_details':user_details,'selid':selected_udi,
                                          'post_details':post_details,'friends_details':final_friends_list})

def my_frnds(friendslist):
    a = []
    for temp in friendslist:
        for temp2 in temp.myfriendslist:
            a.append(temp2.myfriends_ids)
    return a

def update_info(request):
   if request.method == 'POST':
       return render(request,'updateinfo.html',{})

def getuserdetailsbyid(user_id):
    return User.objects(id=user_id)




def update_userinfo(request):
    if request.method == 'POST':
        u = User.objects(id=request.user.id).update(set__username=request.POST['username'])
        if u:
            return HttpResponse('successfully saved')
        else:
            return HttpResponse('failded to save')
    else:
        return False


@csrf_exempt
def loaded_userposts(request):
    try:
        data = Userpost.objects.filter().order_by('-publish_date').limit(10)
        serialize_data = UserpostSerializer(data)
        data =  json.dumps(serialize_data.data, cls=DjangoJSONEncoder)
        return HttpResponse(data)
    except Exception as e:
        return HttpResponse(e)

def savepost(request):

        if request.method == 'POST':
            try:
                f = Postdetails(postname = request.POST['postname'])
                f.save()
                return render(request,'savepost.html',{})
            except Exception as e:
                return render(request,'savepost.html',{'e':e})
        else:
            return render(request,'savepost.html',{})

@csrf_exempt
def upload_profile_pic(request):
    try:
        if request.method == 'POST':

            #data = json.loads(request.body)
            #return  HttpResponse(request.FILES['file'])
            #return HttpResponse(request.FILES['myFile'])
            #form = DocumentForm(request.POST,request.FILES)
            #if form.is_valid():

            #store_postdata = json.loads(request.body)

            #return HttpResponse(json.dumps('sdfdsfsd'))
            uploaded_pic = user_pics(docfile=request.FILES['file'])
            uploaded_pic.save()

            #uploaded_pic = user_pics.objects.filter(docfile=uploaded_pic)
            data = uploaded_pic['docfile'].read()
            #return HttpResponse(readed_imaged,content_type='image/jpeg')
            #return HttpResponse("data:image/jpg;base64,%s" % data.encode('base64'))
            return HttpResponse("data:image/jpg;base64,%s" % data.encode('base64'))

    except Exception as e:
        return HttpResponse(e)