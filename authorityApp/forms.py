from django import forms 
from .models import *

class officer_registration_tbl_form(forms.ModelForm): 
    class Meta: 
        model = officer_registration_tbl
        fields = ['profile_photo','full_name','email','password','mobile_no','address','dob','gender','timestamp','account_status'] 

class emailForm(forms.ModelForm):

	class Meta:
		model = send_email_with_image
		fields = ['message','image'] 
 
class officer_bill_tbl_form(forms.ModelForm):

	class Meta:
		model = amendment_bill_tbl		
		fields = ['authority_id','bill_issued_date','bill_uploading_date','issued_by','bill','subject','description']


class answer_tbl_form(forms.ModelForm):
	class Meta:
		model = answer_tbl
		fields = ['question_id','authority_id','answer','timestamp','likes','dislikes']
