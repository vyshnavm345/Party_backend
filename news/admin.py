from django.contrib import admin

from .models import EventsFeed, NewsFeed

admin.site.register(NewsFeed)
admin.site.register(EventsFeed)
