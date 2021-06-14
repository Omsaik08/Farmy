from django.db import models
from farmerApp import models as m1

class my_cities_tbl(models.Model):
	farmer_id = models.ForeignKey(m1.farmer_registration_tbl,on_delete=models.CASCADE) #userid
	cities = models.CharField(max_length=40)
	timestamp = models.CharField(max_length=20)