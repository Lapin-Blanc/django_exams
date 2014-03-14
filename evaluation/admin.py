from django.contrib import admin
from evaluation.models import QuestionCapture, QuestionChoixMultipleTexte, QuestionChoixMultipleImage

admin.site.register(QuestionCapture)
admin.site.register(QuestionChoixMultipleTexte)
admin.site.register(QuestionChoixMultipleImage)
