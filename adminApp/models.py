from django.db import models
import datetime


class admin_registration_tbl(models.Model):
	username=models.CharField(max_length=100)
	password=models.CharField(max_length=100)
	status=models.CharField(max_length=100,default="active")

class admin_yt_videos_tbl(models.Model):
	title=models.CharField(max_length=100)
	link=models.CharField(max_length=500)
	uploading_date=models.CharField(max_length=35)
