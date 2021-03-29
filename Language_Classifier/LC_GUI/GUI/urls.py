from django.urls import path

from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'GUI'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('doc/', views.doc, name='doc'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)