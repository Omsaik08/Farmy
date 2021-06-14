from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.guestLogin,name="guestLogin"),
	path('register/',views.register,name="register"),
	path('login',views.login,name="login"),
	path('logout/',views.logout,name="logout"),
	path('forgot/',views.forgot,name="forgot"),
	path('farmer_otp/',views.farmer_otp,name="farmer_otp"),
	path('change_password/',views.change_password,name="change_password"),
	path('homepage/',views.homepage,name="homepage"),
	path('give_reply/',views.give_reply,name="give_reply"),
	path('about/',views.about,name="about"),
	path('ask_query/',views.ask_query,name="ask_query"),
	path('contact/',views.contact,name="contact"),
	path('faq/',views.faq,name="faq"),
	path('privacy_policy/',views.privacy_policy,name="privacy_policy"),
	path('terms_conditions/',views.terms_conditions,name="terms_conditions"),
	path('my_profile/',views.my_profile,name="my_profile"),
	path('videos/',views.videos,name="videos"),
	path('delete_account/',views.delete_account,name="delete_account"),
	path('update_profile/',views.update_profile,name="update_profile"),
	path('videos/',views.videos,name="videos"),
	path('my_questions/',views.my_questions,name="my_questions"),
	path('show_question/<int:qid>/',views.show_question,name="show_question"),
	path('all_questions/',views.all_questions,name="all_questions"),
	path('delete_question/<int:qid>/',views.delete_question,name="delete_question"),
	path('darkModeChange/',views.darkModeChange,name="darkModeChange"),
]
