from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
	path('homepage/',views.index,name='homepage'),
	path('authority_homepage/',views.authority_homepage,name='authority_homepage'),
	path('bills/',views.showbills,name='bills'),
]
