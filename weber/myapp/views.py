# Create your views here.
import json
from django.views.generic import TemplateView
from django_sse.redisqueue import RedisQueueView
from django_sse.redisqueue import send_event
#from models import *
from myapp.utils import redis_connection, emit_to_channel
from django.http import HttpResponse
#from django.shortcuts import render
#from django.shortcuts import *
from django.http import HttpResponse
#from models import Usernote

#from serializers import *
from django.views.decorators.csrf import csrf_exempt

import datetime
# Create your views here.

class SSE(RedisQueueView):
    pass

@csrf_exempt
def sse_push_message(request):
    #if request.method == 'POST':
    r = redis_connection()
        #dd = Usernote.objects.create(title=request.POST['message'])
    #d = UsernoteSerializer(dd)
    send_event("myevent",json.dumps('hai'))
    return HttpResponse('OK')
