from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse 
from django.db import connection 
from . import models
# Create your views here.

def AppORM(request):
	# Renders 'AppRaw/forms.html' template with empty dictionary
	return render(request, 'AppORM/forms.html', {})



def getrows_db(request):
	if request.method == 'GET':

		# values sent via GET by the user
		form = request.GET.get('regex_id', '')

		results = models.Item.objects.filter(i_name__regex="{}".format(form))
		context = {'records': list(results)}
		return render(request, 'AppORM/results.html', context)
