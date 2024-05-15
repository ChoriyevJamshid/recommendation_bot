from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('parse/', views.parser)
]

