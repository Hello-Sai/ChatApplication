from django.contrib import admin

from chat.models import ChatNotification, Profile,Message

# Register your models here.
admin.site.register([Profile,Message,ChatNotification])
# admin.site.register()