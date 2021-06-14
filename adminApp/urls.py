from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
	path('',views.homepage,name="homepage"),
	path('login/',views.login,name="login"),
	path('logout/',views.logout,name="logout"),
	path('issues/',views.issues,name="issues"),
	path('issues/<int:id>/',views.issues,name="issues"),
	path('farmer_connect/',views.farmer_connect,name="farmer_connect"),
	path('farmer_connect/<int:id>/',views.farmer_connect,name="farmer_connect"),
	path('add_feeds/',views.add_feeds,name="add_feeds"),
	path('remove_feeds/',views.remove_feeds,name="remove_feeds"),
	path('remove_feeds/<int:id>/',views.remove_feeds,name="remove_feeds"),
	path('add_videos/',views.add_videos,name="add_videos"),
	path('remove_videos/',views.remove_videos,name="remove_videos"),
	path('remove_videos/<int:id>/',views.remove_videos,name="remove_videos"),
]
