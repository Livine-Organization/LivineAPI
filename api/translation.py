from modeltranslation.translator import register, TranslationOptions

from .models import *

@register(Recipe)
class RecipeTranslationOptions(TranslationOptions):
    fields = ('name', 'ingridents', 'directions')

@register(Patient)
class PatientTranslationOptions(TranslationOptions):
    fields = ('name',)    

@register(Difficulty)
class DifficultyTranslationOptions(TranslationOptions):
    fields = ('name',)