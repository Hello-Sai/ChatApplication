from django.contrib import admin

from chat.models import Profile,Message

# Register your models here.
admin.site.register([Profile,Message])
# admin.site.register()