#compose/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.editor, name='editor'),
    path('new', views.editor, name='new'),
]