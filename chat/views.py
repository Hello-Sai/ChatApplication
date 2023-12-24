import json
from django.conf import settings
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize
from chat.models import Profile,Message
from django.db.models import Q
# Create your views here.

def home(request):
    if request.method =="POST":
        user_name = request.POST['user_name']
        try:
            user = User.objects.get(username=user_name)
            login(request,user)
            return redirect('/chats')
        except User.DoesNotExist:
            messages.error(request,"You Don't have an account.","danger")
        except Exception as e:
            messages.error(request,"Got an Error %s"%e,"danger")
    return render(request,'chat/home.html')

@csrf_exempt
@login_required
def chats(request):
    profiles= Profile.objects.exclude(user = request.user)
    return render(request,'chat/chats.html',{'profiles':profiles})

def chat(request,id):
    profile = User.objects.get(id = id).profile
    profiles= Profile.objects.exclude(user = request.user)# to Show all Profiles in page
    messages = Message.objects.filter(
        Q(recepient = request.user.profile,sender = profile) | Q(recepient = profile,sender = request.user.profile)
        )
    # to Get Messages
    return render(request,'chat/chat.html',{'profile':profile,'profiles':profiles,'messagess':messages})
def register(request):
    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if (username is None) or (password is None):
            messages.info(request,"UserName and Password Should be Filled","danger")
        user = User.objects.create(username = username,password=password)
        profile = Profile.objects.create(user = user)
        if not profile:
            messages.error(request,"Profile Not Created","danger")
        messages.success(request,"Successfully Created Account")
        return redirect('home')
    return render(request,"chat/register.html")