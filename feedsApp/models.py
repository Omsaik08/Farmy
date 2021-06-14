from django.db import models
import datetime

def check():
	time= (datetime.datetime.now()).strftime("%Y-%m-%d")
	return time
# Create your models here.
class Feed(models.Model):
	title=models.CharField(max_length=100)
	link=models.CharField(max_length=50)
	date=models.CharField(max_length=15)
	source=models.CharField(max_length=50)
	thumbnail=models.CharField(max_length=15000)
	description=models.CharField(max_length=200)
	uploading_date=models.CharField(max_length=20,default=check)
