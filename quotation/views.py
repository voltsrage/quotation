from django.shortcuts import render,redirect,get_object_or_404
from django.core.paginator import Paginator
from django.http import HttpResponse,Http404
from django.urls import reverse
from django.forms.models import modelformset_factory
from .models import Quotation,SizePrice,SizePriceBoxNetWeight,Supplier
from .forms import QuotationForm,SizePriceForm,SizeFormSet,SupplierForm
from django.contrib import messages
from django.views.generic import ListView
from django.core.serializers import serialize
import json
from django.http import JsonResponse
from django.views.generic.edit import (
    CreateView, UpdateView
)
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

def detailQuotation(request, id=None):
	hx_url = reverse("quotation:hx-detail", kwargs={"id":id})
	context = {
		"hx_url" :hx_url
	}
	return render(request,'quotations/details.html',context)

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

def listQuotation(request):
	obj_list = Quotation.objects.all()
	paginator = Paginator(obj_list,10)
	page = request.GET.get('page')
	data = paginator.get_page(page)
	context = {
		"obj_list":obj_list,
		"data":data,
	}
	return render(request,'quotations/list.html',context)

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
		print(f'sizeprices: {sizeprices}')
		for obj in formset.deleted_objects:
			obj.delete()
		for i,sizeprice in enumerate(sizeprices):
			sizeprice.quotation = self.object
			sizeprice.save()
			if formset[i].cleaned_data["net_weight_box"]:
				if(formset[i].cleaned_data["id"]):
					netweight = SizePriceBoxNetWeight.objects.filter(sizeprice__id = formset[i]["id"].value()).first()
					if netweight is not None:
						netweight.net_weight = formset[i].cleaned_data["net_weight_box"]
						netweight.save()
				else:
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