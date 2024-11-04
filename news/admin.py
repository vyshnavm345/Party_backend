# Register your models here.
from django.contrib import admin

from .models import Event, News

admin.site.register(News)
admin.site.register(Event)
