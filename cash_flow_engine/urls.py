from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('table/', views.table, name="table"),
    path('exportportfolio/', views.exportportfolio, name='exportportfolio'),
    path('table/individualcf/<int:pk>/', views.individualcf, name='individualcf'),
    path('export/individualcf/<int:pk>/', views.exportindividualcf, name='exportindividualcf'),
    path('loanupload/', views.loanupload, name="loanupload"),
    path('loanupload/<int:pk>/', views.delete_file, name='delete_file'),
    path('documentation/', views.documentation, name="documentation"),


]