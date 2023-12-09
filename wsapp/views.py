from django.http import HttpResponse
from django.shortcuts import render
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import json
import time
# Create your views here.


async def home(request):
    channel_layer = get_channel_layer()
    for i in range(10):
        data = {'count':i}
        await channel_layer.group_send(
            'new_consumer_group',
            {
                'type':'CountApp',
                'value':json.dumps(data)
            }
        )
    return render(request,'home.html')

# def home(request):
#     channel_layer = get_channel_layer()
#     for i in range(10):
#         data = {'count':i+1}
#         async_to_sync(channel_layer.group_send)(
#             'test_consumer_group',{
#                 'type':'CountApp',
#                 'value':json.dumps(data)
#             }
#         )
#     return render(request,'home.html')


def home(request):
    return HttpResponse("<h1>Hello world</h1>")    