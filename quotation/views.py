from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.urls import reverse
from django.forms.models import modelformset_factory
from .models import Quotation,SizePrice
from .forms import QuotationForm,SizePriceForm,SizeFormSet
from django.contrib import messages
from django.views.generic import ListView
from django.views.generic.edit import (
    CreateView, UpdateView
)
# Create your views here.
def createQuotation(request):
	form = QuotationForm(request.POST or None)
	context = {
		"form" :form,
		"new_sizeprice_url":new_sizeprice_url
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
	print(hx_url)
	context = {
		"hx_url" :hx_url
	}
	return render(request,'quotations/details.html',context)

def detailQuotation_hx(request, id=None):
	print(id)
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
	for item in obj_list:
		print(item.specie)
	context = {
		"obj_list":obj_list
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
	print(f'form: {form}')
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
		for sizeprice in sizeprices:
			sizeprice.quotation = self.object
			sizeprice.save()

class QuotationCreate(QuotationInline, CreateView):

	def get_context_data(self, **kwargs):
		ctx = super(QuotationCreate, self).get_context_data(**kwargs)
		ctx['named_formsets'] = self.get_named_formsets()
		print(ctx)
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
        return {
            'sizeprices': SizeFormSet(self.request.POST or None, self.request.FILES or None, instance=self.object, prefix='sizeprices'),
        }

def delete_sizeprice(request, pk):
    try:
        sizeprice = SizePrice.objects.get(id=pk)
    except SizePrice.DoesNotExist:
        messages.success(
            request, 'Object Does not exit'
            )
        return redirect('quotations:update_quotation', pk=sizeprice.quotation.id)

    sizeprice.delete()
    messages.success(
            request, 'sizeprice deleted successfully'
            )
    return redirect('quotations:update_quotation', pk=sizeprice.quotation.id)