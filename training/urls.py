
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/',views.dashboard, name ='dashboard'),
    path('register/',views.register, name ='register'),
    path('login/',views.user_login, name ='login'),
    path('adminDash/', views.adminDash, name = 'adminDash'),
    path('createTask/', views.createTask, name = 'createTask'),
    path('viewTask/', views.viewTask, name = 'viewTask'),
    path('submission/', views.submission, name = 'submission'),
    path('mainView/', views.mainView, name = 'mainView'),
    path('feedback/', views.feedback, name = 'feedback')
   
   
]
   # path('adminDash/createTask/', views.createTask, name = 'createTask'),
   # path('adminDash/viewTask/', views.viewTask, name = 'viewTask'),
   # path('dashboard/submission/', views.submission, name = 'submission')