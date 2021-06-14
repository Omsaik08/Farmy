from django.urls import path
from . import views

urlpatterns = [
	path('homepage/',views.homepage,name="homepage"),
    path('homepage/<str:city_name>/',views.homepage,name="homepage"),
    path('my_cities/',views.my_cities,name="my_cities"),

    path('authority_homepage/',views.authority_homepage,name="authority_homepage"),
    path('authority_homepage/<str:city_name>/',views.authority_homepage,name="authority_homepage"),
    
]
