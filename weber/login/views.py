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



# Create your views here.

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User_save = User.create_user(username=username,email=None,password=password)
        User_save.save()
        return HttpResponseRedirect('/theweber.in/')
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
            user = authenticate(username=username,password=password)#request.POST['password']):
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponse(1)
            else:
                return HttpResponse(0)
    except Exception as e:
        return HttpResponse(e)




