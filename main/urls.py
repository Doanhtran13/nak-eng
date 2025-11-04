from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name = 'home'),
    path('login', views.loginPage, name = 'login'),
    path('register', views.register, name = 'register'),
    path('Adult_English', views.Aldult_English, name = 'Adult_English'), 
    path('Aldult_English1', views.Aldult_English1, name = 'Adult_English1'),
    path('Aldult_English2', views.Aldult_English2, name = 'Adult_English2'),
    path('Children_English', views.Children_English, name = 'Children_English'),
    path('Children_English1', views.Children_English1, name = 'Children_English1'),
    path('Children_English2', views.Children_English2, name = 'Children_English2'),
    path('ielts', views.ielts, name = 'ielts'),
    path('logout', views.logoutPage, name = 'logout'),
    path('unit1', views.unit1, name = 'unit1'),
    path('unit2', views.unit2, name = 'unit2'),
    path('unit3', views.unit3, name = 'unit3'),
    path('unit4', views.unit4, name = 'unit4'),
    path('unit5', views.unit5, name = 'unit5'),
    path('unit6', views.unit6, name = 'unit6'),
    path('unit7', views.unit7, name = 'unit7'), 
    path('unit8', views.unit8, name = 'unit8'),
    path('unit9', views.unit9, name = 'unit9'),
	# API endpoints
	path('api/test-result', views.api_test_result, name='api_test_result'),
	path('api/recommendation', views.api_recommendation, name='api_recommendation'),
    path('api/generate', views.api_generate, name='api_generate'),
]