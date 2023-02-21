from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,Http404
from django.forms.models import modelformset_factory
from .models import Quotation,SizePrice
from .forms import QuotationForm,SizePriceForm
# Create your views here.
def createQuotation(request):
	form = QuotationForm(request.POST or None)
	SizePriceFormSet = modelformset_factory(SizePrice, form=SizePriceForm, extra=2)
	formset = SizePriceFormSet(request.POST or None)
	context = {
		"form" :form
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
	obj = get_object_or_404(Quotation, id=id)
	context = {
		"obj" :obj
	}
	return render(request,'quotations/details.html',context)


def updateQuotation(request, id=None):
	obj = get_object_or_404(Quotation, id=id)
	form = QuotationForm(request.POST or None, instance=obj)
	context = {
		"form" :form,
		"obj": obj
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