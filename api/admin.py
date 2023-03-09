from api.models import Recipe, Patient, Error , Difficulty
from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

@admin.register(Recipe)
class RecipeAdmin(TranslationAdmin):
    list_display = ("name", "patient","difficulty","time_taken","isVegetarian")
    group_fieldsets = True
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Difficulty)
@admin.register(Patient)
class PatientAdmin(RecipeAdmin):
    list_display = ("name",)



admin.site.register(Error)









