# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from evaluation import views

urlpatterns = patterns('',
    # Détail d'une question à partir du site d'administration
    url(r'^question/(?P<pk>\d+)/$', views.QuestionDetailView, name='question-detail'),
)
