from django import forms
from .models import *

class my_cities_tbl_form(forms.ModelForm):
	class Meta:
		model = my_cities_tbl
		fields = ['cities','timestamp','farmer_id']