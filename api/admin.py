from api.models import *
from django.contrib import admin

class CustomDisplay(admin.ModelAdmin):
    list_display = ("name", "patient","diff","time_taken","isVegetarian")

admin.site.register(Recipe,CustomDisplay)

admin.site.register(Patient)





