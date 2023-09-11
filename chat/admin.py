from django.contrib.admin import ModelAdmin, site
from chat.models import Message
from django.contrib import admin


class MessageModelAdmin(ModelAdmin):
    readonly_fields = ('timestamp',)
    # search_fields = ('id', 'body', 'user__username', 'recipient__username')
    list_display = ('id',)
    list_display_links = ('id',)
    # list_filter = ('user', 'recipient')
    date_hierarchy = 'timestamp'


site.register(Message, MessageModelAdmin)
