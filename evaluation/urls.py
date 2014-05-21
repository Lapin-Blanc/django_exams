# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from evaluation import views

urlpatterns = patterns('',
    # Détail d'une question à partir du site d'administration
    url(r'^question/(?P<pk>\d+)/$', views.question_detail, name='question-detail'),
    url(r'^question/(?P<pk>\d+)/answer/$', views.answer_single_question, name='answer-single-question'),

    url(r'^$', views.exams_for_user, name='exams-list'),
    url(r'^(?P<exam_id>\d+)/$', views.exam_for_user, name='user-exam'),
    url(r'^(?P<exam_id>\d+)/(?P<question_id>\d+)/answer/$', views.answer_exam_question, name='answer-exam-question'),
)
