from django.shortcuts import render,HttpResponse,redirect

# Create your views here.

def home(request):
    if request.method =="POST":
        room_name = request.POST['room_name']
        user_name = request.POST['user_name']
        return redirect(f'chat/{room_name}?user={user_name}')
    return render(request,'chat/home.html')
def chat(request,room_name):
    user = request.GET.get('user')
    return render(request,'chat/chat.html',{'room_name':room_name,'user':user})