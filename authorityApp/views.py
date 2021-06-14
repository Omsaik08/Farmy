from django.shortcuts import render,redirect,HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .forms import *
from .models import *
import pathlib
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from django.db import connection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from fpdf import FPDF
from django.http import FileResponse
import datetime
from django.http import JsonResponse
import random

gmailaddress = "bizzfarmy@gmail.com"
gmailpassword = "bizzfarmy@321"

# Create your views here.
imgtype = ['png','jpg','jpeg']

def homepage(request):
	if 'authority_id' in request.session :

		data = []

		cursor = connection.cursor()

		cursor.execute(" SELECT count(*),lower(substring_index( substring_index(ar.address,',',-2),',',1 )) FROM authorityApp_officer_registration_tbl ar join farmerApp_farmer_registration_tbl fr on lower(substring_index( substring_index(ar.address,',',-2),',',1 )) = lower(substring_index( substring_index(fr.address,',',-2),',',1 )) join farmerApp_questions_tbl q on q.farmer_id_id=fr.id where ar.id=%s and q.status='not answered' ",[request.session['authority_id']])
		pql = cursor.fetchall()  #pending question location
		data.append(pql[0])

		cursor.execute(" SELECT count(*),lower(substring_index( substring_index(ar.address,',',-2),',',1 )) FROM authorityApp_officer_registration_tbl ar join farmerApp_farmer_registration_tbl fr on lower(substring_index( substring_index(ar.address,',',-2),',',1 )) = lower(substring_index( substring_index(fr.address,',',-2),',',1 )) join farmerApp_questions_tbl q on q.farmer_id_id=fr.id where ar.id=%s ",[request.session['authority_id']])
		tql = cursor.fetchall()  #total question location
		data.append(tql[0])

		cursor.execute(" SELECT count(*) from farmerApp_questions_tbl where status = 'not answered' ")
		tpq = cursor.fetchall()  #total pending question on platform
		data.append(tpq[0])

		cursor.execute(" SELECT count(*) from farmerApp_questions_tbl ")
		tqp = cursor.fetchall()  #total question on platform
		data.append(tqp[0])

		cursor.close()
		return render(request,'authority/homepage.html',{'data':data})
	else:
		return redirect('authorityApp:login')

def register(request):
	if request.method=='POST':
		try:
			ext = request.FILES['profile_photo'].name
			ext = ext.lower()
			ext = ext.split('.')[-1]
			if( ext not in imgtype ):
				return render(request,'authorityApp/login.html',{'errors':['fileType']})

		except:
			pass




		form = officer_registration_tbl_form(request.POST,request.FILES)
		if( form.is_valid() ):
			form.save()


			try:
				t = officer_registration_tbl.objects.get(timestamp=request.POST['timestamp'])
			except:
				pass



		else:
			return render(request,'authority/login.html',{'errors':form.errors})
			#return render(request,'farmer/login.html',{'status':0})
		return redirect('authorityApp:login')

	else:
		return render(request,'authority/register.html')

def login(request):
    username=request.GET.get("username",None)
    password=request.GET.get("password",None)
    if username==None and password==None:
        return render(request,'authority/login.html')
    if( '@' in username ):# for username as email
        try:
            result = officer_registration_tbl.objects.get(email=username)
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
            result = officer_registration_tbl.objects.get(mobile_no=username)
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
        request.session['authority_id']=result.id
        cursor = connection.cursor()
        cursor.execute('select full_name,profile_photo from authorityApp_officer_registration_tbl where id=%s',[result.id])
        name=cursor.fetchall()
        request.session['authority_name']=name[0][0]
        request.session['profile_photo']=name[0][1]
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
				data = officer_registration_tbl.objects.get(email=request.POST['username'])
			except:
				return render(request,'authority/login.html',{'errors':['Not registered']})
			if( data.account_status == "deactive" ):
				return render(request,'authority/login.html',{'errors':['blocked']})


		else: # for username as mobile
			try:
				data = officer_registration_tbl.objects.get(mobile_no=request.POST['username'])
			except:# means no Mobile no. exists
				return render(request,'authority/login.html',{'errors':['Not registered']})
			if( data.account_status == "deactive" ):
				return render(request,'authority/login.html',{'errors':['blocked']})

		if( request.POST['password'] == data.password ):
			request.session['authority_id']=data.id
			cursor = connection.cursor()
			cursor.execute('select full_name,profile_photo from authorityApp_officer_registration_tbl where id=%s',[data.id])
			name=cursor.fetchall()
			request.session['authority_name']=name[0][0]
			request.session['profile_photo']=name[0][1]
			request.session['darkMode'] = False

			return redirect('authorityApp:homepage')
		else:
			return render(request,'authority/login.html',{'errors':['Password is Incorrect']})

	else:
		return render(request,'authority/login.html')"""

def logout(request):
	request.session.clear()
	return redirect('authorityApp:login')



def forgot(request):
	if( request.method == 'POST' ):
		send_otp_to=str(request.POST['username'])
		cursor = connection.cursor()
		cursor.execute("select email from authorityApp_officer_registration_tbl");
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

Dear Authority,\n\nYour OTP for Change of Password is: """+str(OTP)+""".\n\nThanks and Regards,\nTeam FARMY."""
				mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
				mailServer.starttls()
				mailServer.login(gmailaddress , gmailpassword)
				mailServer.sendmail(gmailaddress, send_otp_to , message)
				mailServer.quit()
				f=1
				break
		if f:
			return render(request,'authority/authority_otp.html',{'username':request.POST['username'],'OTP':OTP,'status':'found'})
		else:
			return render(request,'authority/authority_otp.html',{'status':'not found'})
	else:
		return render(request,'authority/forgot.html')



def authority_otp(request):# forgot password
	if request.method=='POST':
		if request.POST['otp']==request.POST['main_otp']:
			return render(request,'authority/change_password.html',{'username':request.POST['username']})
		else:
			return render(request,'authority/authority_otp.html',{'username':request.POST['username'],'status':'invalid'})
	return redirect('authorityApp:forgot')

def change_password(request):
	if request.method=='POST':
		new_pass=request.POST['password']
		cursor = connection.cursor()
		cursor.execute("update authorityApp_officer_registration_tbl set password=%s where email=%s",[new_pass,request.POST['username']])
		cursor.close()
		return redirect('authorityApp:login')
	return redirect('authorityApp:forgot')



def add_bills(request):
	if 'authority_id' in request.session :
		if request.method=='POST':
			ext = request.FILES['bill'].name
			ext = ext.lower()
			ext = ext.split(".")[-1]
			if ext=="pdf":
				form = officer_bill_tbl_form(request.POST,request.FILES)
				if( form.is_valid() ):
					form.save()
					return redirect('authorityApp:show_bills')
				else:
					return HttpResponse('no')
			else:
				return HttpResponse("Invalid Image Type")
		return render(request,'authority/add_bills.html')
	else:
		return redirect('authorityApp:login')

def delete_bills(request,bill_id):
	if 'authority_id' in request.session :
		data = amendment_bill_tbl.objects.get(id=bill_id)
		r = 'farmy/media/'+str(data.bill)
		os.remove(r)
		amendment_bill_tbl.objects.filter(id=bill_id).delete()
		data = amendment_bill_tbl.objects.filter(authority_id_id=request.session['authority_id'])
		return render(request,'authority/show_bills.html')
	else:
		return redirect('authorityApp:login')

def show_bills(request):
	if 'authority_id' in request.session :
		data = amendment_bill_tbl.objects.filter(authority_id_id=request.session['authority_id'])

		page = request.GET.get('page', 1)
		paginator = Paginator(data, 2)
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)
		return render(request,'authority/show_bills.html',{'data':data})
	else:
		return redirect('authorityApp:login')

def my_profile(request):
	if 'authority_id' in request.session :
		data = officer_registration_tbl.objects.filter(id=request.session['authority_id'])
		return render(request,'authority/my_profile.html',{'data':data})
	else:
		return redirect('authorityApp:login')

def update_profile(request):
	if 'authority_id' in request.session :
		if( request.method == "POST" ):

			final_image_name= request.POST['old_profile_photo']
			if( not(request.FILES.get('profile_photo','') == "") ):
				image_name = request.FILES['profile_photo']

				ext = image_name.name.split('.')[-1]
				ext = ext.lower()
				ext = ext.split('.')[-1]
				if( ext not in imgtype ):
					return render(request,'authority/update_profile',{'errors':['fileType']})

				try:
					os.remove('farmy/media/'+request.POST['old_profile_photo'])
					os.rmdir('farmy/media/images/farmer/'+request.POST['mobile_no'])
				except:
					pass

				final_image_name = 'farmy/media/images/officer/registrations/'+ request.POST['mobile_no'] + '/' + request.POST['mobile_no'] +'.'+ext   # for fs
				fs = FileSystemStorage()
				filename = fs.save(final_image_name, image_name)
			cursor = connection.cursor()
			cursor.execute("update authorityApp_officer_registration_tbl set profile_photo=%s,full_name=%s,address=%s,dob=%s,gender=%s,timestamp=%s where id=%s",[final_image_name,request.POST['full_name'],request.POST['address'],request.POST['dob'],request.POST['gender'],request.POST['timestamp'],request.session['authority_id']])
			cursor.close()
			return redirect('authorityApp:my_profile')
		else:
			data = officer_registration_tbl.objects.filter(id=request.session['authority_id'])
			return render(request,'authority/update_profile.html',{'data':data})
	else:
		return redirect('authorityApp:login')

def change_password(request):
	if 'authority_id' in request.session :
		return render(request,'authority/change_password.html')
	else:
		return redirect('authorityApp:login')

def delete_account(request):
	if 'authority_id' in request.session :
		cursor = connection.cursor()
		cursor.execute("update authorityApp_officer_registration_tbl set account_status=%s where id=%s",['deactive',request.session['authority_id']])
		cursor.close()
		request.session.clear()
		return redirect('authorityApp:register')
	else:
		return redirect('authorityApp:login')



def contact_admin(request):
	if 'authority_id' in request.session :
		form=emailForm()
		if request.method=='POST':
			form=emailForm(request.POST,request.FILES)
			if form.is_valid():
				email_pr=form.save(commit=False)
				demo=request.FILES['image'].name
				Imgname=demo.split(".")[-1]
				#print(Imgname)
				if Imgname.lower() in ['png','jpg','jpeg']:
					email_pr.save()


					imgpath ='farmy/media/'+'Email/authority_id_issue.'+Imgname
					img_data = open(imgpath, 'rb').read()
					msg = MIMEMultipart()
					emails=["omsaikalekar2000@gmail.com","buravenu@gmail.com","maheshrachha1225@gmail.com","hemantdyavarkonda2000@gmail.com"]
					msg['Subject'] = 'Error From Platform'
					msg['From'] = 'bizzfarmy@gmail.com'
					msg['To'] = ",".join(emails)

					text = MIMEText("Hi admin,\n\nYou Platform has got a issue.Please Solve it.\nAttaching a Image for your reference!\n\nIssue:"+str(request.POST['message'])+"\n\nThanks and Regards,\n"+str(request.session['authority_name'][0])+"!")
					msg.attach(text)
					image = MIMEImage(img_data, name="Issue")
					msg.attach(image)

					s = smtplib.SMTP('smtp.gmail.com' , 587)
					s.ehlo()
					s.starttls()
					s.ehlo()
					s.login('bizzfarmy@gmail.com', 'bizzfarmy@321')
					s.sendmail('bizzfarmy@gmail.com',emails, msg.as_string())
					#sprint('sent')
					s.quit()

					#remove file
					os.remove(imgpath)
					return redirect('authorityApp:homepage')
				else:
					return HttpResponse(form.errors())
			else:
				return HttpResponse("Invalid Image Type")

		return render(request,'authority/contact_admin.html')
	else:
		return redirect('authorityApp:login')



def all_questions(request):
	if('authority_id' in request.session):
		cursor = connection.cursor()
		cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id")
		data = cursor.fetchall()
		#cursor.execute(" select lower(substring_index( substring_index(address,',',-2),',',1 )) from authorityApp_officer_registration_tbl where id=%s ",[request.session['authority_id']])
		#cityName = cursor.fetchall()
		cursor.close()



		page = request.GET.get('page', 1)
		paginator = Paginator(data, 5)
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)

		if( len(data)  == 0 ):
			return render(request,'authority/all_questions.html',{'data':0})
		else:
			return render(request,'authority/all_questions.html',{'data':data})
	else:
		return redirect('authorityApp:login')

def pending_questions(request):
	if('authority_id' in request.session):
		cursor = connection.cursor()
		cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id")
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

		return render(request,'authority/all_questions.html',{'data':data})
	else:
		return redirect('authorityApp:login')


def show_question(request,qid):
	if('authority_id' in request.session):
		if( request.method == "POST" ):


			cursor = connection.cursor()

			cursor.execute(" update farmerApp_questions_tbl set status='answered' where id=%s",[request.POST['question_id']])

			cursor.execute("insert into authorityApp_answer_tbl (answer,timestamp,likes,dislikes,authority_id_id,question_id_id) VALUES (%s,%s,%s,%s,%s,%s) ",[request.POST['answer'],request.POST['timestamp'],request.POST['likes'],request.POST['dislikes'],request.POST['authority_id'],request.POST['question_id']])


			cursor.execute("select q.question,r.first_name,r.last_name,r.email from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where q.id=%s",[qid])
			qdata = cursor.fetchall() # question data

			name=qdata[0][1] + " " + qdata[0][2]
			mail=qdata[0][3]
			subject="Query has been resolved !"

			message = """\
From:"""+gmailaddress+"""
To:"""+mail+"""
Subject:"""+subject+"""

Dear """+str(name)+""",\n\nAgricultural Authority has answered to your question : \n"""+ (qdata[0][0]) +""".\nPlease Login To Your Account,To check answer !\nHappy Farming. \n\nThanks and Regards,\nTeam FARMY."""
			mailServer = smtplib.SMTP('smtp.gmail.com' , 587)
			mailServer.starttls()
			mailServer.login(gmailaddress , gmailpassword)
			mailServer.sendmail(gmailaddress, mail , message)
			#print(" \n Sent!")
			mailServer.quit()


			cursor.close()

			return redirect('authorityApp:all_questions')  # answered questions page
		else:
			cursor = connection.cursor()
			cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where q.id=%s",[qid])
			qdata = cursor.fetchall() # question data
			cursor.execute("select * from authorityApp_answer_tbl aa join authorityApp_officer_registration_tbl ar on aa.authority_id_id=ar.id WHERE aa.question_id_id=%s",[qid])
			adata = cursor.fetchall() # answer data

			return render(request,'authority/show_question.html',{'qdata':qdata,'adata':adata})
	else:
		return redirect('authorityApp:login')

def genrate_report(request):
	if( 'authority_id' in request.session ):
		f=open('Report.txt','w')
		tdate = str(datetime.datetime.now())
		tdate =tdate[0:10]
		data = officer_registration_tbl.objects.filter(id=request.session['authority_id'])
		cursor = connection.cursor()
		cursor.execute('SELECT count(*) FROM farmerApp_questions_tbl')
		nqp=cursor.fetchall()

		cursor.execute('SELECT count(*) FROM farmerApp_questions_tbl where status="answered" ')
		naqp=cursor.fetchall()

		cursor.execute('SELECT count(*) FROM `authorityApp_answer_tbl` where authority_id_id=%s',[request.session['authority_id']])
		nqay=cursor.fetchall()

		cursor.execute('SELECT COUNT(*) FROM farmerApp_farmer_registration_tbl')
		tfp=cursor.fetchall()

		cursor.execute('SELECT COUNT(*) FROM farmerApp_farmer_registration_tbl where account_status="active"')
		tfap=cursor.fetchall()

		cursor.execute('SELECT COUNT(*) FROM farmerApp_farmer_registration_tbl where account_status="deactive"')
		tfip=cursor.fetchall()
		message=""""FARMY REPORT"
	Date of Report Genration: """+str(tdate)+"""

	1. Officer Information :

	Authority Name        : """+str(data[0].full_name)+"""
	Authority Email       : """+str(data[0].email)+"""
	Authority Mobile      : +91 """+str(data[0].mobile_no)+"""
	Authority DOB         : """+str(data[0].dob)+"""
	Authority Location    : """+str(data[0].address)+"""
	Date of Registration  : """+str(data[0].timestamp)[0:9]+"""

	2. Platform Usage :

	Number of Question on platform           : """+str(nqp[0][0])+"""
	Number of Answered Questions on platform : """+str(naqp[0][0])+"""
	Number of Questions Ansewered by you     : """+str(nqay[0][0])+"""

	3. Farmer Information :

	Total Farmer's On platform                    : """+str(tfp[0][0])+"""
	Total number of active farmer's On platform   : """+str(tfap[0][0])+"""
	Total number of inactive farmer's On platform : """+str(tfip[0][0])+"""

	This is Autogenrated and Confidential Report we request you to do not share this with anyone.
	Farmy-2021 © Coyrights.
	"""
		f.write(message)
		f.close()

		pdf=FPDF()
		pdf.add_page()
		pdf.set_font("Arial",size=12)
		f=open('Report.txt','r')
		for data in f:
			pdf.cell(200,10,txt=data,ln=1)
		pdf.output('Report.pdf')

		response = FileResponse(open('Report.pdf', 'rb'))
		return response
	else:
		return redirect('authorityApp:login')


def filterQuestions(request):
	if( 'authority_id' in request.session ):
		if( request.method == 'POST' ):
			cursor = connection.cursor()
			if( request.POST['cityName'] != "" ):

				if( request.POST['qstatus'].lower()== 'all'):
					if( request.POST['tstatus'] == 'asc' ):
						cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where lower(substring_index( substring_index(r.address,',',-2),',',1 )) = %s order by q.timestamp ",[request.POST['cityName'].lower()])
					else:
						cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where lower(substring_index( substring_index(r.address,',',-2),',',1 )) = %s order by q.timestamp desc ",[request.POST['cityName'].lower()])
				else:
					if( request.POST['tstatus'] == 'asc' ):
						cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where lower(substring_index( substring_index(r.address,',',-2),',',1 )) = %s && q.status=%s order by q.timestamp ",[request.POST['cityName'].lower(),request.POST['qstatus']])
					else:
						cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where lower(substring_index( substring_index(r.address,',',-2),',',1 )) = %s && q.status=%s order by q.timestamp desc ",[request.POST['cityName'].lower(),request.POST['qstatus']])
				data = cursor.fetchall()
				cursor.close()
				return render(request,'authority/all_questions.html',{'data':data})
			else:
				if( request.POST['qstatus'].lower()== 'all'):
					if( request.POST['tstatus'] == 'asc' ):
						cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id order by q.timestamp ")
					else:
						cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id order by q.timestamp desc ")
				else:
					if( request.POST['tstatus'] == 'asc' ):
						cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where q.status=%s order by q.timestamp ",[request.POST['qstatus']])
					else:
						cursor.execute("select * from farmerApp_questions_tbl q join farmerApp_farmer_registration_tbl r on q.farmer_id_id=r.id where q.status=%s order by q.timestamp desc ",[request.POST['qstatus']])
				data = cursor.fetchall()
				cursor.close()
				return render(request,'authority/all_questions.html',{'data':data})
	else:
		return redirect('authorityApp:login')



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

def faq(request):
	return render(request,'authority/faq.html')

def privacy_policy(request):
	return render(request,'authority/privacy_policy.html')

def terms_and_conditions(request):
	return render(request,'authority/terms_and_conditions.html')

def about(request):
	return render(request,'authority/about.html')
'''
SELECT ar.address FROM authorityApp_officer_registration_tbl ar join farmerApp_farmer_registration_tbl fr on lower(substring_index( substring_index(ar.address,',',-2),',',1 )) = lower(substring_index( substring_index(fr.address,',',-2),',',1 )) join farmerApp_questions_tbl q on q.farmer_id_id=fr.id where ar.id=1 and q.status='not answered'
'''