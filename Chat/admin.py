from django.contrib import admin

from Chat.models import Message, Room

admin.site.register(Message)
admin.site.register(Room)
