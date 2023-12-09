from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('chat/<room_name>',views.chat)
]