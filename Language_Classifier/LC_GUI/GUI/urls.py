from django.urls import path

from . import views


app_name = 'GUI'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('doc/', views.doc, name='doc'),

]