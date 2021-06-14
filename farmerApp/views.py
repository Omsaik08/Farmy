from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
import farmyBot as fb
from .forms import *
from .models import *
from weatherApp.models import *
from weatherApp.forms import *
from feedsApp import views as v
from feedsApp import models as m1
import string
from nltk.corpus import stopwords
import re
from . import forms
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import smtplib
gmailaddress = "bizzfarmy@gmail.com"
gmailpassword = "bizzfarmy@321"
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import random
from django.http import JsonResponse



from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pickle
import numpy as np



# Create your views here.


with open(r"toxic_vect.pkl", "rb") as f:
    tox = pickle.load(f)

with open(r"insult_vect.pkl", "rb") as f:
    ins = pickle.load(f)

with open(r"toxic_model.pkl", "rb") as f:
    tox_model = pickle.load(f)

with open(r"insult_model.pkl", "rb") as f:
    ins_model  = pickle.load(f)

imgtype = ['png','jpg','jpeg']


def guestLogin(request):
    res="Hello there! Need help? Reach out to us right here, and we'll get back to you as soon as we can!"
    if( 'msg' not in request.session  ):
        request.session['msg']=res
    return render(request,'farmer/guest.html')

def register(request):
	if( request.method == 'POST' ):

		try:
			ext = request.FILES['profile_photo'].name
			ext = ext.lower()
			ext = ext.split('.')[-1]
			if( ext not in imgtype ):
				return render(request,'farmer/login.html',{'errors':['fileType']})

		except:
			pass




		form = farmer_registration_tbl_form(request.POST,request.FILES)
		if( form.is_valid() ):
			form.save()


			try:
				t = farmer_registration_tbl.objects.get(timestamp=request.POST['timestamp'])
			except:
				pass
			data = {
			'cities':request.POST['city'] ,
			'timestamp':request.POST['timestamp'],
			'user':'farmer',
			'farmer_id':t.id

			}
			add_weather = my_cities_tbl_form(data)
			add_weather.save()

		else:
			return render(request,'farmer/login.html',{'errors':form.errors})
			#return render(request,'farmer/login.html',{'status':0})
		return render(request,'farmer/login.html')

	else:
		return render(request,'farmer/register.html')


def login(request):
    username=request.GET.get("username",None)
    password=request.GET.get("password",None)
    if username==None and password==None:
        return render(request,'farmer/login.html')
    if( '@' in username ):# for username as email
        try:
            result = farmer_registration_tbl.objects.get(email=username)
        except:
            data={
                'status':0,
            }
            return JsonResponse(data)
        if( result.account_status == "deactive" ):
            data={
                'status':2,
            }
            return JsonResponse(data)
    else:
        try:
            result = farmer_registration_tbl.objects.get(mobile_no=username)
        except:# means no Mobile no. exists
            data={
                'status':0,
            }
            return JsonResponse(data)
        if( result.account_status == "deactive" ):
            data={
                'status':2,
            }
            return JsonResponse(data)

    if( password == result.password ):
        request.session['farmer_id']=result.id
        request.session['darkMode'] = False
        data={
            'status':1,
        }
        return JsonResponse(data)
    else:
        data={
            'status':3,
            }
        return JsonResponse(data)
        """if( request.method == 'POST' ):
		#return HttpResponse(request.POST.items())
		if( '@' in request.POST['username'] ):# for username as email
			try:
				data = farmer_registration_tbl.objects.get(email=request.POST['username'])
			except:
				return render(request,'farmer/login.html',{'errors':['Not registered']})
			if( data.account_status == "deactive" ):
				return render(request,'farmer/login.html',{'errors':['blocked']})


		else: # for username as mobile
			try:
				data = farmer_registration_tbl.objects.get(mobile_no=request.POST['username'])
			except:# means no Mobile no. exists
				return render(request,'farmer/login.html',{'errors':['Not registered']})
			if( data.account_status == "deactive" ):
				return render(request,'farmer/login.html',{'errors':['blocked']})

		if( request.POST['password'] == data.password ):
			request.session['farmer_id']=data.id

			request.session['darkMode'] = False
			return redirect('farmerApp:homepage')
		else:
			return render(request,'farmer/login.html',{'errors':['Password is Incorrect']})
	else:
		return render(request,'farmer/login.html')
	"""

def forgot(request):
	if( request.method == 'POST' ):
		send_otp_to=str(request.POST['username'])
		cursor = connection.cursor()
		cursor.execute("select email from farmerApp_farmer_registration_tbl");
		data = cursor.fetchall();
		cursor.close()
		OTP=0
		f=0
		#return HttpResponse(data)
		for i in data:
			if i[0]==send_otp_to:
				OTP=random.randint(1000,9999)
				message = """\
From:"""+gmailaddress+"""
To:"""+send_otp_to+"""
Subject: Farmy-Password Change

Dear Farmer,\n\nYour OTP for Change of Password is: """+str(OTP)+""".\n\nThanks and Regards,\nTeam FARMY."""
				mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
				mailServer.starttls()
				mailServer.login(gmailaddress , gmailpassword)
				mailServer.sendmail(gmailaddress, send_otp_to , message)
				mailServer.quit()
				f=1
				break
		if f:
			return render(request,'farmer/farmer_otp.html',{'username':request.POST['username'],'OTP':OTP,'status':'found'})
		else:
			return render(request,'farmer/farmer_otp.html',{'status':'not found'})
	else:
		return render(request,'farmer/forgot.html')



def farmer_otp(request):# forgot password
	if request.method=='POST':
		if request.POST['otp']==request.POST['main_otp']:
			return render(request,'farmer/change_password.html',{'username':request.POST['username']})
		else:
			return render(request,'farmer/farmer_otp.html',{'username':request.POST['username'],'status':'invalid'})
	return redirect('farmerApp:forgot')

def change_password(request):
	if request.method=='POST':
		new_pass=request.POST['password']
		cursor = connection.cursor()
		cursor.execute("update farmerApp_farmer_registration_tbl set password=%s where email=%s",[new_pass,request.POST['username']])
		cursor.close()
		return render(request,'farmer/login.html')
	return redirect('farmerApp:forgot')



def homepage(request):
	if( 'farmer_id' in request.session):
		feeds_data = m1.Feed.objects.filter().order_by('id')[:2]



		cursor = connection.cursor()
		cursor.execute("select q.id,q.title,q.question,q.image1,q.image2,q.timestamp,r.first_name,r.last_name from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id limit 2")
		questions_data = cursor.fetchall()

		if( len(questions_data) == 0  ):
			questions_data=0

		#chatbot
		res="Hello there! Need help? Reach out to us right here, and we'll get back to you as soon as we can!"

		if( 'msg' not in request.session ):
			request.session['msg']=res

		#


		cursor.execute("select * from adminApp_admin_yt_videos_tbl limit 0,2")
		vdata=cursor.fetchall()

		if len(vdata)==0:
			vdata=""

		cursor.close()

		return render(request,'farmer/homepage.html',{'feeds_data':feeds_data,'questions_data':questions_data,'vdata':vdata})

	else:
		return redirect('farmerApp:login')

def give_reply(request):
    try:
        impdata={}
        userMsg=request.GET.get("userMsg",None)


        rp=fb.my_bot.get_response(userMsg.lower())


        data = [userMsg.lower()]
        vect = tox.transform(data)
        pred_tox = tox_model.predict_proba(vect)[:,1]
        vect = ins.transform(data)
        pred_ins = ins_model.predict_proba(vect)[:,1]
        out_tox = round(pred_tox[0], 2)
        out_ins = round(pred_ins[0], 2)

        if 'hello' in userMsg and out_tox==0.82:
            rp="hello,how are you?"
        elif out_tox>=0.70:
            rp="Your comment is found toxic,Please use proper wording."
        elif out_ins>=0.70:
            rp="Your comment is found Insulting,Please use proper wording."

        impdata["reply"]=str(rp)
        impdata["status"]=1

        prev=request.session['msg']
        request.session['msg']= str(prev) + "^" + str(userMsg) + "^" +str(rp)


        if( rp == 'hello'):
            rp='Sorry,I am unable to get you!'
            impdata["status"]=0
            impdata["reply"]=str(rp)
        if len(userMsg)== userMsg.count(" "):
            rp='Sorry,I am unable to get you!'
            impdata["status"]=0
            impdata["reply"]=str(rp)

        return JsonResponse(impdata)
    except:
        impdata={}
        impdata["reply"]='Sorry,I am unable to get you!'
        impdata["status"]=0
        return JsonResponse(impdata)
        """if request.method=='POST':
		rq=request.POST['userMsg']

		rp=fb.my_bot.get_response( request.POST['userMsg'].lower() )

		if( rp == 'hello' ):
			rp='Sorry,I am unable to get you!'

		if len(rq)== rq.count(" "):
			rp='Sorry,I am unable to get you!'

		prev=request.session['msg']


		request.session['msg']= str(prev) + "^" + str(rq) + "^" +str(rp)


		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		res="Hello there! Need help? Reach out to us right here, and we'll get back to you as soon as we can!"
		request.session['msg']=res
		return render(request,'farmer/homepage.html')"""

def about(request):
    res="Hello there! Need help? Reach out to us right here, and we'll get back to you as soon as we can!"
    if( 'msg' not in request.session  ):
        request.session['msg']=res
    return render(request,'farmer/about.html')



def ask_query(request):
	if( 'farmer_id' in request.session):
		if request.method=='POST':

		    data = [request.POST.get("title","")]
		    vect = tox.transform(data)
		    pred_tox = tox_model.predict_proba(vect)[:,1]
		    vect = ins.transform(data)
		    pred_ins = ins_model.predict_proba(vect)[:,1]
		    out_tox = round(pred_tox[0], 2)
		    out_ins = round(pred_ins[0], 2)
		    if out_tox>=0.70:
		        return render(request,'farmer/ask_query.html',{"toxic_status":"toxic"})
		    if out_ins>=0.70:
		        return render(request,'farmer/ask_query.html',{"toxic_status":"insult"})

		    data = [request.POST.get("question","")]
		    vect = tox.transform(data)
		    pred_tox = tox_model.predict_proba(vect)[:,1]
		    vect = ins.transform(data)
		    pred_ins = ins_model.predict_proba(vect)[:,1]
		    out_tox = round(pred_tox[0], 2)
		    out_ins = round(pred_ins[0], 2)
		    if out_tox>=0.70:
		        return render(request,'farmer/ask_query.html',{"toxic_status":"toxic"})
		    if out_ins>=0.70:
		        return render(request,'farmer/ask_query.html',{"toxic_status":"insult"})

		    try:
		        ext = request.FILES['profile_photo'].name
		        ext = ext.split('.')[-1]
		        ext1 = request.FILES['profile_photo'].name
		        ext1 = ext1.split('.')[-1]
		        if( ext not in imgtype or ext1 not in imgtype ):
		            return render(request,'farmer/homepage.html',{'errors':['fileType']})
		    except:
		        pass
		    title=request.POST.get("title","")
		    title=title.lower()
		    cleaned_data=title.translate(str.maketrans('','',string.punctuation))
		    words=cleaned_data.split()
		    stop_words = set(stopwords.words('english'))
		    final_words=[]
		    for word in words:
		        if word not in stop_words:
		            final_words.append(word)
		            description=request.POST.get("question","")
		    r=','.join(final_words)
		    i1=""
		    i2=""
		    if(request.FILES.get('image1','')):
		        i1=request.FILES['image1'].name
		    if(request.FILES.get('image2','')):
		        i2=request.FILES['image2'].name
		    data ={
				'farmer_id':request.POST['farmer_id'],
				'title':request.POST['title'],
				'question':request.POST['question'],
				'image1':i1,
				'image2':i2,
				'tags':r,
				'timestamp':request.POST['timestamp'],
				'status':request.POST['status']
				}

		    form = forms.questions_tbl_form(data,request.FILES)
		    if( form.is_valid() ):
		        form.save()
		        return redirect('farmerApp:my_questions') # go to my questions.html
		    else:
		        return redirect('farmerApp:homepage')
		else:
		    return render(request,'farmer/ask_query.html')
	else:
	    return redirect('farmerApp:login')


def contact(request):
	if request.method=='POST':
		name=request.POST.get("farmer_name", "")
		mail=request.POST.get("farmer_email","")
		subject=request.POST.get("email_subject","")
		from_message=request.POST.get("message","")

		obj=contact_us_tbl(farmer_name=name,farmer_email=mail,subject=subject,message=from_message)
		obj.save()

		#store this in db


		message = """\
From:"""+gmailaddress+"""
To:"""+mail+"""
Subject: Farmy

Dear """+str(name)+""",\n\nWe have sucessfully received your message, Our team will connect with you soon!\nHappy Farming. \n\nThanks and Regards,\nTeam FARMY."""
		mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
		mailServer.starttls()
		mailServer.login(gmailaddress , gmailpassword)
		mailServer.sendmail(gmailaddress, mail , message)
		#print(" \n Sent!")
		mailServer.quit()
		return redirect('farmerApp:homepage')
	else:
	    res="Hello there! Need help? Reach out to us right here, and we'll get back to you as soon as we can!"
	    if ('msg' not in request.session):
	        request.session['msg']=res
	    return render(request,'farmer/contact.html')

def faq(request):
	return render(request,'farmer/faq.html')

def privacy_policy(request):
	return render(request,'farmer/privacy_policy.html')

def terms_conditions(request):
	return render(request,'farmer/terms_conditions.html')

def my_profile(request):
	if( 'farmer_id' in request.session):
		data = farmer_registration_tbl.objects.filter(id=request.session['farmer_id'])
		return render(request,'farmer/my_profile.html',{'data':data})
	else:
		return redirect('farmerApp:login')

def update_profile(request):
	if( 'farmer_id' in request.session):
		if( request.method == "POST" ):

			final_image_name= request.POST['old_profile_photo']
			if( not(request.FILES.get('profile_photo','') == "") ):
				image_name = request.FILES['profile_photo']

				ext = image_name.name.split('.')[-1]

				if( ext not in imgtype ):
					return render(request,'farmer/update_profile.html',{'errors':['fileType']})


				try:
					os.remove('farmy/media/'+request.POST['old_profile_photo'])
					os.rmdir('farmy/media/images/farmer/'+request.POST['mobile_no'])
				except:
					pass

				final_image_name = 'farmy/media/images/farmer/registrations/'+request.POST['mobile_no']+"/"+request.POST['mobile_no'] +'.'+ext   # for fs
				fs = FileSystemStorage()
				filename = fs.save(final_image_name, image_name)

			cursor = connection.cursor()
			cursor.execute("update farmerApp_farmer_registration_tbl set profile_photo=%s,first_name=%s,last_name=%s,address=%s,dob=%s,gender=%s,timestamp=%s where id=%s",[final_image_name,request.POST['first_name'],request.POST['last_name'],request.POST['address'],request.POST['dob'],request.POST['gender'],request.POST['timestamp'],request.session['farmer_id']])
			city_name = request.POST['address']
			city_name = city_name.split(',')[-2]
			cursor.execute("select min(id) from weatherApp_my_cities_tbl where farmer_id_id=%s ",[request.session['farmer_id']])
			min_wid=cursor.fetchone()
			cursor.execute("update weatherApp_my_cities_tbl set cities=%s where id=%s ",[city_name,min_wid])

			cursor.close()
			return redirect('farmerApp:my_profile')


		else:
			data = farmer_registration_tbl.objects.filter(id=request.session['farmer_id'])
			return render(request,'farmer/update_profile.html',{'data':data})
	else:
		return redirect('farmerApp:login')


def delete_account(request):
	if( 'farmer_id' in request.session):

		#data = farmer_registration_tbl.objects.raw("update farmerApp_farmer_registration_tbl set account_status=%s",['deactivated'])
		cursor = connection.cursor()
		cursor.execute("update farmerApp_farmer_registration_tbl set account_status=%s where id=%s",['deactive',request.session['farmer_id']])

		cursor.close()

		request.session.clear()
		return redirect('farmerApp:register')
	else:
		return redirect('farmerApp:login')


def videos(request):
	if( 'farmer_id' in request.session):
		cursor=connection.cursor()
		cursor.execute("select * from adminApp_admin_yt_videos_tbl")
		data=cursor.fetchall()
		cursor.close()
		if len(data)==0:
			return render(request,'farmer/videos.html',{'data':""})
		else:
			return render(request,'farmer/videos.html',{'data':data})
	else:
		return redirect('farmerApp:login')




def logout(request):
	request.session.clear()
	return redirect('farmerApp:login')




def all_questions(request):
	if('farmer_id' in request.session):
		cursor = connection.cursor()
		cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id")
		#cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id join authorityApp_answer_tbl aa on q.id=aa.question_id_id join authorityApp_officer_registration_tbl ar on aa.authority_id_id=ar.id")
		data = cursor.fetchall()
		cursor.close()

		page = request.GET.get('page', 1)
		paginator = Paginator(data, 5)
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)

		if( len(data) == 0 ):
			return render(request,'farmer/my_questions.html',{'data':0,'title':'All Questions'})
		else:
			return render(request,'farmer/my_questions.html',{'data':data,'title':'All Questions'})
	else:
		return redirect('farmerApp:login')



def my_questions(request):
	if( 'farmer_id' in request.session):
		cursor = connection.cursor()
		cursor.execute("select * from farmerApp_questions_tbl where farmer_id_id=%s",[request.session['farmer_id']])
		data = cursor.fetchall()

		page = request.GET.get('page', 1)
		paginator = Paginator(data, 5)
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)

		cursor.close()
		if(len(data) ==0 ):
			return render(request,"farmer/my_questions.html",{'data':0,'title':'My Questions'})
		else:
			return render(request,"farmer/my_questions.html",{'data':data,'title':'My Questions'})
	else:
		return redirect('farmerApp:login')


def show_question(request,qid):
	if('farmer_id' in request.session):
		cursor = connection.cursor()
		#cursor.execute("select q.id,q.title,q.question,q.image1,q.image2,q.timestamp,q.status,r.profile_photo,r.first_name,r.last_name,r.email,r.account_status from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where q.id=%s",[qid])
		cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where q.id=%s",[qid])
		qdata = cursor.fetchall() # question data

		cursor.execute("select * from authorityApp_answer_tbl aa join authorityApp_officer_registration_tbl ar on aa.authority_id_id=ar.id WHERE aa.question_id_id=%s",[qid])
		adata = cursor.fetchall() # answer data


		cursor.close()


		return render(request,'farmer/show_question.html',{'qdata':qdata,'adata':adata})
	else:
		return redirect('farmerApp:login')


def delete_question(request,qid):

	cursor = connection.cursor()

	cursor.execute("select * from farmerApp_questions_tbl where id=%s",[qid])
	data = cursor.fetchall()

	if( data[0][3] == "" or data[0][4] == "" ):
		try:
			os.remove('farmy/media/'+str(data[0][3]))
		except:
			try:
				os.remove('farmy/media/'+str(data[0][4]))
			except:
				pass

	cursor.execute("delete from farmerApp_questions_tbl where id=%s",[qid])
	cursor.close()

	return redirect('farmerApp:my_questions')



def darkModeChange(request):
	if( 'darkMode' in request.session ):
		if( request.session['darkMode'] ):
			request.session['darkMode'] = False
		else:
			request.session['darkMode'] = True
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		#return HttpResponse('hello')
	else:
		request.session['darkMode'] = False
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


'''
select q.id,r.first_name,aa.id,ar.full_name from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id join authorityApp_answer_tbl aa on q.id=aa.question_id_id join authorityApp_officer_registration_tbl ar on aa.authority_id_id=ar.id
'''