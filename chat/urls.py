from django.urls import path
from chat import views
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('',views.home,name="home"),
    path('chats',views.chats,name="chats"),
    path('chat/<id>',views.chat,name="chat"),
    path('register',views.register,name="register"),
    # path('logout',LogoutView.as_view(),name="logout"),
    path('logout',views.logoutview,name="logout"),

    # path('sample/base',TemplateView.as_view(template_name = 'chat/sample/base.html')),
    # path('sample/home',TemplateView.as_view(template_name = 'chat/sample/home.html')),
    # path('sample/another',TemplateView.as_view(template_name = 'chat/sample/another.html')),
]