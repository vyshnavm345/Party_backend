from django.contrib import admin

from .models import OTP, BaseUser, Candidate, DeviceToken, District, Member

admin.site.register(BaseUser)
admin.site.register(Candidate)
admin.site.register(Member)
admin.site.register(OTP)
admin.site.register(District)
admin.site.register(DeviceToken)
