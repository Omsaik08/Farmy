from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests,pickle
from .models import Feed
#from .models import my_cities_tbl
from authorityApp.models import amendment_bill_tbl

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def index(request):
	if( 'farmer_id' in request.session ):
		data=Feed.objects.all()

		page = request.GET.get('page', 1)
		paginator = Paginator(data, 5)
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)
		return render(request,'feeds/homepage.html',{'data':data})
	else:
		return redirect('farmerApp:login')

def authority_homepage(request):
	if('authority_id' in request.session ):
		data=Feed.objects.all()

		page = request.GET.get('page', 1)
		paginator = Paginator(data, 5)
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)
		return render(request,'feeds/authority_homepage.html',{'data':data})
	else:
		return redirect('authorityApp:login')

def showbills(request):
	if( 'farmer_id' in request.session ):
		data = amendment_bill_tbl.objects.all()
		page = request.GET.get('page', 1)
		paginator = Paginator(data, 5)
		try:
			data = paginator.page(page)
		except PageNotAnInteger:
			data = paginator.page(1)
		except EmptyPage:
			data = paginator.page(paginator.num_pages)

		return render(request,'feeds/bills.html',{'data':data})
	else:
		return redirect('farmerApp:login')
