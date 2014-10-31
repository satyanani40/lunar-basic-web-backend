from django.shortcuts import render
from django.shortcuts import render_to_response
#from forms import UserForm
from models import User1
from django.http import HttpResponse,HttpResponseRedirect
from mongoengine.queryset import DoesNotExist
from django.contrib import messages,auth
from mongoengine.django.auth import User
from django.contrib.auth import authenticate,logout
#from django.contrib.auth.models import check_password
#from mongoengine import *
from django.contrib.auth.decorators import login_required
from home_func.models import Userpost
from django.views.decorators.csrf import csrf_exempt
import json
import textwrap
from django.core.mail import EmailMessage
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import check_password, make_password
from django.views.generic import TemplateView




def send_invitation(request):
    if request.method == 'POST':
        email = request.POST['email']
        email1 = request.POST['email1']
        email2 = request.POST['email2']
        email_user = request.user.email

def password_reset_success(request):
    status = 0
    if request.method == 'POST':
        password1 = request.POST['password1']
        contain_password = make_password(password1)
        User.objects.get(email = request.session['reset_email_holder']).update(set__password=contain_password)
        status = 1
    else:
        status =0
    return HttpResponse(status)

def set_password(request,password_email):
    decoded_content = '\r\n'.join(textwrap.wrap(password_email.decode('base64'), 76))
    check_email = User.objects(email=decoded_content)
    if check_email:
        request.session['reset_email_holder'] = decoded_content
        return HttpResponseRedirect('/theweber.in/set_new_password')
    else:
        return HttpResponse('something went wrong')


def password_recovery(request):
    if request.method == 'POST':
        status = 0
        email = request.POST['email']
        check_email = User.objects.get(email=email)
        user_email = check_email.email
        encoded_content = '\r\n'.join(textwrap.wrap(user_email.encode('base64'), 76))



        ss = '127.0.0.1:8000/theweber.in/set_password/'+encoded_content
        subject, from_email, to = 'Websoc password recovery', email, user_email
        text_content = 'This is an important message.'
        html_content = '<h1 style="color:green;font-family:cursive, sans-serif;font-size: 25px;font-weight: bold;">' \
                       'This Is From Websoc Team</h1><br>' \
                       ' you are requested to change the password<br>' \
                       '<h4>if you are interested to change it please click on the link</h4>' \
                       '127.0.0.1:8000/theweber.in/set_password/'+encoded_content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        if msg.send():
            status = 1
        else:
            status = 0
        #email = EmailMessage('websoc password recovery',ss,to=[user_email])
        #email.send()
        return HttpResponse(status)



def email_confirmation(request,email):
    decoded_content = '\r\n'.join(textwrap.wrap(email.decode('base64'), 76))
    check_email = User.objects.get(email=decoded_content)
    check_email.is_active = True
    check_email.save()
    return HttpResponseRedirect('/theweber.in/login')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']  #request_data['username']
        password = request.POST['password']  #request_data['email']
        email = request.POST['email']       #request_data['email']
        User_save = User.create_user(username=username,email=email,password=password)
        User_save.save()

        user_email = User_save.email
        encoded_content = '\r\n'.join(textwrap.wrap(user_email.encode('base64'), 76))
        ss = '127.0.0.1:8000/theweber.in/activate/'+encoded_content
        subject, from_email, to = 'Websoc activation link', email, user_email
        text_content = 'This is an important message.'
        html_content = '<h1 style="color:green;font-family:cursive, sans-serif;font-size: 25px;font-weight: bold;">' \
                       'This Is From Websoc Team</h1><br>' \
                       ' you are requested to change the password<br>' \
                       '<h4>if you are interested to change it please click on the link</h4>' \
                       '127.0.0.1:8000/theweber.in/activate/'+encoded_content
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return HttpResponse('a link  has been sent to your '+user_email+' please click on the link')

    else:
        return render(request,'register.html')

@login_required(login_url='/theweber.in/login')
def home(request):
    if request.user.is_authenticated:
        posts = Userpost.objects.filter().order_by('-publish_date').limit(12)

        return render(request,'home.html',{'userposts': posts, 'username':request.user.username})
    else:
        return HttpResponseRedirect('/theweber.in/login')

#@csrf_exempt
def login_check(request):
    try:
        if request.method == 'POST':
            logindata = json.loads(request.body)
            username = logindata['username']
            password = logindata['password']

            user = authenticate(username=username, password=password)#request.POST['password']):
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponse(1)
            else:
                return HttpResponse(0)
    except Exception as e:
        return HttpResponse(e)

def is_useravaible(username):
    status = 0
    try:
        if username:
            User.objects.get(username=username)
            status = 1
    except Exception as e:
        status = 0
    return status








