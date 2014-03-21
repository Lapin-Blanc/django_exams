# -*- coding: utf-8 -*-
from django.contrib import admin
from evaluation.models import QuestionCategory, QuestionCapture, ZoneImage, QuestionChoixMultiple, Choix

admin.site.register(QuestionCategory)

# Question capture d'écran
class ZoneImageInline(admin.TabularInline):
    model = ZoneImage
    extra = 1

class QuestionCaptureAdmin(admin.ModelAdmin):
    list_display = ['numero', 'description', 'niveau', 'categorie',]
    list_display_links = ['numero','description']
    list_filter = ['niveau', 'categorie__nom',]
    inlines = [ZoneImageInline,]
admin.site.register(QuestionCapture, QuestionCaptureAdmin)

class ChoixInline(admin.TabularInline):
    model = Choix
    extra = 3

class QuestionChoixMultipleAdmin(admin.ModelAdmin):
    list_display = ['numero', 'description', 'niveau', 'categorie',]
    list_display_links = ['numero','description']
    list_filter = ['niveau', 'categorie__nom',]
    inlines = [ChoixInline,]
admin.site.register(QuestionChoixMultiple, QuestionChoixMultipleAdmin)