from django.shortcuts import render,HttpResponse,redirect
from django.db import connection
import requests,pickle
from .models import *
from feedsApp.models import Feed
import requests,pickle
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def login(request):
	if( request.method == 'POST' ):
		try:
			data = admin_registration_tbl.objects.get(username=request.POST['username'])
		except:
			return render(request,'admin/login.html',{'errors':['Not registered']})
		if( data.status == "deactive" ):
			return render(request,'admin/login.html',{'errors':['blocked']})
		if( request.POST['password'] == data.password ):
			request.session['admin_id']=data.id
			request.session['admin_name']=data.username
			return redirect('adminApp:homepage')
		else:
			return render(request,'admin/login.html',{'errors':['Password is Incorrect']})
	else:
		return render(request,'admin/login.html')

def logout(request):
	request.session.clear()
	return render(request,'admin/login.html')

def homepage(request):
	if 'admin_id' in request.session :
		return render(request,'admin/index.html')
	else:
		return render(request,'admin/login.html')

def issues(request,id=0):
	if 'admin_id' in request.session :
		if id==0:
			cursor=connection.cursor()
			cursor.execute("select * from authorityApp_send_email_with_image where status='Unsolved'")
			data=cursor.fetchall()
			#return HttpResponse(data)
			cursor.close()
			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			return render(request,'admin/issues.html',{'data':data})
		else:
			cursor=connection.cursor()
			cursor.execute("update authorityApp_send_email_with_image set status=%s where id=%s",['Solved',id])
			cursor.execute("select * from authorityApp_send_email_with_image where status='Unsolved'")
			data=cursor.fetchall()
			#return HttpResponse(data)
			cursor.close()
			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			return render(request,'admin/issues.html',{'data':data})
	else:
		return render(request,'admin/login.html')

def add_feeds(request):
	if 'admin_id' in request.session :
	    """
        headers = {
        "apikey": "37c9d680-50c4-11eb-9469-2b1955fa0d7d"}

        params = (
           ("q","Farmer"),
           ("tbm","nws"),
           ("device","desktop"),
           ("gl","IN"),
           ("hl","en"),
           ("num","20"),
        );

        response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params);

        x=response.json()
        #print(x)
        f=open("FeedData.txt","wb")
        pickle.dump(response,f)
        f.close()
        #37c9d680-50c4-11eb-9469-2b1955fa0d7d
        """
	    f=open("FeedData.txt","rb")
	    data=pickle.load(f)
	    for i in range(19):
		    feeds=Feed(title=str(data['news_results'][i]['title']),link=str(data['news_results'][i]['link']),date=str(data['news_results'][i]['date']),source=str(data['news_results'][i]['source']),description=str(data['news_results'][i]['description']),thumbnail=str(data['news_results'][i]['thumbnail']))
		    feeds.save()
	    return render(request,'admin/index.html')
	else:
		return render(request,'admin/login.html')

def remove_feeds(request,id=0):
	if 'admin_id' in request.session :
		if id==0:
			if request.method=='POST':
				uploading_date=request.POST['uploading_date']
				cursor=connection.cursor()
				cursor.execute("delete from feedsApp_feed where uploading_date=%s",[uploading_date])
				cursor.close()
			cursor=connection.cursor()
			cursor.execute("select * from feedsApp_feed")
			data=cursor.fetchall()
			if len(data)==0:
				return render(request,'admin/remove_feeds.html',{'data':""})
			#return HttpResponse(data)
			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			return render(request,'admin/remove_feeds.html',{'data':data})
		else:
			cursor=connection.cursor()
			cursor.execute("delete from feedsApp_feed where id=%s",[id])
			cursor.execute("select * from feedsApp_feed")
			data=cursor.fetchall()
			if len(data)==0:
				return render(request,'admin/remove_feeds.html',{'data':""})
			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			return render(request,'admin/remove_feeds.html',{'data':data})
	else:
			return render(request,'admin/login.html')

def remove_videos(request,id=0):
	if 'admin_id' in request.session :
		if id==0:
			if request.method=='POST':
				uploading_date=request.POST['uploading_date']
				cursor=connection.cursor()
				cursor.execute("delete from adminApp_admin_yt_videos_tbl where uploading_date=%s",[uploading_date])
			cursor=connection.cursor()
			cursor.execute("select * from adminApp_admin_yt_videos_tbl")
			data=cursor.fetchall()
			if len(data)==0:
				return render(request,'admin/remove_videos.html',{'data':""})
			#return HttpResponse(data)
			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			return render(request,'admin/remove_videos.html',{'data':data})
		else:
			cursor=connection.cursor()
			cursor.execute("delete from adminApp_admin_yt_videos_tbl where id=%s",[id])
			cursor.execute("select * from adminApp_admin_yt_videos_tbl")
			data=cursor.fetchall()

			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			return render(request,'admin/remove_videos.html',{'data':data})
	else:
			return render(request,'admin/login.html')

def add_videos(request):
	if 'admin_id' in request.session:
		if request.method=='POST':
			title=request.POST['title']
			link=request.POST['link']
			date=str((datetime.datetime.now()).strftime("%Y-%m-%d"))
			cursor=connection.cursor()
			cursor.execute("insert into adminApp_admin_yt_videos_tbl(title,link,uploading_date) values(%s,%s,%s)",[title,link,date])

			cursor=connection.cursor()
			cursor.execute("select * from adminApp_admin_yt_videos_tbl")
			data=cursor.fetchall()
			if len(data)==0:
				return render(request,'admin/remove_videos.html',{'data':""})
			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			cursor.close()
			return render(request,'admin/remove_videos.html',{'data':data})
		else:
			return render(request,'admin/add_videos.html')
	else:
		return render(request,'admin/login.html')

def farmer_connect(request,id=0):
	if 'admin_id' in request.session :
		if id==0:
			cursor=connection.cursor()
			cursor.execute("select * from farmerApp_contact_us_tbl where status='Unsolved'")
			data=cursor.fetchall()
			#return HttpResponse(data)
			cursor.close()
			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			return render(request,'admin/farmer_connect.html',{'data':data})
		else:
			cursor=connection.cursor()
			cursor.execute("update farmerApp_contact_us_tbl set status=%s where id=%s",['Solved',id])
			cursor.execute("select * from farmerApp_contact_us_tbl where status='Unsolved'")
			data=cursor.fetchall()
			#return HttpResponse(data)
			cursor.close()
			page = request.GET.get('page', 1)
			paginator = Paginator(data, 5)
			try:
				data = paginator.page(page)
			except PageNotAnInteger:
				data = paginator.page(1)
			except EmptyPage:
				data = paginator.page(paginator.num_pages)
			return render(request,'admin/farmer_connect.html',{'data':data})
	else:
		return render(request,'admin/login.html')