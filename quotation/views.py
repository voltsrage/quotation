from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse,Http404
from django.urls import reverse
from django.forms.models import modelformset_factory
from .models import *
from .forms import QuotationForm,SizePriceForm,SizeFormSet,SupplierForm,QuotationFilterForm
from django.contrib import messages
from django.views.generic import ListView
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import Avg,Max,Min,Sum,Count, Q,F,Case, Value, When,ExpressionWrapper, DecimalField
from decimal import Decimal
import datetime
from django.views.generic.edit import (
    CreateView, UpdateView
)
from django.contrib.auth.decorators import login_required


@login_required(login_url='user:loginUser')
# Create your views here.
def createQuotation(request):
	form = QuotationForm(request.POST or None)
	context = {
		"form" :form,
	}
	if form.is_valid():
		obj = form.save(commit=False)
		obj.create_by = request.user
		obj.save()
		redirect('quotations/list.html')
	if request.htmx:
		return render(request,"quotations/partials/forms.html",context)
	return render(request,'quotations/create.html',context)

@login_required(login_url='user:loginUser')
def detailQuotation(request, id=None):
	hx_url = reverse("quotation:hx-detail", kwargs={"id":id})
	context = {
		"hx_url" :hx_url
	}
	return render(request,'quotations/details.html',context)

@login_required(login_url='user:loginUser')
def deleteQuotation(request, id=None):
	try:
		obj = Quotation.objects.get(id=id)
	except:
		obj = None
	if obj is None:
		if request.htmx:
			return HttpResponse("Not Found")
		raise Http404
	if request.method == "POST":
		obj.delete()
		success_url = reverse('quotation:list')
		if request.htmx:
			headers = {
				'HX-Redirect': success_url
			}
			return HttpResponse("Success", headers=headers)
		return redirect(success_url)
	context = {
		"obj" :obj
	}
	return render(request,'quotations/delete.html',context)

# def deleteQuotation(request, id=None):
# 	obj = get_object_or_404(Quotation, id=id)
# 	print(obj)
# 	if request.method == "POST":
# 		print(f'obj delete: {obj}')
# 		obj.delete()
# 		success_url = reverse('quotation:list')
# 		return redirect(success_url)
# 	context = {
# 		"obj" :obj
# 	}
# 	return render(request,'quotations/delete.html',context)

@login_required(login_url='user:loginUser')
def detailQuotation_hx(request, id=None):
	if not request.htmx:
		raise Http404
	try:
		obj = Quotation.objects.get(id=id)
	except:
		obj = None
	if obj is None:
		return HttpResponse("Not Found.")
	context = {
		"obj" :obj
	}
	return render(request,'quotations/partials/details.html',context)

@login_required(login_url='user:loginUser')
def updateQuotation(request, id=None):
	obj = get_object_or_404(Quotation, id=id)
	form = QuotationForm(request.POST or None, instance=obj)
	new_sizeprice_url = reverse("quotation:hx-sizeprices-create", kwargs={"parent_id": obj.id})
	context = {

		"form" :form,
		"obj": obj,
		"new_sizeprice_url":new_sizeprice_url
	}
	if form.is_valid():
		form.save()
		context['message'] = 'Data saved!'
	if request.htmx:
		return render(request,"quotations/partials/forms.html",context)
	return render(request,'quotations/create.html',context)

@login_required(login_url='user:loginUser')
def listQuotation(request):

	selected_freezingMethods  = request.GET.getlist('freezingMethods[]')
	selected_origins  = request.GET.getlist('origins[]')
	selected_species  = request.GET.getlist('species[]')
	selected_destinations  = request.GET.getlist('destinations[]')
	selected_processingMethods   = request.GET.getlist('processingMethods[]')
	selected_harvestingMethods = request.GET.getlist('harvestingMethods[]', '')
	selected_startDate = request.GET.get('startDate', '')
	selected_endDate = request.GET.get('endDate', '')

	form = QuotationFilterForm(request.GET)

	obj_list = Quotation.objects.all()

	if selected_startDate:
		startDate = datetime.datetime.strptime(selected_startDate, '%Y-%m-%d').date()
		obj_list = obj_list.filter(recieved_date__gte=startDate)
	if selected_endDate:
		endDate = datetime.datetime.strptime(selected_endDate, '%Y-%m-%d').date()
		obj_list = obj_list.filter(recieved_date__lte=endDate)

	if len(selected_freezingMethods) > 0:
		obj_list = obj_list.filter(Q(freezing_method__in=selected_freezingMethods))

	if len(selected_origins) > 0:
		obj_list = obj_list.filter(Q(origin__in=selected_origins))

	if len(selected_species) > 0:
		obj_list = obj_list.filter(Q(specie__in=selected_species))

	if len(selected_destinations) > 0:
		obj_list = obj_list.filter(Q(destination__in=selected_destinations))

	if len(selected_processingMethods) > 0:
		obj_list = obj_list.filter(Q(processing_method__in=selected_processingMethods))

	if len(selected_harvestingMethods) > 0:
		obj_list = obj_list.filter(Q(harvesting_method__in=selected_harvestingMethods))


	pageSize = request.GET.get('pageSize')

	if pageSize is None:
		pageSize = 10

	paginator = Paginator(obj_list,pageSize)
	page = request.GET.get('page')
	data = paginator.get_page(page)

	context = {
		"obj_list":obj_list,
		"data":data,
		'form':form,
	}
	return render(request,'quotations/list.html',context)


@login_required(login_url='user:loginUser')
def detailSizePrice_update_hx_view(request, parent_id=None, id=None):

	if not request.htmx:
		raise Http404
	try:
		parent_obj = Quotation.objects.get(id=parent_id)
	except:
		parent_obj = None
	if parent_obj is None:
		return HttpResponse("Not Found.")

	instance = None
	if id is not None:
		try:
			instance = SizePrice.objects.get(quotation=parent_obj,id=id)
		except:
			instance = None
	form = SizePriceForm(request.POST or None, instance=instance)
	url = instance.get_hx_edit_url() if instance else reverse("quotation:hx-sizeprices-create", kwargs={"parent_id":parent_obj.id})
	# if instance:
	# 	url = instance.get_hx_edit_url()
	context = {
		'url':url,
		"obj" :instance,
		'form':form
	}
	if form.is_valid():

		new_obj = form.save(commit=False)
		if instance is None:
			new_obj.quotation = parent_obj
		new_obj.save()
		context['object'] = new_obj
		return render(request,'quotations/partials/sizeprice-inline.html',context)
	return render(request,'quotations/partials/sizeprice-form.html',context)


class QuotationInline():
	form_class = QuotationForm
	model = Quotation
	template_name = "quotations/quotation_create_or_update.html"

	def form_valid(self,form):
		named_formsets = self.get_named_formsets()
		if not all((x.is_valid() for x in named_formsets.values())):
			return self.render_to_response(self.get_context_data(form=form))

		self.object = form.save()

		#for every formset, attempt to find a specific formset save function
		#otherwise, just save

		for name, formset in named_formsets.items():
			formset_save_func = getattr(self,'formset_{0}_valid'.format(name), None )
			if formset_save_func is not None:
				formset_save_func(formset)
			else:
				formset.save()
		return redirect('quotation:list')

	def formset_sizeprices_valid(self, formset):
		sizeprices = formset.save(commit=False)
		for obj in formset.deleted_objects:
			obj.delete()
		for i,sizeprice in enumerate(sizeprices):
			sizeprice.quotation = self.object
			if sizeprice.currency_id == 1: #twd
				sizeprice.price_in_usd = round(sizeprice.price / Decimal(30.67),2)
			elif sizeprice.currency_id == 2: #usd
				sizeprice.price_in_usd = round(sizeprice.price / Decimal(1.00),2)
			elif sizeprice.currency_id == 3: #jpy
				sizeprice.price_in_usd = round(sizeprice.price / Decimal(132.33),2)
			elif sizeprice.currency_id == 4: #cny
				sizeprice.price_in_usd = round(sizeprice.price / Decimal(6.89),2)
			elif sizeprice.currency_id ==5: #eur
				sizeprice.price_in_usd = round(sizeprice.price / Decimal(0.94),2)
			sizeprice.save()
			if formset[i].cleaned_data["net_weight_box"]:
				if(formset[i].cleaned_data["id"]):
					netweight = SizePriceBoxNetWeight.objects.filter(sizeprice__id = formset[i]["id"].value()).first()
					if netweight is not None:
						if(sizeprice.price_unit_id == 3):
							netweight.net_weight = formset[i].cleaned_data["net_weight_box"]
							netweight.save()
						else:
							netweight.delete()
					else:
						if(sizeprice.price_unit_id == 3):
							SizePriceBoxNetWeight.objects.create(sizeprice=sizeprice,net_weight=formset[i].cleaned_data["net_weight_box"])
				else:
					if(sizeprice.price_unit_id == 3):
						SizePriceBoxNetWeight.objects.create(sizeprice=sizeprice,net_weight=formset[i].cleaned_data["net_weight_box"])
				#


class QuotationCreate(QuotationInline, CreateView):

	def get_context_data(self, **kwargs):
		ctx = super(QuotationCreate, self).get_context_data(**kwargs)
		ctx['supplierform'] = SupplierForm(self.request.POST or None)
		ctx['named_formsets'] = self.get_named_formsets()
		return ctx

	def get_named_formsets(self):
		if self.request.method == "GET":
			return {
				'sizeprices': SizeFormSet(prefix='sizeprices')
			}
		else:
			return {
				'sizeprices': SizeFormSet(self.request.POST or None, self.request.FILES or None, prefix='sizeprices')
			}


class QuotationUpdate(QuotationInline, UpdateView):

	def get_context_data(self, **kwargs):
			ctx = super(QuotationUpdate, self).get_context_data(**kwargs)
			ctx['named_formsets'] = self.get_named_formsets()
			return ctx

	def get_named_formsets(self):
			sizeprices =  SizeFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='sizeprices')
			quotation_id = self.object.id
			sizeprice_objs = Quotation.objects.get(id=quotation_id).sizeprices.all()
			sizeprice_objs_list = list(sizeprice_objs)
			for i,sizeprice in enumerate(sizeprices):
				if i < len(sizeprice_objs_list):
					id = sizeprice['id'].value()
					if sizeprice_objs.get(id=id).netweight.first():
						netweight = sizeprice_objs.get(id=id).netweight.first()
						sizeprice.fields['net_weight_box'].widget.attrs.update({'value':netweight})
				pass

			return {
					'sizeprices': sizeprices,
			}

@login_required(login_url='user:loginUser')
def delete_sizeprice(request, pk):
    try:
        sizeprice = SizePrice.objects.get(id=pk)
    except SizePrice.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('quotation:update_quotation', pk=sizeprice.quotation.id)

    sizeprice.delete()
    messages.success(
            request, 'sizeprice deleted successfully'
            )
    return redirect('quotation:update_quotation', pk=sizeprice.quotation.id)


@login_required(login_url='user:loginUser')
def add_supplier(request):
	if request.method == 'POST':
		form = SupplierForm(request.POST or None)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.create_by = request.user
			obj.save()
			return HttpResponse("Supplier saved successfully")
		else:
			return HttpResponse("Form is not valid")

@login_required(login_url='user:loginUser')
def add_supplier_reload_supplier_dropdown(request):
	"""Add new supplier then update droplist"""
	name = request.GET.get('name',None)
	supplier, created = Supplier.objects.get_or_create(name=name,create_by = request.user)
	suppliers = Supplier.objects.all()
	serialized_data = serialize("json", suppliers)
	serialized_data = json.loads(serialized_data)
	response = {
        'suppliers': serialized_data
    }
	return JsonResponse(response)

@login_required(login_url='user:loginUser')
@require_GET
def quotation_chart_data(request):
		supplier = request.GET.get('supplier', '')
		origin = request.GET.get('origin', '')
		destination = request.GET.get('destination', '')
		specie = request.GET.get('specie', '')
		incoterm = request.GET.get('incoterm', '')
		shipped_from = request.GET.get('shipped_from', '')
		startDate = request.GET.get('startDate', '')
		endDate = request.GET.get('endDate', '')

		queryset = Quotation.objects.all()

		if startDate:
			startDate = datetime.datetime.strptime(startDate, '%d/%m/%Y').date()
			queryset = queryset.filter(recieved_date__gte=startDate)
		if endDate:
			endDate = datetime.datetime.strptime(endDate, '%d/%m/%Y').date()
			queryset = queryset.filter(recieved_date__lte=endDate)

		if supplier:
				queryset = queryset.filter(supplier=supplier)

		if origin:
				queryset = queryset.filter(origin=origin)

		if destination:
				queryset = queryset.filter(destination=destination)

		if specie:
				queryset = queryset.filter(specie=specie)

		if incoterm:
				queryset = queryset.filter(incoterm=incoterm)

		if shipped_from:
				queryset = queryset.filter(shipped_from=shipped_from)

		data = queryset.values('recieved_date__year','recieved_date__month').annotate(
			avg_price=Avg(Case (
				When(sizeprices__price_unit_id=1, then=F("sizeprices__price_in_usd")),
				When(sizeprices__price_unit_id=2, then=F("sizeprices__price_in_usd")*Decimal(2.2)),
				When(sizeprices__price_unit_id=3, then=F("sizeprices__price_in_usd")/F("sizeprices__netweight__net_weight")),
				default=Decimal(0.0))
			)).order_by('recieved_date__year','recieved_date__month')

		labels = []
		for item in data:
			year = item['recieved_date__year']
			month = item['recieved_date__month']
			if month < 10:
				month = f'0{month}'
			labels.append(f'{year}-{month}')

		prices = [round(item['avg_price'],2) for item in data]

		return JsonResponse({
				'labels': labels,
				'prices': prices
		})

@login_required(login_url='user:loginUser')
def price_chart_data_multiple(request):
		selected_suppliers  = request.GET.getlist('suppliers[]')
		selected_origins  = request.GET.getlist('origins[]')
		selected_species  = request.GET.getlist('species[]')
		selected_incoterms  = request.GET.getlist('incoterms[]')
		selected_years   = request.GET.getlist('years[]')
		selected_period = request.GET.get('period', '')
		selected_unit = request.GET.get('unit', '')
		selected_currency = request.GET.get('currency', '')

		price_conversion = 1
		print(selected_currency)
		if selected_currency == '1': #twd
			price_conversion = Decimal(30.67)
		elif selected_currency == '2': #usd
			price_conversion = Decimal(1.00)
		elif selected_currency == '3': #jpy
			price_conversion = Decimal(132.33)
		elif selected_currency == '4': #cny
			price_conversion = Decimal(6.89)
		elif selected_currency =='5': #eur
			price_conversion = Decimal(0.94)

		# price_conversion = Case(
		# 	When(sizeprices__currency_id=1, then=Value(Decimal(30.67))),
		# 	When(sizeprices__currency_id=2, then=Value(Decimal(1.00))),
		# 	When(sizeprices__currency_id=3, then=Value(Decimal(132.33))),
		# 	When(sizeprices__currency_id=4, then=Value(Decimal(6.89))),
		# 	When(sizeprices__currency_id=5, then=Value(Decimal(0.98)))
		# )

		if selected_unit == 'kg':
			avg_price = Avg(Case (
									When(sizeprices__price_unit_id=1, then=F("sizeprices__price_in_usd")),
									When(sizeprices__price_unit_id=2, then=F("sizeprices__price_in_usd")*Decimal(2.2)),
									When(sizeprices__price_unit_id=3, then=F("sizeprices__price_in_usd")/F("sizeprices__netweight__net_weight")),
									default=Decimal(0.0))
								)
		elif selected_unit == 'lb':
			avg_price = Avg(Case (
									When(sizeprices__price_unit_id=1, then=F("sizeprices__price_in_usd")/Decimal(2.2)),
									When(sizeprices__price_unit_id=2, then=F("sizeprices__price_in_usd")),
									When(sizeprices__price_unit_id=3, then=(F("sizeprices__price_in_usd")/F("sizeprices__netweight__net_weight"))/Decimal(2.2)),
									default=Decimal(0.0))
								)

		years_filter = Quotation.objects.filter(
			recieved_date__year__in=selected_years
			)

		if len(selected_suppliers) > 0:
			years_filter = years_filter.filter(Q(supplier__in=selected_suppliers))

		if len(selected_origins) > 0:
			years_filter = years_filter.filter(Q(origin__in=selected_origins))

		if len(selected_species) > 0:
			years_filter = years_filter.filter(Q(specie__in=selected_species))

		if len(selected_incoterms) > 0:
			years_filter = years_filter.filter(Q(incoterm__in=selected_incoterms))

		prices = years_filter
		datasets = []
		dataset_borderColors = ['rgba(0,110,185, 1)',
		    'rgba(242,108,82, 1)',
				'rgba(0,48,70, 1)',
				'rgba(0, 125, 137, 1)',
				'rgba(255,205,52, 1)',
				'rgba(63,191,176, 1)',
				'rgba(162,38,21, 1)',
				'rgba(34,192,241, 1)',
				'rgba(171,127,25, 1)',
				'rgba(236,233,36, 1)',
				'rgba(115,184,101, 1)',
				'rgba(95,100,106, 1)',]

		dataset_backgroundColors = ['rgba(0,110,185, 0.1)',
		    'rgba(242,108,82, 0.1)',
				'rgba(0,48,70, 0.1)',
				'rgba(0, 125, 137, 0.1)',
				'rgba(255,205,52, 0.1)',
				'rgba(63,191,176, 0.1)',
				'rgba(162,38,21, 0.1)',
				'rgba(34,192,241, 0.1)',
				'rgba(171,127,25, 0.1)',
				'rgba(236,233,36, 0.1)',
				'rgba(115,184,101, 0.1)',
				'rgba(95,100,106, 0.1)']

		for i,year in enumerate(selected_years):
			prices_year = prices.filter(recieved_date__year=year)
			data = []

			if selected_period == 'mtn':
				for month in range(1, 13):
						prices_month = prices_year.filter(recieved_date__month=month)
						if prices_month.exists():
							average_price = prices_month.aggregate(
								avg_price=avg_price * price_conversion)['avg_price']

							data.append(round(average_price, 2))
						else:
								data.append(0)

			elif selected_period == 'wk':
				for week in range(1, 53):
						prices_week = prices_year.filter(recieved_date__week=week)
						if prices_week.exists():
							average_price = prices_week.aggregate(
								avg_price=avg_price* price_conversion)['avg_price']

							data.append(round(average_price, 2))
						else:
								data.append(0)

			elif selected_period == 'qtr':
				for quarter in range(1, 5):
						prices_quarter = prices_year.filter(recieved_date__quarter=quarter)
						if prices_quarter.exists():
							average_price = prices_quarter.aggregate(
								avg_price=avg_price* price_conversion)['avg_price']

							data.append(round(average_price, 2))
						else:
								data.append(0)

			dataset = {
						'label': str(year),
						'data': data,
						'borderColor': dataset_borderColors[i],
						'backgroundColor': dataset_backgroundColors[i]
				}
			datasets.append(dataset)

		labels = []
		if selected_period == 'mtn':
			labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
		elif selected_period == 'wk':
			labels = []
			for week in range(1, 53):
				labels.append(f'Wk{week}')
		elif selected_period == 'qtr':
			labels = ['Qtr1', 'Qtr2', 'Qtr3', 'Qtr4']

		data = {
				'labels': labels,
				'datasets': datasets
		}
		options = {
				'scales': {
						'yAxes': [{
								'ticks': {
										'beginAtZero': True
								}
						}]
				}
		}

		return JsonResponse({
			'data': data, 'options': options
		})

