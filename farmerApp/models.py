from django.db import models
import datetime
import os

# Create your models here.

def path_and_rename(instance,filename):
	upload_to = 'images/'+'farmer/'+'registrations/'+instance.mobile_no+"/"
	ext = filename.split('.')[-1]  #demo.jpg we get "jpg"
	image_name = instance.mobile_no +'.'+ext
	return os.path.join(upload_to,image_name)

def ask_query_path_and_rename1(instance,filename):
	imgname= (datetime.datetime.now()).strftime("%d-%m-%YT%H%M%S")
	farmer_id=str(instance.farmer_id)[-2]
	upload_to = 'images/farmer/questions/'+farmer_id+"/"
	ext = filename.split('.')[-1]
	image_name = "01"+imgname+"."+ext
	return os.path.join(upload_to,image_name)

def ask_query_path_and_rename2(instance,filename):
	imgname= (datetime.datetime.now()).strftime("%d-%m-%YT%H%M%S")
	farmer_id=str(instance.farmer_id)[-2]
	upload_to = 'images/farmer/questions/'+farmer_id+"/"
	ext = filename.split('.')[-1]
	image_name = "02"+imgname+"."+ext
	return os.path.join(upload_to,image_name)

class farmer_registration_tbl(models.Model):
	profile_photo = models.ImageField(null=True,blank=True,upload_to=path_and_rename)
	first_name = models.CharField(max_length=20)
	last_name = models.CharField(max_length=20)
	email = models.CharField(max_length=40,unique=True)	# verify at html and verify using OTP
	password = models.CharField(max_length=16)	# use cipher text , restrict minlen=8 at html side
	mobile_no = models.CharField(max_length=10,unique=True) # verify at html
	address = models.CharField(max_length=100)	# houseNo,streetName,city,state,India
	dob = models.CharField(max_length=10) # verify at html	01/12/2000
	gender = models.CharField(max_length=10) # male or female or NA(prefer not to say)
	account_status = models.CharField(max_length=10,default='active')
	timestamp = models.CharField(max_length=20) # 2021-02-16 17:06:12.573181



class questions_tbl(models.Model):
	farmer_id = models.ForeignKey(farmer_registration_tbl,on_delete=models.CASCADE)
	title = models.CharField(max_length=50)
	question = models.CharField(max_length=400)
	image1 = models.ImageField(null=True,blank=True,upload_to=ask_query_path_and_rename1)
	image2 = models.ImageField(null=True,blank=True,upload_to=ask_query_path_and_rename2)
	tags = models.CharField(max_length=50)	# apple,disease,pesticides
	timestamp = models.CharField(max_length=20) # 2021-02-16 17:06:12.573181
	status = models.CharField(max_length=15,default="not answered")


class comments_tbl(models.Model):
	question_id = models.ForeignKey(questions_tbl,on_delete=models.CASCADE)
	farmer_id = models.ForeignKey(farmer_registration_tbl,on_delete=models.CASCADE)
	comment = models.CharField(max_length=400)
	timestamp = models.CharField(max_length=20) # 2021-02-16 17:06:12.573181
	likes = models.PositiveSmallIntegerField(default=0)
	dislikes = models.PositiveSmallIntegerField(default=0)


class history_of_searched_questions_tbl(models.Model):
	farmer_id = models.ForeignKey(farmer_registration_tbl,on_delete=models.CASCADE)
	question_id = models.ForeignKey(questions_tbl,on_delete=models.CASCADE)



class contact_us_tbl(models.Model):
	farmer_name = models.CharField(max_length=50)
	farmer_email = models.CharField(max_length=50)
	subject = models.CharField(max_length=100)
	message = models.CharField(max_length=400)
	status = models.CharField(max_length=10,default="Unsolved")