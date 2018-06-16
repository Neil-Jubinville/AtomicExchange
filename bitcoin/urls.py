# Author:  Neil Jubinville
# App Microservices and Dashboard to interface bitcoin

from django.conf.urls import  url
from django.views.generic import TemplateView
from views import ListsinceblockView

urlpatterns = [

        url(r'^rpc/listsinceblock', ListsinceblockView.as_view()),

    ]