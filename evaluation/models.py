# -*- coding: utf-8 -*-
from django.db import models

# Partie consacrées aux questions
#####################################

# Catégories de question
class QuestionCategory(models.Model):
    nom = models.CharField(max_length=30)

    def __unicode__(self):
        return self.nom

    class Meta:
        verbose_name = u"Catégorie de question"
        verbose_name_plural = u"Catégories de question"
        ordering = ['nom',]

# Attribue automatiquement un numéro aux questions
def _get_next_question_num():
    questions = Question.objects.all()
    if questions:
        return max([q.numero for q in questions])+1
    else:
        return 1

# Niveau de difficulté des questions
NIVEAU_CHOICES = (
    (1, u'Très facile'),
    (2, u'Facile'),
    (3, u'Normal'),
    (4, u'Difficile'),
    (5, u'Très difficile'),
)

# Classe Question principale
# Les autres classes de question héritent de celle-ci, et doivent implémenter les méthodes check_answer
# 
class Question(models.Model):

    numero = models.IntegerField("numéro", help_text=u"Le numéro de référence de la question", unique=True, default=_get_next_question_num)
    description = models.CharField(max_length=100, default=u"Description courte de la question", help_text=u"Description identifiant la question")
    intitule = models.TextField("intitulé", default=u"Entrez le texte de la question ici...", help_text=u"Les balises HTML sont accept&eacute;es")
    niveau = models.IntegerField(choices=NIVEAU_CHOICES, default=3)
    categorie = models.ForeignKey(QuestionCategory, verbose_name="catégorie")
    
    def __unicode__(self):
        question_type = getattr(self._get_subclass_question(),"question_type","")
        return u"{0:>04} [{1:<15}]: {2}".format(self.numero, question_type, self.description)

    class Meta:
        ordering = ["numero",]

    def _get_subclass_question(self):
        from django.db.models.fields.related import SingleRelatedObjectDescriptor
        subclass_question_types = [a for a in dir(Question) if isinstance(getattr(Question, a), SingleRelatedObjectDescriptor)]
        for subclass_question_type in subclass_question_types:
            if hasattr(self, subclass_question_type):
                return getattr(self, subclass_question_type)
    
    def check_answer(self, *args, **kwargs):
        return self._get_subclass_question().check_answer(*args, **kwargs)

# Question avec une capture d'écran où il faut indiquer sa réponse en déposant un curseur sur une image
# si le curseur est dans l'une des bonnes zones, alors la réponse est correcte
class QuestionCapture(Question):
    question_type = u"Capture d'écran"
    template = "questions/question_capture.html"

    # Capture specific attributes
    image = models.ImageField(upload_to="captures")
    
    def check_answer(self, x, y):
        x = int(x[0])
        y = int(y[0])
        for z in self.zoneimage_set.all():
            if x>=z.x and x<=z.x+z.width and y>=z.y and y<=z.y+z.height:
                return True
        return False

    class Meta:
        verbose_name = u"Question capture d'écran"
        verbose_name_plural = u"Questions capture d'écran"

# Les zone de l'image qui sont considérées comme de bonnes réponses
class ZoneImage(models.Model):
    x = models.IntegerField("Abscisse")
    y = models.IntegerField("Ordonnée")
    width = models.IntegerField("Largeur")
    height = models.IntegerField("Hauteur")
    question = models.ForeignKey(QuestionCapture)
    
    def __unicode__(self):
        return u"{0}, {1}, {2}, {3}".format(self.x, self.y, self.width, self.height)

    class Meta:
        verbose_name = u"Zone de réponse"
        verbose_name_plural = u"Zones de réponse"





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
