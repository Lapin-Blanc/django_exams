# -*- coding: utf-8 -*-
from django.contrib import admin
from evaluation.models import QuestionCapture, ZoneImage, QuestionChoixMultipleTexte, QuestionChoixMultipleImage, QuestionCategory

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


class QuestionChoixMultipleTexteAdmin(admin.ModelAdmin):
    list_display = ['numero', 'niveau', 'categorie', 'description',]
    list_filter = ['niveau', 'categorie__nom',]
admin.site.register(QuestionChoixMultipleTexte, QuestionChoixMultipleTexteAdmin)

class QuestionChoixMultipleImageAdmin(admin.ModelAdmin):
    list_display = ['numero', 'niveau', 'categorie', 'description',]
    list_filter = ['niveau', 'categorie__nom',]
admin.site.register(QuestionChoixMultipleImage, QuestionChoixMultipleImageAdmin)
