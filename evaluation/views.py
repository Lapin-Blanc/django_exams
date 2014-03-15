# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404

from evaluation.models import Question

def QuestionDetailView(request, pk):
    # retourne la question qui a été effectivement créée (sous-classe de Question)
    question = get_object_or_404(Question, pk=pk)._get_subclass_question()
    return render(request, question.template_name, {'question' : question})