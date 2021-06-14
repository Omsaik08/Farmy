from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
	path('homepage/',views.homepage,name="homepage"),
	path('register/',views.register,name="register"),
	path('login/',views.login,name="login"),
	path('logout/',views.logout,name="logout"),
	path('forgot/',views.forgot,name="forgot"),
	path('authority_otp/',views.authority_otp,name="authority_otp"),
	path('change_password/',views.change_password,name="change_password"),
	path('add_bills/',views.add_bills,name="add"),	
	path('show_bills/',views.show_bills,name="show_bills"),
	path('delete_bills/<int:bill_id>/',views.delete_bills,name="delete_bills"),
	path('my_profile/',views.my_profile,name="my_profile"),
	path('update_profile/',views.update_profile,name="update_profile"),
	path('change_password/',views.change_password,name="change_password"),
	path('delete_account/',views.delete_account,name="delete_account"),
	path('contact_admin/',views.contact_admin,name="contact_admin"),
	path('about/',views.about,name="about"),
	path('all_questions/',views.all_questions,name="all_questions"),
	path('show_question/<int:qid>',views.show_question,name="show_question"),
	path('pending_questions',views.pending_questions,name="pending_questions"),
	path('genrate_report',views.genrate_report,name='genrate_report'),
	path('filterQuestions',views.filterQuestions,name='filterQuestions'),
	path('darkModeChange/',views.darkModeChange,name="darkModeChange"),	
	path('faq/',views.faq,name="faq"),
	path('terms_and_conditions/',views.terms_and_conditions,name="terms_and_conditions"),
	path('privacy_policy/',views.privacy_policy,name="privacy_policy"),
]
