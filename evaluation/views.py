# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.template import RequestContext, loader
from evaluation.models import Question, Examen, ExamenLine

@staff_member_required
def question_detail(request, pk):
    # retourne la question qui a été effectivement créée (sous-classe de Question)
    question = get_object_or_404(Question, pk=pk)._get_subclass_question()
    return render(request, question.template_name, {'question' : question, 'single_question' : True})

@staff_member_required
def answer_single_question(request, pk):
    question = get_object_or_404(Question, pk=pk)._get_subclass_question()
    answer = dict(request.POST)
    # la réponse ne doit pas contenir autre chose que le(s) champ(s) de réponse pour
    # être corrigée -> on retire le token de sécurité
    answer.pop('csrfmiddlewaretoken')
    result = question.check_answer(answer=answer)
    message= u"Réponse correcte à {:.2f} %".format(result*100)
    messages.add_message(request, messages.INFO, message)
    return HttpResponseRedirect(reverse('question-detail', args=[question.id,]))

@login_required
def exams_for_user(request):
    utilisateur = request.user
    return render(request, "examens/liste_examens.html", {"exams_list":request.user.examen_set.all()})

@login_required
def exam_for_user(request, exam_id):
    exam = get_object_or_404(Examen, id=exam_id, utilisateur=request.user)
    if not exam.debut:
        exam.debut = timezone.now()
    exam.save()
    unanswered_questions = exam.examenline_set.filter(repondu=False)
    elapsed = (timezone.now()-exam.debut).seconds
    if unanswered_questions and elapsed < (exam.questionnaire.duree * 60):
        next_question = unanswered_questions[0]
        q_questionnaire = next_question.question_line
        q_position = q_questionnaire.position
        q = next_question.question_line.question._get_subclass_question()
        template = loader.get_template(q.template_name)
        context = RequestContext(request, {
            'question_line': next_question,
            'question':q,
            'questionnaire' : exam,
            'position' : q_position,
        })
        return render(request, "examens/examen.html", { "exam":exam, 
                                                        "question":q,
                                                        "elapsed":elapsed,
                                                        "total":exam.questionnaire.duree * 60,
                                                        #"question_html":q_questionnaire.question.render_to_html(q_position=q_position, answer_url="/test/%s/%s/answer/" % (exam_id, next_question.id)),
                                                        "question_html": template.render(context),
                                                        })
    else:
        #Examen terminé ou bien sans questions à gérer
        from django.db.models import Sum
        if not exam.fin:
            exam.fin = timezone.now()
        exam.resultat = exam.examenline_set.aggregate(Sum('resultat'))['resultat__sum']
        total = exam.questionnaire.questionnaireline_set.aggregate(Sum('ponderation'))['ponderation__sum']
        exam.save()
        return HttpResponse("""
        <h1>Test terminé</h1>
        <h2>R&eacute;sultat:&nbsp;%0d/%s</h2>
        <a href="%s">Retour aux tests...</a>
        """ % (round(exam.resultat,0),total, reverse('exams-list')))


@login_required
def answer_exam_question(request, exam_id, question_id):
    exam_question = get_object_or_404(ExamenLine, id=question_id, examen=exam_id, examen__utilisateur=request.user)
    answer = dict(request.POST)
    answer.pop('csrfmiddlewaretoken')
    exam_question.repondu = True
    exam_question.resultat = exam_question.question_line.ponderation * exam_question.question_line.question.check_answer(**answer)
    exam_question.save()

    return HttpResponseRedirect(reverse('user-exam', args=[exam_id,]))


