from django.contrib import admin
from .models import SiteUser, PersonalInformation

# Register your models here.
admin.site.register(SiteUser)
admin.site.register(PersonalInformation)
