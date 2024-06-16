from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('casosBorde/', views.casosBorde, name='casosBorde'),
    path('masTransacciones/', views.masTransacciones, name='masTransacciones'),
    path('masRecurrentes/', views.masRecurrentes, name='masRecurrentes'),
    path('top10/', views.top10, name='top10'),
    path('masTranRecu/', views.masTranRecu, name='masTranRecu'),
]