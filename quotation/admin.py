from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from django import forms

# Register your models here.
from .models import (
	PriceUnit,
	Animal,
	Specie,
	Incoterm,
	FreezingMethod,
	ProcessingMethod,
	HarvestingMethod,
	Supplier,
	CatchType,
	Currency,
	Country,
	Port,
	Scientificname,
	Quotation,
	SizePrice
)

class QuotationAdminArea(admin.AdminSite):
	site_header = 'Quotation Admin Area'

admin.site = QuotationAdminArea(name='QuotationAdmin')

class EditLinkInline(object):
	def box_details(self,instance):
		url = reverse(
			f"admin:{instance._meta.app_label}_{instance._meta.model_name}_change",
			args=[instance.pk]
		)
		print(f'instance: {instance}')
		if instance.price_unit_id == 3:
			link = mark_safe('<a href="{u}">Details</a>'.format(u=url))
			return link
		else:
			return ""

# class SizePriceForm( forms.ModelForm):
# 	def __init__(self, *args, **kwargs):
# 		super(SizePriceForm, self).__init__( *args, **kwargs)

# 	class Meta:
# 		model = SizePrice
# 		exclude = ('create_by',)
# 		readonly_fields = ('edit',)

class SizePriceInline(EditLinkInline,admin.TabularInline):
	model = SizePrice
	# extra = 3
	fields = ['size','price','price_unit','currency','box_details']
	#form = SizePriceForm
	extra = 3
	readonly_fields = ('box_details',)


class SpecieInline(admin.TabularInline):
	fields = ['name']
	model = Specie
	extra = 1

class PortInline(admin.TabularInline):
	model = Port
	extra = 1

class IncotermAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ['name', 'description']

    def save_model(self, request, obj, form, change):
      obj.create_by = request.user
      return super().save_model(request, obj, form, change)

class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ['name', 'code']

    inlines = [PortInline]


class FreezingMethodAdmin(admin.ModelAdmin):
	fields = ['name']

	def save_model(self, request, obj, form, change):
		obj.create_by = request.user
		return super().save_model(request, obj, form, change)

class ProcessingMethodAdmin(admin.ModelAdmin):
	fields = ['name']

	def save_model(self, request, obj, form, change):
		obj.create_by = request.user
		return super().save_model(request, obj, form, change)

class HarvestingMethodAdmin(admin.ModelAdmin):
	fields = ['name']

	def save_model(self, request, obj, form, change):
		obj.create_by = request.user
		return super().save_model(request, obj, form, change)

class CatchTypeMethodAdmin(admin.ModelAdmin):
	fields = ['name']

	def save_model(self, request, obj, form, change):
		obj.create_by = request.user
		return super().save_model(request, obj, form, change)

class PriceUnitMethodAdmin(admin.ModelAdmin):
	fields = ['name']

	def save_model(self, request, obj, form, change):
		obj.create_by = request.user
		return super().save_model(request, obj, form, change)

class SupplierAdmin(admin.ModelAdmin):
	fields = ['name']

	def save_model(self, request, obj, form, change):
		obj.create_by = request.user
		return super().save_model(request, obj, form, change)

class AnimalAdmin(admin.ModelAdmin):
	fields = ['name']
	inlines = [SpecieInline]

	def save_model(self, request, obj, form, change):
		obj.create_by = request.user
		return super().save_model(request, obj, form, change)

	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for instance in instances:
			instance.create_by = request.user
			instance.save()
			formset.save()



class QuotationAdmin(admin.ModelAdmin):
	fieldsets = [
		('',{'fields':['recieved_date']}),
		('Product Information', {'fields':['specie','product_image','origin','processing_method','harvesting_method','freezing_method','catch_type','packing']}),
		('Quotation Information', {'fields':['container_quantity','incoterm','supplier','tax','shipped_from','destination']}),
		('',{'fields':['note']})
	]
	list_display = ['specie','processing_method','harvesting_method','freezing_method','origin','destination','recieved_date']
	inlines = [SizePriceInline]
	search_fields = ['specie', 'origin', 'destination']

	def save_model(self, request, obj, form, change):
		obj.create_by = request.user
		return super().save_model(request, obj, form, change)

	def save_formset(self, request, form, formset, change):
		instances = formset.save(commit=False)
		for instance in instances:
			instance.create_by = request.user
			instance.save()
			formset.save()

admin.site.register(Country,CountryAdmin)
admin.site.register(Port)
admin.site.register(Animal,AnimalAdmin)
admin.site.register(Specie)
admin.site.register(Supplier,SupplierAdmin)
admin.site.register(CatchType,CatchTypeMethodAdmin)
admin.site.register(Currency)
admin.site.register(PriceUnit,PriceUnitMethodAdmin)
admin.site.register(Incoterm,IncotermAdmin)
admin.site.register(FreezingMethod,FreezingMethodAdmin)
admin.site.register(ProcessingMethod,ProcessingMethodAdmin)
admin.site.register(HarvestingMethod,HarvestingMethodAdmin)
admin.site.register(Quotation,QuotationAdmin)
admin.site.register(SizePrice)

