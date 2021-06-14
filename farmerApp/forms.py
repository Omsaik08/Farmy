from django import forms 
from .models import *
  
class farmer_registration_tbl_form(forms.ModelForm): 
    class Meta: 
        model = farmer_registration_tbl
        fields = ['profile_photo','first_name','last_name','email','password','mobile_no','address','dob','gender','account_status','timestamp'] 


class questions_tbl_form(forms.ModelForm): 
    class Meta: 
        model = questions_tbl
        fields = ['farmer_id','title','question','image1','image2','tags','timestamp','status'] 


class comments_tbl_form(forms.ModelForm):
	class Meta:
		model = comments_tbl
		fields = ['question_id','farmer_id','comment','timestamp','likes','dislikes']

class history_of_searched_questions_tbl_form(forms.ModelForm):
	class Meta:
		model = history_of_searched_questions_tbl
		fields = ['farmer_id','question_id']