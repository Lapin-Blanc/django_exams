# -*- coding: utf-8 -*-
from django.contrib import admin
from evaluation.models import QuestionCategory, QuestionCapture, ZoneImage, QuestionChoixMultiple, Choix, Questionnaire, QuestionnaireLine, Examen, ExamenLine

admin.site.register(QuestionCategory)

# Administration des questions
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

# Administration des questionnaires d'examen
class QuestionnaireLineInline(admin.TabularInline):
    model = QuestionnaireLine
    extra = 1

class QuestionnaireAdmin(admin.ModelAdmin):
    inlines = [QuestionnaireLineInline,]
    class Media:
        js = (
        '//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js',
        '//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js',
        '/static/js/inline_sortable.js',
        )
        css = {"all" : ('//ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css',)
        }

# Administration des examens
class ExamenLineInline(admin.TabularInline):
    model = ExamenLine

    can_delete = False
    extra = 0
    editable_fields = []
    
    extra = 0

    def get_readonly_fields(self, request, obj=None):
        fields = []
        for field in self.model._meta.get_all_field_names():
            if (not field == 'id'):
                if (field not in self.editable_fields):
                    fields.append(field)
        return fields
    
    def has_add_permission(self, request):
        return False

class ExamenAdmin(admin.ModelAdmin):
    
    def get_readonly_fields(self, request, obj=None):
        if obj: # obj is not None, so this is an edit
            return ['utilisateur', 'questionnaire', 'debut', 'fin', 'resultat']
        else: # This is an addition
            return ['debut', 'fin', 'resultat']

    inlines = [ExamenLineInline,]

admin.site.register(Questionnaire, QuestionnaireAdmin)
admin.site.register(Examen, ExamenAdmin)
