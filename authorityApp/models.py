from django.db import models
import datetime
from farmerApp import models as m1
import os

# Create your models here.
def path_and_rename(instance,filename):
	upload_to = 'images/'+'officer/'+'registrations/'+instance.mobile_no+"/"
	ext = filename.split('.')[-1]  #demo.jpg we get "jpg"
	image_name = instance.mobile_no+'.'+ext
	return os.path.join(upload_to,image_name)

def temporary_image(instance,filename):
	upload_to="Email/"
	ext=filename.split(".")[-1]
	filename="authority_id"+"_issue"+"."+ext
	return os.path.join(upload_to,filename)

def bill_rename(instance,filename):
	imgname= str(instance.bill_uploading_date)
	upload_to = "Bills/" + str(instance.authority_id_id)  +"/" #change with session
	ext = filename.split(".")[-1]
	filename = imgname + "." +ext
	return os.path.join(upload_to,filename)

class officer_registration_tbl(models.Model):
	profile_photo = models.ImageField(null=True,blank=True,upload_to=path_and_rename)
	full_name = models.CharField(max_length=40)
	email = models.CharField(max_length=40,unique=True)	# verify at html and verify using OTP
	password = models.CharField(max_length=16)	# use cipher text , restrict minlen=8 at html side
	mobile_no = models.CharField(max_length=10,unique=True) # verify at html
	address = models.CharField(max_length=100)	# houseNo,streetName,city,state,India
	dob = models.CharField(max_length=10) # verify at html	01/12/2000
	gender = models.CharField(max_length=10) # male or female or NA(prefer not to say)
	timestamp =models.CharField(max_length=20) # 2021-02-16 17:06:12.573181
	account_status = models.CharField(max_length=10,default='active')


class answer_tbl(models.Model):
	question_id = models.ForeignKey(m1.questions_tbl,on_delete=models.CASCADE)
	authority_id = models.ForeignKey(officer_registration_tbl,on_delete=models.CASCADE)
	answer = models.CharField(max_length=400)
	timestamp = models.CharField(max_length=20) # 2021-02-16 17:06:12.573181
	likes = models.PositiveSmallIntegerField(default=0)
	dislikes = models.PositiveSmallIntegerField(default=0)

class amendment_bill_tbl(models.Model):
	authority_id = models.ForeignKey(officer_registration_tbl,on_delete=models.CASCADE)
	bill_issued_date = models.CharField(max_length=15)
	bill_uploading_date = models.CharField(max_length=20)
	issued_by = models.CharField(max_length=50)
	bill = models.FileField(null=False,upload_to=bill_rename)
	subject = models.CharField(max_length=100)
	description = models.CharField(max_length=400)

class send_email_with_image(models.Model):
	message=models.CharField(max_length=100)
	image=models.ImageField(null=True,blank=True,upload_to=temporary_image)
	status=models.CharField(max_length=10,default='Unsolved')