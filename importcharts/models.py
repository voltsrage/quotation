from django.db import models
from quotation.models import Country,Animal

# Create your models here.
class Import(models.Model):
	commodity_code = models.CharField(max_length=13)
	month = models.DateField(blank=True, null=True)
	animal = models.ForeignKey(Animal,on_delete=models.SET_NULL, blank=True, null=True)
	production_description = models.CharField(max_length=250)
	country = models.ForeignKey(Country,on_delete=models.SET_NULL, blank=True, null=True)
	country_name = models.CharField(max_length=50)
	total_price = models.DecimalField(max_digits=12,decimal_places=2)
	total_weight_tons = models.DecimalField(max_digits=7,decimal_places=2)
	total_weight_kg = models.DecimalField(max_digits=9,decimal_places=2)
	price_per_kg = models.DecimalField(max_digits=5,decimal_places=2)

	def __str__(self):
		return f'{self.country}-{self.production_description}-{self.total_price}'

	class Meta:
		unique_together  = ["commodity_code","month",'country','production_description']
