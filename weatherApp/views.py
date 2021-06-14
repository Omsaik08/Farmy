from django.shortcuts import render,HttpResponse,redirect
import requests,json
from datetime import *
from django.db import connection
from .models import *
from authorityApp.models import *
from django.contrib import messages
from .forms import my_cities_tbl_form
from weatherApp.models import my_cities_tbl


# get city name and farmer_id defult from session



def homepage(request,city_name="1"):

	if ('farmer_id' in request.session):

		api_key="1911d1245e0aed5436a41e41ccccc903"
		dcity = my_cities_tbl.objects.filter(farmer_id=request.session['farmer_id']).order_by('timestamp')  # -timestamp for descending sort
		res_dcity = dcity[0].cities      #gives first city of user
		if( city_name != "1" ):
			cities=city_name
		else:
			cities=res_dcity

		# for my_cities.html
		if( request.method == 'POST' ):
			cities = request.POST['cities']
		

		# start for getting one day weather
		base_url = "http://api.openweathermap.org/data/2.5/weather?"	
		complete_url = base_url + "appid=" + api_key + "&q=" + cities +"&units=metric"
		response = requests.get(complete_url) 
		x = response.json()

		weather_data={}
		
		degrees=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
		if(int(x['cod'])==404):
			
			city=0
			return render(request,'weather/homepage.html',{'weather_data':weather_data,'city':0})
		else:
			weather_data['City']=cities
			weather_data['Weather_Type']=x['weather'][0]['main']
			weather_data['Description']=x['weather'][0]['description']
			weather_data['Icon']=x['weather'][0]['icon']
			weather_data['Current_Temperature']=str(x['main']['temp'])+" ℃"
			weather_data['Feels_Like']=str(x['main']['feels_like'])+" ℃"
			weather_data['Minimum_Temperature']=str(x['main']['temp_min'])+" ℃"
			weather_data['Maximum_Temperature']=str(x['main']['temp_max'])+" ℃"
			weather_data['Pressure']=str(x['main']['temp'])+"hPa"
			weather_data['Humidity']=str(x['main']['humidity'])+" %"
			direction=int(x['wind']['deg']//22.5)%16
			weather_data['Wind_Speed']=str(x['wind']['speed'])
			weather_data['Wind_Degree']=str(degrees[direction])
			weather_data['Cloud_Percentage']=str(x['clouds']['all'])+" %"
			try:
				weather_data['Rain_1hr']=str(x['rain']['1h'])+" mm"
			except:
				weather_data['Rain_1hr']="--"
			try:
				weather_data['Snow_3hr']=str(x['snow']['1h'])+" mm"
			except:
				weather_data['Snow_3hr']="--"
			weather_data['Country']=str(x['sys']['country'])

			utc_sunrise=datetime.datetime.fromtimestamp(x['sys']['sunrise'])
			weather_data['Sunrise']=str(utc_sunrise.strftime("%d-%B-%Y  %I:%M:%S%p"))

			utc_sunset=datetime.datetime.fromtimestamp(x['sys']['sunset'])
			weather_data['Sunset']=str(utc_sunset.strftime("%d-%B-%Y  %I:%M:%S%p"))
			
			if( request.method == 'POST' ):
				form = my_cities_tbl_form(request.POST)

				if(form.is_valid()):
				 	form.save()
			
					#return render(request,'weather/my_cities.html',{'status':0})

			#for i,j in weather_data.items():
			#	print(i,":",j)
			# end for getting one day weather


		# start for getting next five day weather

		api_call="https://api.openweathermap.org/data/2.5/forecast?q="+cities+"&units=metric&appid="+api_key
		five_day=[]
		demo=[]
		response = requests.get(api_call) 
		x = response.json()
		weather_data1={}
		degrees=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
		no=[0,1,2,3,4,10,11,12,18,19,20,26,27,28,34,35,36]


		for i in range(0,40):
			if i in no :
				continue
			elif(int(x['cod'])==404):
				city=0
				return render(request,'weather/homepage.html',{'weather_data':weather_data,'city':0})
			else:
				weather_data1['City']=cities
				weather_data1['DateTime']=datetime.datetime.strptime(str(x['list'][i]['dt_txt']),"%Y-%m-%d %H:%M:%S").strftime("%d-%B-%Y  %I:%M:%S%p")
				weather_data1['Weather_Type']=x['list'][i]['weather'][0]['main']
				weather_data1['Description']=x['list'][i]['weather'][0]['description']
				weather_data1['Weather_Icon ']=x['list'][i]['weather'][0]['icon']
				weather_data1['Current_Temperature']=str(x['list'][i]['main']['temp'])+" ℃"
				weather_data1['Feels_Like']=str(x['list'][i]['main']['feels_like'])+" ℃"
				weather_data1['Minimum_Temperature']=str(x['list'][i]['main']['temp_min'])+" ℃"
				weather_data1['Maximum_Temperature']=str(x['list'][i]['main']['temp_max'])+" ℃"
				weather_data1['Pressure']=str(x['list'][i]['main']['temp'])+"hPa"
				weather_data1['Humidity']=str(x['list'][i]['main']['humidity'])+" %"
				direction=int(x['list'][i]['wind']['deg']//22.5)%16
				weather_data1['Wind_Speed']=str(x['list'][i]['wind']['speed'])
				weather_data1['Wind_Degree']=str(degrees[direction])
				weather_data1['Cloud_Percentage']=str(x['list'][i]['clouds']['all'])+" %"
				
				weather_data1['Country']=str(x['city']['country'])

				utc_sunrise=datetime.datetime.fromtimestamp(x['city']['sunrise'])
				weather_data1['Sunrise']=str(utc_sunrise.strftime("%d-%B-%Y  %I:%M:%S%p"))

				utc_sunset=datetime.datetime.fromtimestamp(x['city']['sunrise'])
				weather_data1['Sunset']=str(utc_sunset.strftime("%d-%B-%Y  %I:%M:%S%p"))
			demo.append(weather_data1)
			weather_data1={}


		"""
		for i in range(len(demo)):
			print(demo[i])
			print()
		print(len(demo))
		"""

		# end for getting next five day weather


		return render(request,'weather/homepage.html',{'one_day':weather_data,'five_day':demo,"farmer_id":request.session['farmer_id']})
	else:
		return redirect('farmerApp:login')






def my_cities(request):
	if ('farmer_id' in request.session):
		data = my_cities_tbl.objects.all().filter(farmer_id=request.session['farmer_id'])
		return render(request,"weather/my_cities.html",{'data':data})
	else:
		return redirect('farmerApp:login')



def authority_homepage(request,city_name="solapur"):
	if( 'authority_id' in request.session ):

		api_key="1911d1245e0aed5436a41e41ccccc903"
		data = officer_registration_tbl.objects.filter(id=request.session['authority_id'])
		addr=(data[0].address).split(",")
		cities = addr[-2]

		# for my_cities.html
		if( request.method == 'POST' ):
			cities = request.POST['cities']
		

		# start for getting one day weather
		base_url = "http://api.openweathermap.org/data/2.5/weather?"	
		complete_url = base_url + "appid=" + api_key + "&q=" + cities +"&units=metric"
		response = requests.get(complete_url) 
		x = response.json()

		weather_data={}
		
		degrees=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
		if(int(x['cod'])==404):
			
			city=0
			return render(request,'weather/authority_homepage.html',{'weather_data':weather_data,'city':0})
		else:
			weather_data['City']=cities
			weather_data['Weather_Type']=x['weather'][0]['main']
			weather_data['Description']=x['weather'][0]['description']
			weather_data['Icon']=x['weather'][0]['icon']
			weather_data['Current_Temperature']=str(x['main']['temp'])+" ℃"
			weather_data['Feels_Like']=str(x['main']['feels_like'])+" ℃"
			weather_data['Minimum_Temperature']=str(x['main']['temp_min'])+" ℃"
			weather_data['Maximum_Temperature']=str(x['main']['temp_max'])+" ℃"
			weather_data['Pressure']=str(x['main']['temp'])+"hPa"
			weather_data['Humidity']=str(x['main']['humidity'])+" %"
			direction=int(x['wind']['deg']//22.5)%16
			weather_data['Wind_Speed']=str(x['wind']['speed'])
			weather_data['Wind_Degree']=str(degrees[direction])
			weather_data['Cloud_Percentage']=str(x['clouds']['all'])+" %"
			try:
				weather_data['Rain_1hr']=str(x['rain']['1h'])+" mm"
			except:
				weather_data['Rain_1hr']="--"
			try:
				weather_data['Snow_3hr']=str(x['snow']['1h'])+" mm"
			except:
				weather_data['Snow_3hr']="--"
			weather_data['Country']=str(x['sys']['country'])

			utc_sunrise=datetime.datetime.fromtimestamp(x['sys']['sunrise'])
			weather_data['Sunrise']=str(utc_sunrise.strftime("%d-%B-%Y  %I:%M:%S%p"))

			utc_sunset=datetime.datetime.fromtimestamp(x['sys']['sunset'])
			weather_data['Sunset']=str(utc_sunset.strftime("%d-%B-%Y  %I:%M:%S%p"))
			
			if( request.method == 'POST' ):
				form = my_cities_tbl_form(request.POST)

				if(form.is_valid()):
				 	form.save()
			
					#return render(request,'weather/my_cities.html',{'status':0})

			#for i,j in weather_data.items():
			#	print(i,":",j)
			# end for getting one day weather


		# start for getting next five day weather

		api_call="https://api.openweathermap.org/data/2.5/forecast?q="+cities+"&units=metric&appid="+api_key
		five_day=[]
		demo=[]
		response = requests.get(api_call) 
		x = response.json()
		weather_data1={}
		degrees=['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW','W','WNW','NW','NNW']
		no=[0,1,2,3,4,10,11,12,18,19,20,26,27,28,34,35,36]


		for i in range(0,40):
			if i in no :
				continue
			elif(int(x['cod'])==404):
				city=0
				return render(request,'weather/authority_homepage.html',{'weather_data':weather_data,'city':0})
			else:
				weather_data1['City']=cities
				weather_data1['DateTime']=datetime.datetime.strptime(str(x['list'][i]['dt_txt']),"%Y-%m-%d %H:%M:%S").strftime("%d-%B-%Y  %I:%M:%S%p")
				weather_data1['Weather_Type']=x['list'][i]['weather'][0]['main']
				weather_data1['Description']=x['list'][i]['weather'][0]['description']
				weather_data1['Weather_Icon ']=x['list'][i]['weather'][0]['icon']
				weather_data1['Current_Temperature']=str(x['list'][i]['main']['temp'])+" ℃"
				weather_data1['Feels_Like']=str(x['list'][i]['main']['feels_like'])+" ℃"
				weather_data1['Minimum_Temperature']=str(x['list'][i]['main']['temp_min'])+" ℃"
				weather_data1['Maximum_Temperature']=str(x['list'][i]['main']['temp_max'])+" ℃"
				weather_data1['Pressure']=str(x['list'][i]['main']['temp'])+"hPa"
				weather_data1['Humidity']=str(x['list'][i]['main']['humidity'])+" %"
				direction=int(x['list'][i]['wind']['deg']//22.5)%16
				weather_data1['Wind_Speed']=str(x['list'][i]['wind']['speed'])
				weather_data1['Wind_Degree']=str(degrees[direction])
				weather_data1['Cloud_Percentage']=str(x['list'][i]['clouds']['all'])+" %"
				
				weather_data1['Country']=str(x['city']['country'])

				utc_sunrise=datetime.datetime.fromtimestamp(x['city']['sunrise'])
				weather_data1['Sunrise']=str(utc_sunrise.strftime("%d-%B-%Y  %I:%M:%S%p"))

				utc_sunset=datetime.datetime.fromtimestamp(x['city']['sunrise'])
				weather_data1['Sunset']=str(utc_sunset.strftime("%d-%B-%Y  %I:%M:%S%p"))
			demo.append(weather_data1)
			weather_data1={}


		"""
		for i in range(len(demo)):
			print(demo[i])
			print()
		print(len(demo))
		"""

		# end for getting next five day weather


		return render(request,'weather/authority_homepage.html',{'one_day':weather_data,'five_day':demo,"farmer_id":request.session['authority_id']})
	else:
		return redirect('authorityApp:login')



