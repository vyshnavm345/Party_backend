from django.contrib import admin

from .models import BaseUser, Candidate, Member

admin.site.register(BaseUser)
admin.site.register(Candidate)
admin.site.register(Member)