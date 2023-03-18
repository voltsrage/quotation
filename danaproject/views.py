from django.shortcuts import render
from django.http import HttpResponse,Http404
from quotation.models import *


def dashboard(request):
	suppliers = Supplier.objects.all()
	origins = Country.objects.all()
	destinations = Port.objects.all()
	species = Specie.objects.all()
	incoterms = Incoterm.objects.all()
	shipped_froms = Country.objects.all()
	years = Quotation.objects.order_by('recieved_date__year').values_list('recieved_date__year', flat=True).distinct()
	context = {
		'suppliers':suppliers,
		'origins':origins,
		'destinations':destinations,
		'species':species,
		'incoterms':incoterms,
		'shipped_froms':shipped_froms,
		'years':years,
	}

	return render(request, 'dashboard.html', context)