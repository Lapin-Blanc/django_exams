# -*- coding: utf-8 -*-
from django.db import models

# Classe Question principale
class Question(models.Model):
    numero = models.IntegerField(help_text=u"Un numéro pour identifier facilement la question")
    description = models.CharField(max_length=100, default=u"Description courte de la question", help_text=u"Pour identifier facilement la question")
    intitule = models.TextField(default=u"Entrez le texte de la question ici...", help_text=u"Les balises HTML sont accept&eacute;es")
    
    def __unicode__(self):
        question_type = getattr(self._get_subclass_question(),"question_type","")
        return u"{0:>04}[{1:>15}]: {2}".format(self.numero, question_type, self.description)
    
    def _get_subclass_question(self):
        from django.db.models.fields.related import SingleRelatedObjectDescriptor
        subclass_question_types = [a for a in dir(Question) if isinstance(getattr(Question, a), SingleRelatedObjectDescriptor)]
        for subclass_question_type in subclass_question_types:
            if hasattr(self, subclass_question_type):
                return getattr(self, subclass_question_type)
    
    def check_answer(self, *args, **kwargs):
        return self._get_subclass_question().check_answer(*args, **kwargs)

class QuestionCapture(Question):
    question_type = u"Capture d'écran"

    class Meta:
        verbose_name = u"Question capture d'écran"
        verbose_name_plural = u"Questions capture d'écran"

class QuestionChoixMultipleTexte(Question):
    question_type = u"QCM sur texte"

    class Meta:
        verbose_name = u"Question à choix multiple (texte)"
        verbose_name_plural = u"Questions à choix multiple (texte)"

class QuestionChoixMultipleImage(Question):
    question_type = u"QCM sur image"

    class Meta:
        verbose_name = u"Question à choix multiple (image)"
        verbose_name_plural = u"Questions à choix multiple (image)"
