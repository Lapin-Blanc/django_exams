# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from evaluation import views

urlpatterns = patterns('',
    # Détail d'une question à partir du site d'administration
    url(r'^question/(?P<pk>\d+)/$', views.question_detail, name='question-detail'),
    url(r'^question/(?P<pk>\d+)/answer/$', views.answer_single_question, name='answer-single-question'),
)
