from django.urls import path
from . import views


urlpatterns = [
    path('', views.about, name='about'),
    path('experience/', views.experience_view, name='experience'),
    path('projects/', views.projects_view, name='projects'),
    path('contact/', views.contact_view, name='contact'),
]

#agregar en el navegador sin el html