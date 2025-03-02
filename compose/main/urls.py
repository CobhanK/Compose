#main/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('record', views.record, name='record'),
    path('upload-wav', views.upload_wav, name='upload_wav'),
]