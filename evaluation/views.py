﻿# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from evaluation.models import Question

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