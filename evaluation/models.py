# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse

#####################################
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
# Une Question n'est jamais instanciée à partir d'ici, mais bien à partir de l'une des classes Django dérivées
# ci-après (héritage Django).
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

    # Méthode qui retourne la sous-classe Django qui a hérité de celle-ci et a servi à son instanciation
    def _get_subclass_question(self):
        from django.db.models.fields.related import SingleRelatedObjectDescriptor
        subclass_question_types = [a for a in dir(Question) if isinstance(getattr(Question, a), SingleRelatedObjectDescriptor)]
        for subclass_question_type in subclass_question_types:
            if hasattr(self, subclass_question_type):
                return getattr(self, subclass_question_type)
    
    # Vue du détail d'une Question à partir du site d'administration
    def get_absolute_url(self):
        return reverse("question-detail", args=[self.id])

    def check_answer(self, *args, **kwargs):
        return self._get_subclass_question().check_answer(*args, **kwargs)
    

# Question avec une capture d'écran où il faut indiquer sa réponse en déposant un curseur sur une image
# si le curseur est dans l'une des bonnes zones, alors la réponse est correcte
class QuestionCapture(Question):
    question_type = u"Capture"
    template_name = "evaluation/question_capture.html"

    # QuestionCapture specific attributes
    image = models.ImageField(upload_to="captures")
    
    def check_answer(self, answer):
        x = float(answer['x'][0])
        y = float(answer['y'][0])
        for z in self.zoneimage_set.all():
            if x>=z.x and x<=z.x+z.width and y>=z.y and y<=z.y+z.height:
                return 1.
        return 0.

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

# Questions à choix. Le chois peut-être multiple ou unique, et la question peut comporter ou non une image comme 
# support à la question.
QCM_ANSWER_TYPE_CHOICES = (
    ("M", "Choix multiples"),
    ("U", "Choix unique"),
)
class QuestionChoixMultiple(Question):
    question_type = u"QCM"
    template_name = "evaluation/question_qcm.html"

    # QuestionChoixMultiple specific attributes
    type_reponse = models.CharField("Type de réponse", max_length=1, choices=QCM_ANSWER_TYPE_CHOICES, default="U")
    image = models.ImageField(upload_to="captures", blank=True, null=True)

    class Meta:
        verbose_name = u"Question à choix multiple"
        verbose_name_plural = u"Questions à choix multiple"

    def check_answer(self, answer):
        choix = answer.get('choix', [])
        # Si il s'agit d'une réponse admettant plusieurs réponses
        if self.type_reponse == "M":
            points = 0
            total = self.choix_set.count()
            # Pour chacun des choix prévu comme réponse
            for choix_reponse in self.choix_set.all():
                # Si le choix est une bonne réponse
                if choix_reponse.correct:
                    # et qu'il a été coché comme réponse
                    if u"{}".format(choix_reponse.id) in choix:
                        # alors on ajoute un point
                        points = points +1
                # sinon, si le choix n'est pas une réponse correcte
                else:
                    # et qu'il n'a pas été coché comme réponse
                    if u"{}".format(choix_reponse.id) not in choix:
                        # alors on ajoute un point
                        points = points +1
            # on retourne la proportion de bonnes réponses...
            return float(points)/total    
        # Sinon, il s'agit d'une question n'admettant qu'une seule réponse                
        else:
            # Si pas de réponse donnée, on retourne 0
            if not choix:
                return 0.
            if choix[0] in [u"{}".format(c.id) for c in self.choix_set.all() if c.correct]:
                return 1.
            else:
                return 0.

class Choix(models.Model):
    libelle = models.CharField(max_length=200)
    correct = models.BooleanField(default=False)
    question = models.ForeignKey(QuestionChoixMultiple)
    
    def __unicode__(self):
        return self.libelle

#####################################
# Partie consacrées aux examens
#####################################

# Attribue automatiquement la prochaine position
def _get_next_position():
    lines = QuestionnaireLine.objects.all()
    if lines:
        return max([l.position for l in lines])+1
    else:
        return 1

class Questionnaire(models.Model):
    libelle = models.CharField(max_length=20,help_text="Nom descriptif du questionnaire")
    duree = models.IntegerField("Durée",help_text="Exprimée en minutes", default=30)
    niveau = models.IntegerField(choices=NIVEAU_CHOICES, default=3)
    categorie = models.ForeignKey(QuestionCategory, verbose_name="catégorie")
    
    def __unicode__(self):
        return self.libelle

class QuestionnaireLine(models.Model):
    questionnaire = models.ForeignKey(Questionnaire)
    position = models.IntegerField(null=True, blank=True)
    question = models.ForeignKey(Question)
    ponderation = models.IntegerField("Pondération", default=1)
    
    def save(self, *args, **kwargs):
        if not self.position:
            lines_pos = [l.position for l in self.questionnaire.questionnaireline_set.all()]
            if lines_pos:
                self.position = max(lines_pos)+1
            else:
                self.position = 1
        return super(QuestionnaireLine, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return u"{0:>2} - {1}".format(self.position, self.question)
    
    class Meta:
        ordering = ['position',]
