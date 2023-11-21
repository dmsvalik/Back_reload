from django.contrib import admin

from .models import MessageModel, ChatModel

admin.site.register(MessageModel)
admin.site.register(ChatModel)
