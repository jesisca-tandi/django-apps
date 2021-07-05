from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse 
from django.db import connection #␣connection␣module␣for␣Database␣operations
# Create your views here.

def AppRaw(request):
	# Renders 'AppRaw/forms.html' template with empty dictionary
	return render(request, 'AppRaw/forms.html', {})



def getrows_db(request):
	if request.method == 'GET':

		# values sent via GET by the user
		form = request.GET.get('regex_id', '')
		query = "SELECT * FROM item WHERE i_name ~ \'%s\'" % form

		# The connection object
		c = connection.cursor()

		# Execute query by connection object
		c.execute(query)

		# Fetch all the rows. fetchall() returns a list of tuples
		results = c.fetchall()
		context = {'records': results}
		return render(request, 'AppRaw/results.html', context)

		