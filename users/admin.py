from django.contrib import admin
from users.models import *

class CustomDisplay(admin.ModelAdmin):
    list_display = ("user", "patient","isVegan")

admin.site.register(UserProfile,CustomDisplay)
