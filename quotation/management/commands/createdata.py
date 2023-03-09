import faker.providers
import random
from django.core.management.base import BaseCommand
from faker import Faker
from quotation.models import Supplier,Quotation,SizePrice,SizePriceBoxNetWeight
from django.db.models import Avg,Max,Min,Sum,Count

picture_list = [
	'quotations/products/freshwater-shrimp-species.jpg',
	'quotations/products/crystal-red-shrimp.jpg',
	'quotations/products/red-cherry-shrimp.jpg',
	'quotations/products/amano-shrimp.jpg',
	'quotations/products/tiger-shrimp.jpg',
	'quotations/products/blue-bolt-shrimp.jpg',
	'quotations/products/pinto-shrimp.jpg',
	'quotations/products/bamboo-wood-shrimp.jpg',
	'quotations/products/ghost-shrimp.jpg',
	'quotations/products/Baked Shrimp.png',
	'quotations/products/shrimps_PNG96469.png',
	'quotations/products/Freshwater-Aquarium-Shrimp.jpg',
	'quotations/products/shrimp-1482920644-2661955.png',
	'quotations/products/10329.jpg',
	'quotations/products/baked-stuffed-shrimp-wcrabmeat-and-ritz-crackers.jpg',
	'quotations/products/shrimp_nutritional_value.jpg'

]

size_list = [
	"U10", "U12", "U15", "16/20", "21/25", "26/30", "31/40", "41/50", "51/60",'31/35', "51/60", "61/70", "71/80", "110/130", "71/90", "91/120", "121/200", "200/300", "300/500"
]

class Provider(faker.providers.BaseProvider):
	def quotation_picture(self):
		return self.random_element(picture_list)

	def quotation_size(self):
		return self.random_element(size_list)

class Command(BaseCommand):
	help = "Command Information"

	def handle(self, *args, **kwargs):

		fake = Faker()

		fake.add_provider(Provider)

		get_all_quotations = Quotation.objects.all()
		#print(get_all_quotations)

		get_quotation_by_primary_key = Quotation.objects.get(pk=5)
		#print(get_quotation_by_primary_key)

		get_the_origin_of_quotation_with_id_5 = Quotation.objects.get(id=5).origin
		#print(get_the_origin_of_quotation_with_id_5)

		get_all_the_quotations_recd_in_year_2020 = Quotation.objects.filter(recieved_date__year=2020)
		#print(get_all_the_quotations_recd_in_year_2020)

		get_all_the_quotations_recd_in_year_2020_with_destination_starting_with_M = Quotation.objects.filter(recieved_date__year=2020).filter(destination__name__istartswith='M')
		#print(get_all_the_quotations_recd_in_year_2020_with_destination_starting_with_M)

		get_all_quotations_with_sizeprices_gte_10_dollars = Quotation.objects.filter(sizeprices__price__gte=10.00)
		#print(f'get_all_quotations_with_sizeprices_gte_10_dollars: {get_all_quotations_with_sizeprices_gte_10_dollars}')

		# get_first_ten_quotations = Quotation.objects.all()[:10]
		# print(f'get_first_ten_quotations: {get_first_ten_quotations}')

		# get_first_ten_quotations_ordered_by_destination = Quotation.objects.order_by('destination')[:10]
		# print(f'get_first_ten_quotations_ordered_by_destination: {get_first_ten_quotations_ordered_by_destination}')

		# get_ten_to_twenty_quotations = Quotation.objects.all()[10:20]
		# print(f'get_ten_to_twenty_quotations: {get_ten_to_twenty_quotations}')

		# get_quotation_with_sizeprice_netweight_gte_1 = Quotation.objects.filter(sizeprices__netweight__net_weight__gte=1.00)
		# print(f'get_quotation_with_sizeprice_netweight_gte_1: {get_quotation_with_sizeprice_netweight_gte_1}')

		get_top_10_suppliers_with_the_highest_price = Supplier.objects.annotate(supplier_max = Max('quotation__sizeprices__price')).order_by('-supplier_max')[:10]
		#print(f'test: {test}')

		for i,t in enumerate(get_top_10_suppliers_with_the_highest_price):
					print(f't{1}: {vars(get_top_10_suppliers_with_the_highest_price[i])}')

		# quotations = Quotation.objects.all()

		# for quote in quotations:
		# 	quote.recieved_date = fake.date_between(start_date='-10y',
    #                           end_date='today')
		# 	quote.save()

		### SizePriceBoxNetWeight Start ###

		# sizeprice_with_box = SizePrice.objects.filter(price_unit_id=3)

		# for sizeprice in sizeprice_with_box:
		# 	net_weight = (round(random.uniform(0.00,1.99),2))
		# 	SizePriceBoxNetWeight.objects.get_or_create(sizeprice=sizeprice,net_weight=net_weight)

		### SizePriceBoxNetWeight End ###

		### SizePrice Start ###

		# for _ in range(5000):
		# 	quotation_id = random.randint(1,1000)
		# 	create_by_id = 1
		# 	currency_id = random.randint(1,5)
		# 	price_unit_id = random.randint(1,4)
		# 	size = fake.quotation_size()
		# 	price = (round(random.uniform(0.99,19.99),2))
		# 	SizePrice.objects.get_or_create(quotation_id=quotation_id,
		# 		   create_by_id=create_by_id,
		# 			 currency_id=currency_id,
		# 			 price_unit_id=price_unit_id,
		# 			 size=size,price=price)

		### SizePrice End ###

		### Quotation Start ###

		# for _ in range(1000):
		# 	catch_type_id = random.randint(1,2)
		# 	create_by_id = 1
		# 	destination_id = random.randint(1,832)
		# 	freezing_method_id = random.randint(3,8)
		# 	harvesting_method_id = random.randint(1,2)
		# 	incoterm_id = random.randint(1,11)
		# 	origin_id = random.randint(1,171)
		# 	processing_method_id = random.randint(1,10)
		# 	specie_id = random.randint(1,20)
		# 	supplier_id = random.randint(1,25)
		# 	tax = random.randint(10,25)
		# 	container_quantity = random.randint(1,5)
		# 	shipped_from_id = random.randint(1,171)
		# 	note =fake.sentence(nb_words=15)
		# 	product_image = fake.quotation_picture()
		# 	recieved_date = fake.date_between()
		# 	packing = f'{random.randint(1,20)}KG x {random.randint(1,20)}B'
		# 	Quotation.objects.get_or_create(catch_type_id=catch_type_id,
		# 		   create_by_id=create_by_id,
		# 			 destination_id=destination_id,
		# 			 freezing_method_id=freezing_method_id,
		# 			 harvesting_method_id=harvesting_method_id,
		# 			 incoterm_id=incoterm_id,
		# 			 origin_id=origin_id,
		# 			 processing_method_id=processing_method_id,
		# 			 specie_id=specie_id,
		# 			 supplier_id=supplier_id,
		# 			 tax=tax,
		# 			 container_quantity=container_quantity,
		# 			 shipped_from_id=shipped_from_id,
		# 			 note=note,
		# 			 product_image=product_image,
		# 			 recieved_date=recieved_date,
		# 			 packing=packing)

		### Quotation End ###
