from django.shortcuts import render
from django.http import HttpResponse,Http404
from django.db.models import Avg,Max,Min,Sum,Count, Q,F,Case, Value, When,ExpressionWrapper, DecimalField
import datetime
from quotation.models import *


def dashboard(request):
	suppliers = Supplier.objects.all()
	origins = Country.objects.all()
	destinations = Port.objects.all()
	species = Specie.objects.all()
	incoterms = Incoterm.objects.all()
	shipped_froms = Country.objects.all()
	years = Quotation.objects.order_by('recieved_date__year').values_list('recieved_date__year', flat=True).distinct()
	currencies = Currency.objects.all()


	min_date =  Quotation.objects.aggregate(min_dt=Min('recieved_date'))
	max_date =  Quotation.objects.aggregate(max_dt=Max('recieved_date'))

	date_range = {
		'min': min_date['min_dt'].strftime('%Y-%m-%d'),
		'max':max_date['max_dt'].strftime('%Y-%m-%d')
	}

	print(date_range)

	context = {
		'suppliers':suppliers,
		'origins':origins,
		'destinations':destinations,
		'species':species,
		'incoterms':incoterms,
		'shipped_froms':shipped_froms,
		'years':years,
		'date_range':date_range,
		'currencies':currencies
	}

	return render(request, 'dashboard.html', context)