from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse 
from django.db import connection 
from . import models
# Create your views here.

def AppLine(request):

	# Renders 'AppRaw/forms.html' template with empty dictionary
	return render(request, 'AppLine/forms.html', {})



def processRequest(request):

	context = {}

	if request.method == 'POST':

		# Get the filled values
		requestedQty, requestedItem, requestedWarehouse, requestedLine = loadSavedItem(request)

		# Items to keep
		itemsToKeep = {
		'requestedItem': requestedItem,
		'requestedQty': requestedQty,
		'requestedWarehouse': requestedWarehouse,
		'requestedLine': requestedLine
		}

		if 'getItemsButton' in request.POST:

			# Get all search results
			context = getSearchResults(request)
			contextToKeep = keepSavedItem(**itemsToKeep)
			context.update(contextToKeep)


		# To prevent submission of order when both buttons are pressed (happen when enter is pressed)
		if ('checkStockButton' in request.POST ) and ('getItemsButton' not in request.POST):

			context = dict()

			# Do a check on the order first
			errorMessage = checkOrder(request)

			if (len(errorMessage) == 0):

				availableItems = models.Stock.objects.filter(i=requestedItem).filter(w=requestedWarehouse)
				stockAvailable = list(availableItems.values())[0]['s_qty']

				# Check stock if order
				if requestedLine == 'Order':

					if len(availableItems)==1:

						if stockAvailable >= requestedQty:

							newStock = stockAvailable - requestedQty
							models.Stock.objects.filter(i=requestedItem).filter(w=requestedWarehouse).update(s_qty=newStock)
							successFlag = True

						else:

							# Get all search results
							contextSearchResults = getSearchResults(request)
							context.update(contextSearchResults)
							contextToKeep = keepSavedItem(**itemsToKeep)
							context.update(contextToKeep)
							successFlag = False

					else:
						print('Can''t find items in the database')

				else:

					newStock = stockAvailable + requestedQty
					models.Stock.objects.filter(i=requestedItem).filter(w=requestedWarehouse).update(s_qty=newStock)
					successFlag = True

				context['lineType'] = requestedLine
				context['successFlag'] = successFlag

			else:

				# Get all search results
				contextSearchResults = getSearchResults(request)
				context.update(contextSearchResults)
				contextToKeep = keepSavedItem(**itemsToKeep)
				context.update(contextToKeep)

				context['errorMessage'] = errorMessage

	return render(request, 'AppLine/forms.html', context)


def getSearchResults(request):

	if request.method == 'POST':

		# Get items search results
		itemStr = request.POST.get('itemsRegex', '')
		itemResults = []
		if itemStr is not '':
			itemResults = models.Item.objects.filter(i_name__regex="{}".format(itemStr))

		# Get warehouse search results
		warehouseStr = request.POST.get('warehouseRegex', '')
		warehouseResults = []
		if warehouseStr is not '':
			warehouseResults = models.Warehouse.objects.filter(w_name__regex="{}".format(warehouseStr))

		context = {
		'itemStr': itemStr, 
		'warehouseStr':warehouseStr, 
		'itemRecords': list(itemResults), 
		'warehouseRecords': list(warehouseResults)
		}

		return context


def loadSavedItem(request):

	if request.method == 'POST':

		# Get the filled values
		requestedQty 		= request.POST.get('Quantity', '')
		requestedItem 		= request.POST.get('ItemName', '')
		requestedWarehouse 	= request.POST.get('Warehouse', '')
		requestedLine 		= request.POST.get('LineType', '')
		if requestedQty != '':
			requestedQty = int(requestedQty)

		return requestedQty, requestedItem, requestedWarehouse, requestedLine


def keepSavedItem(**kwargs):

	context = {}

	if 'requestedItem' in kwargs:

		if kwargs['requestedItem'] != '':

			itemStr = models.Item.objects.get(i_id=kwargs['requestedItem'])
			context['ItemNameShown'] = '<div class="itemStyle"><div>{}</div><div>Price : {}</div></div>'.format(
				itemStr.i_name,
				itemStr.i_price
				)
			context['ItemNameVal'] = itemStr.i_id

	if 'requestedWarehouse' in kwargs:

		if kwargs['requestedWarehouse'] != '':

			WarehouseShownStr = models.Warehouse.objects.get(w_id=kwargs['requestedWarehouse'])
			context['WarehouseShown'] = '<div class="itemStyle"><div>{}</div><div>{}, {}, {}</div></div>'.format(
				WarehouseShownStr.w_name,
				WarehouseShownStr.w_street,
				WarehouseShownStr.w_city,
				WarehouseShownStr.w_country)
			context['WarehouseVal'] = WarehouseShownStr.w_id

	if 'requestedQty' in kwargs:
		if kwargs['requestedQty'] != '':
			context['QuantityShown'] = kwargs['requestedQty']

	if 'requestedLine' in kwargs:
		context['lineTypeShown'] = kwargs['requestedLine']

	return context




def checkOrder(request):

	if request.method == 'POST':

		requestedQty = (request.POST.get('Quantity', ''))
		if requestedQty != '':
			requestedQty = int(requestedQty)
		requestedItem = request.POST.get('ItemName', '')
		requestedWarehouse = request.POST.get('Warehouse', '')
		requestedLine = request.POST.get('LineType', '')

		# Do a check first
		# Quantity has to be >0
		errorMessage = []
		# Item and warehouse have to be filled
		if requestedItem == '':
			errorMessage += ['Item has not been chosen']
		if requestedWarehouse == '':
			errorMessage += ['Please choose warehouse']
		if requestedQty == '':
			errorMessage += ['Please enter item quantity']
		if requestedQty == 0:
			errorMessage += ['Quantity has to be more than 0']

	return errorMessage

