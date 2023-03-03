from django.db import models
from django.conf import settings
from django.urls import reverse

# Create your models here.
class LogInfo(models.Model):
    create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING
		)
    create_at = models.DateTimeField(auto_now_add=True)
    update_by = models.ForeignKey(
					settings.AUTH_USER_MODEL,
					on_delete=models.DO_NOTHING
				)
    update_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class CatchType(models.Model):
	"""Create a model for the time fishes caught"""

	name = models.CharField(max_length=100)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name




class Currency(models.Model):
	"""Create a model for currencies"""

	name = models.CharField(max_length=100)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]
		verbose_name_plural = ("Currencies")

	def __str__(self):
			 return self.name

class Country(models.Model):
	"""Create a model for countries"""

	name = models.CharField(max_length=100)
	code = models.CharField(max_length=5, blank=True, null=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]
		verbose_name_plural = ("Countries")

	def __str__(self):
			 return self.name

class Port(models.Model):
	"""Create a model for countries"""

	name = models.CharField(max_length=100)
	country = models.ForeignKey(Country,on_delete=models.SET_NULL, blank=True, null=True)
	country_name = models.CharField(max_length=100, blank=True, null=True)
	latlong = models.CharField(max_length=100)
	telephone = models.CharField(max_length=50, blank=True, null=True)
	web = models.URLField(max_length=100, blank=True, null=True)
	code = models.CharField(max_length=100)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name

class Incoterm(models.Model):
	"""Create a model for incoterms"""

	name = models.CharField(max_length=100, unique=True)
	description = models.CharField(max_length=250, blank=True, null=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name

class PriceUnit(models.Model):
	"""Create a model for price units"""

	name = models.CharField(max_length=100, unique=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name

class FreezingMethod(models.Model):
	"""Create a model for freezing methods"""

	name = models.CharField(max_length=100, unique=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name

class HarvestingMethod(models.Model):
	"""Create a model for harvesting methods"""

	name = models.CharField(max_length=100, unique=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name

class ProcessingMethod(models.Model):
	"""Create a model for processing methods"""

	name = models.CharField(max_length=100, unique=True)
	note = models.TextField(blank=True, null=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name

class Animal(models.Model):
	"""Create a model for animals"""

	name = models.CharField(max_length=100, unique=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name

class Specie(models.Model):
	"""Create a model for species"""

	name = models.CharField(max_length=100, unique=True)
	animal = models.ForeignKey(Animal,on_delete=models.CASCADE)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]
		verbose_name_plural = ("Species")

	def __str__(self):
			 return self.name

class Scientificname(models.Model):
	"""Create a model for scientific names of animals"""

	name = models.CharField(max_length=100, unique=True)
	specie = models.ForeignKey(Specie,on_delete=models.CASCADE)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name


class Supplier(models.Model):
	"""Create a model for incoterms"""

	name = models.CharField(max_length=100, unique=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["name"]

	def __str__(self):
			 return self.name

class Quotation(models.Model):
	"""Create a model for incoterms"""

	destination = models.ForeignKey(Port, on_delete=models.SET_NULL, blank=True, null=True)
	shipped_from = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='shipped_from')
	origin = models.ForeignKey(Country, on_delete=models.SET_NULL, blank=True, null=True, related_name='origin')
	recieved_date = models.DateField(blank=True, null=True)
	specie = models.ForeignKey(Specie, on_delete=models.SET_NULL, blank=True, null=True)
	processing_method = models.ForeignKey(ProcessingMethod, on_delete=models.SET_NULL, blank=True, null=True)
	harvesting_method = models.ForeignKey(HarvestingMethod, on_delete=models.SET_NULL, blank=True, null=True)
	freezing_method = models.ForeignKey(FreezingMethod, on_delete=models.SET_NULL, blank=True, null=True)
	catch_type = models.ForeignKey(CatchType, on_delete=models.SET_NULL, blank=True, null=True)
	product_image = models.ImageField(upload_to='quotations/products', blank=True, null=True)
	supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
	incoterm = models.ForeignKey(Incoterm,on_delete=models.SET_NULL, blank=True, null=True)
	packing = models.CharField(max_length=150)
	tax = models.IntegerField()
	note = models.TextField(blank=True, null=True)
	container_quantity = models.DecimalField(max_digits=4,decimal_places=2,blank=True, null=True)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	def get_absolute_url(self):
		return reverse('quotation:detail', kwargs={'id':self.id})

	def get_hx_url(self):
		return reverse('quotation:hx-detail', kwargs={'id':self.id})

	def get_edit_url(self):
		return reverse('quotation:edit', kwargs={'id':self.id})

	def get_formset_edit_url(self):
		return reverse('quotation:update_quotation', kwargs={'pk':self.id})

	def get_sizeprize_children(self):
		return self.sizeprice_set.all()

	def __str__(self):
			 return f'{self.specie}-{self.origin}-{self.destination}'


class SizePrice(models.Model):
	"""Create a model for scientific names of animals"""

	size = models.CharField(max_length=20)
	price = models.DecimalField(decimal_places=2,max_digits=10)
	price_unit = models.ForeignKey(PriceUnit, on_delete=models.SET_NULL, blank=True, null=True)
	currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, blank=True, null=True)
	quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE)
	create_by = models.ForeignKey(
			settings.AUTH_USER_MODEL,
			on_delete=models.DO_NOTHING,null=True, blank=True
		)
	create_at = models.DateTimeField(auto_now_add=True)

	def get_hx_edit_url(self):
		kwargs = {
			"parent_id": self.quotation.id,
			"id":self.id
		}
		print(kwargs)
		return reverse('quotation:hx-sizeprice-detail', kwargs=kwargs)

	def __str__(self):
		return f'{self.quotation}: {self.size} for {self.price}'