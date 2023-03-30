import faker.providers
import random
from django.core.management.base import BaseCommand
from faker import Faker
from quotation.models import Supplier,Quotation,SizePrice,SizePriceBoxNetWeight,Specie,Country,Port
from importcharts.models import *
from django.db.models import Avg,Max,Min,Sum,Count, Q,F,Case, Value, When,ExpressionWrapper, DecimalField
from django.db import connection
from decimal import Decimal
import datetime

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

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# # Total Quotations for each supplier

		# supplier_quotes = Supplier.objects.annotate(num_or_quotes=Count('quotation'))

		# for i,quote in enumerate(supplier_quotes):
		# 	print(f'{supplier_quotes[i].name} - {supplier_quotes[i].num_or_quotes}')

		# print()
		# print('-----------------------------------------------------------------------')
		# print()
		# # Total Quotations from each Specie

		# specie_quotes = Specie.objects.annotate(num_or_quotes=Count('quotation'))

		# for i,quote in enumerate(specie_quotes):
		# 	print(f'{specie_quotes[i].name} - {specie_quotes[i].num_or_quotes}')


		# print()
		# print('-----------------------------------------------------------------------')
		# print()
		# # Total Quotations for each Destination

		# destination_quotes = Port.objects.annotate(num_or_quotes=Count('quotation'))

		# for i,quote in enumerate(destination_quotes):
		# 	print(f'{destination_quotes[i].name} - {destination_quotes[i].num_or_quotes}')

		# """
		# 	[{'sql': 'SELECT "quotation_supplier"."id", "quotation_supplier"."name", "quotation_supplier"."create_by_id",
    # "quotation_supplier"."create_at", COUNT("quotation_quotation"."id") AS "num_or_quotes" FROM "quotation_supplier"
		# LEFT OUTER JOIN "quotation_quotation" ON ("quotation_supplier"."id" = "quotation_quotation"."supplier_id")
		# GROUP BY "quotation_supplier"."id"', 'time': '0.017'},

		# 	{'sql': 'SELECT "quotation_specie"."id", "quotation_specie"."name", "quotation_specie"."animal_id", "quotation_specie"."create_by_id",
		# "quotation_specie"."create_at", COUNT("quotation_quotation"."id") AS "num_or_quotes"
		# FROM "quotation_specie"
		# LEFT OUTER JOIN "quotation_quotation" ON ("quotation_specie"."id" = "quotation_quotation"."specie_id")
		# GROUP BY "quotation_specie"."id"', 'time': '0.007'},

		# {'sql': 'SELECT "quotation_port"."id", "quotation_port"."name", "quotation_port"."country_id", "quotation_port"."country_name",
		# 	"quotation_port"."latlong", "quotation_port"."telephone", "quotation_port"."web", "quotation_port"."code", "quotation_port"."create_by_id",
		# 	"quotation_port"."create_at", COUNT("quotation_quotation"."id") AS "num_or_quotes"
		# 	FROM "quotation_port"
		# 	LEFT OUTER JOIN "quotation_quotation" ON ("quotation_port"."id" = "quotation_quotation"."destination_id")
		# 		GROUP BY "quotation_port"."id"', 'time': '0.027'}]
		# """

		# print()
		# print('-----------------------------------------------------------------------')
		# print()
		# # Total Quotations with taxes greater than 15 for each species

		# above_15 = Count('quotation', filter=Q(quotation__tax__gt=15))
		# Specie_quotes = Specie.objects.annotate(above_15=above_15)

		# for i,quote in enumerate(Specie_quotes):
		# 	print(f'{Specie_quotes[i].name} - {Specie_quotes[i].above_15}')

		# """
		# [{'sql': 'SELECT "quotation_specie"."id", "quotation_specie"."name", "quotation_specie"."animal_id", "quotation_specie"."create_by_id",
		# "quotation_specie"."create_at", COUNT("quotation_quotation"."id")
		# FILTER (WHERE "quotation_quotation"."tax" > 15) AS "above_15"
		# FROM "quotation_specie"
		# LEFT OUTER JOIN "quotation_quotation" ON ("quotation_specie"."id" = "quotation_quotation"."specie_id")
		# GROUP BY "quotation_specie"."id"', 'time': '0.017'}]
		# """

		# print()
		# print('-----------------------------------------------------------------------')
		# print()
		# # Total Quotations with taxes greater than 15 for each shipped from country using related_name

		# above_15 = Count('shipped_from', filter=Q(shipped_from__tax__gt=15))
		# shipped_from_quotes = Country.objects.annotate(above_15=above_15)

		# for i,quote in enumerate(shipped_from_quotes):
		# 	print(f'{shipped_from_quotes[i].name} - {shipped_from_quotes[i].above_15}')
		#get_all_quotations = Quotation.objects.all()
		#print(get_all_quotations)

		#get_quotation_by_primary_key = Quotation.objects.get(pk=5)
		#print(get_quotation_by_primary_key)

		#get_the_origin_of_quotation_with_id_5 = Quotation.objects.get(id=5).origin
		#print(get_the_origin_of_quotation_with_id_5)

		#get_all_the_quotations_recd_in_year_2020 = Quotation.objects.filter(recieved_date__year=2020)
		#print(get_all_the_quotations_recd_in_year_2020)

		#get_all_the_quotations_recd_in_year_2020_with_destination_starting_with_M = Quotation.objects.filter(recieved_date__year=2020).filter(destination__name__istartswith='M')
		#print(get_all_the_quotations_recd_in_year_2020_with_destination_starting_with_M)

		#get_all_quotations_with_sizeprices_gte_10_dollars = Quotation.objects.filter(sizeprices__price__gte=10.00)
		#print(f'get_all_quotations_with_sizeprices_gte_10_dollars: {get_all_quotations_with_sizeprices_gte_10_dollars}')

		# get_first_ten_quotations = Quotation.objects.all()[:10]
		# print(f'get_first_ten_quotations: {get_first_ten_quotations}')

		# get_first_ten_quotations_ordered_by_destination = Quotation.objects.order_by('destination')[:10]
		# print(f'get_first_ten_quotations_ordered_by_destination: {get_first_ten_quotations_ordered_by_destination}')

		# get_ten_to_twenty_quotations = Quotation.objects.all()[10:20]
		# print(f'get_ten_to_twenty_quotations: {get_ten_to_twenty_quotations}')

		# get_quotation_with_sizeprice_netweight_gte_1 = Quotation.objects.filter(sizeprices__netweight__net_weight__gte=1.00)
		# print(f'get_quotation_with_sizeprice_netweight_gte_1: {get_quotation_with_sizeprice_netweight_gte_1}')

		#get_top_10_suppliers_with_the_highest_price = Supplier.objects.annotate(supplier_max = Max('quotation__sizeprices__price')).order_by('-supplier_max')[:10]

		#get_top_10_suppliers_with_the_loeest_price = Supplier.objects.annotate(supplier_max = Min('quotation__sizeprices__price')).order_by('supplier_max')[:10]
		#print(f'test: {test}')

		# for i,t in enumerate(get_top_10_suppliers_with_the_highest_price):
		# 			print(f't{1}: {vars(get_top_10_suppliers_with_the_highest_price[i])}')

		# print()

		# for i,t in enumerate(get_top_10_suppliers_with_the_loeest_price):
		# 			print(f't{1}: {vars(get_top_10_suppliers_with_the_loeest_price[i])}')


		## Or Statemens

		#get_or_statement = Supplier.objects.filter(name__startswith='Ma') | Supplier.objects.filter(name__startswith='E')

		#get_or_statement2 = Supplier.objects.filter(Q(name__startswith='Ma') | Q(name__startswith='E') )

		#get_supplier_who_not_start_with_ma = Supplier.objects.filter(~Q(name__startswith='Ma') )




		## And Statemens

		#get_or_statement = Supplier.objects.filter(name__startswith='Ma') & Supplier.objects.filter(name__startswith='E')

		#get_or_statement2 = Supplier.objects.filter(Q(name__startswith='Ma') & Q(name__startswith='E') )

		# use value list to get only specific columns from the list
		#get_supplier_value_list = Supplier.objects.all().values_list("name")

		#get_quotation_value_list = Quotation.objects.all().values_list("destination","supplier", 'tax' ,'recieved_date')

			# use value list to get only specific columns directly from the db

		# get_quotation_value_list = Quotation.objects.all().only("destination","supplier", 'tax' ,'recieved_date')
		# print(get_quotation_value_list)

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# get_kg_sizeprice = Quotation.objects.all()[:10]

		# get_kg_sizeprice = Quotation.objects.filter(Q(sizeprices__price_unit_id=3) | Q(sizeprices__price_unit_id=2) | Q(sizeprices__price_unit_id=1) ).annotate(
		# 	price_in_kg = Case(
		# 		When(sizeprices__price_unit_id=1, then='sizeprices__price'),
		# 		When(sizeprices__price_unit_id=2, then=ExpressionWrapper(F("sizeprices__price")*Decimal(2.2),output_field=DecimalField())),
		# 		When(sizeprices__price_unit_id=3, then=F('sizeprices__price')/F('sizeprices__netweight__net_weight')),
		# 	)
		# ).values('id','supplier','sizeprices__size','sizeprices__price','price_in_kg')[:10]
		# for y in get_kg_sizeprice:
		# 	list = [{
		# 					'quotation_id':y.id,
	  #   				 'supplier':y.supplier.name,
	  #   				 'destination':y.destination.name,
		# 					 'origin':y.origin.name,
		# 					 'sizeprice_id':x.id,
	  #   				 'size':x.size,
		# 					 'price_unit':x.price_unit.name,
		# 					 'original_price':x.price,
		# 					 'price_in_kg':x.price_in_kg(),
		# 					 'price_in_lb':x.price_in_lb()
		# 					 }
		# 					for x in y.sizeprices.all()[:10]]
		# 	for sizeprice in list:
		# 		print(sizeprice)

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# quotes_yearly = Quotation.objects.all().values('recieved_date__year').annotate(num_of_quotes=Count("id")).order_by('recieved_date__year')

		# print(quotes_yearly)

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# quotes_monthly = Quotation.objects.filter(recieved_date__year=2023).values('recieved_date__month').annotate(num_of_quotes=Count("id")).order_by('recieved_date__month')

		# print(quotes_monthly)

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# quotes_yearlY_monthly = Quotation.objects.all().values('recieved_date__year','recieved_date__month').annotate(num_of_quotes=Count("id")).order_by('recieved_date__year','recieved_date__month')

		# print(quotes_yearlY_monthly)

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# supplier_quotes_yearly = Quotation.objects.all().values('supplier__name','recieved_date__year').annotate(num_of_quotes=Count("id")).order_by('supplier','recieved_date__year')

		# print(supplier_quotes_yearly)

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# quotes_yearly = Quotation.objects.all().values('recieved_date__year').annotate(
		# 	num_of_quotes=Avg(Case (
		# 		When(sizeprices__price_unit_id=1, then=F("sizeprices__price")),
		# 		When(sizeprices__price_unit_id=2, then=F("sizeprices__price")*Decimal(2.2)),
		# 		When(sizeprices__price_unit_id=2, then=F("sizeprices__price")/F("sizeprices__netweight__net_weight")),
		# 		default=Decimal(0.0))
		# 	)
		# 	).order_by('recieved_date__year')

		# print(quotes_yearly)

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# quotes_by_specie_yearly = Quotation.objects.all().values('recieved_date__year','specie__name').annotate(
		# 	num_of_quotes=Avg(Case (
		# 		When(sizeprices__price_unit_id=1, then=F("sizeprices__price")),
		# 		When(sizeprices__price_unit_id=2, then=F("sizeprices__price")*Decimal(2.2)),
		# 		When(sizeprices__price_unit_id=2, then=F("sizeprices__price")/F("sizeprices__netweight__net_weight")),
		# 		default=Decimal(0.0))
		# 	)
		# 	).order_by('recieved_date__year','specie__id')

		# for quotes in quotes_by_specie_yearly:
		# 	print(quotes)




		# quotes_by_origin_specie_yearly = Quotation.objects.all().values('recieved_date__year','origin__name','specie__name').annotate(
		# 	num_of_quotes=Avg(Case (
		# 		When(sizeprices__price_unit_id=1, then=F("sizeprices__price")),
		# 		When(sizeprices__price_unit_id=2, then=F("sizeprices__price")*Decimal(2.2)),
		# 		When(sizeprices__price_unit_id=2, then=F("sizeprices__price")/F("sizeprices__netweight__net_weight")),
		# 		default=Decimal(0.0))
		# 	)
		# 	).order_by('recieved_date__year','origin__name','specie__name')

		# for quotes in quotes_by_origin_specie_yearly:
		# 	print(quotes)

		# # The average, max and min tax required on quotations

		# avg_tax = Quotation.objects.filter(specie__name='Amano Shrimp').aggregate(Avg('tax'), Max('tax'), Min('tax'))
		# print(avg_tax)

		# print()
		# print('-----------------------------------------------------------------------')
		# print()

		# # The get the supplier with the lowest price

		# min_price_each_supplier = Supplier.objects.aggregate(lowest_price=Min('quotation__sizeprices__price'))
		# print(min_price_each_supplier)

		#print(Specie.objects.all().values_list())

		print()
		print('-----------------------------------------------------------------------')
		print()

		# total_weight_tons_per_animal_month =Animal.objects.raw('''SELECT Id ,NAME, SUM(total_weight) as total_weight FROM
		# 		(SELECT A.Id,A.name, SUM(coalesce(I.total_weight_tons,0)) total_weight
		# 		FROM public.quotation_animal A
		# 		LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
		# 		WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now())  AND
		# 			EXTRACT (MONTH FROM I.month) = EXTRACT(MONTH FROM now()) -1
		# 		GROUP BY A.Id,A.name
		# 		UNION
		# 		SELECT A.Id,A.name, 0 FROM public.quotation_animal A) S
		# 		GROUP BY Id ,name
		# 		ORDER BY NAME''')
		# print(total_weight_tons_per_animal_month)
		# for thing in total_weight_tons_per_animal_month:
		# 	print(f'{thing.name} - {thing.total_weight}')

		tests = Import.objects.filter(animal=1).values('month__year','country__name').annotate(total_weight=Sum('total_weight_tons')).order_by('month__year','country__name')[:300]

		for test in tests:
			print(test)

		print()
		print(connection.queries)
		print()

		## Union Statemens

		# get_or_statement = Supplier.objects.filter(name__startswith='Ma').values("name").union(
		# 	 Supplier.objects.filter(name__startswith='E').values("name")
		# )

		# print(get_or_statement)
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
		# 	price_in_usd = round(price / Decimal(1),2)
		# 	if currency_id == 1: #twd
		# 		price_in_usd =  round(price / Decimal(30.67),2)
		# 	elif currency_id == 2: #usd
		# 		price_in_usd =  round(price / Decimal(1),2)
		# 	elif currency_id == 3: #jpy
		# 		price_in_usd =  round(price / Decimal(132.33),2)
		# 	elif currency_id == 4: #cny
		# 		price_in_usd =  round(price / Decimal(6.89),2)
		# 	elif currency_id ==5: #eur
		# 		price_in_usd =  round(price / Decimal(0.94),2)
		# 	SizePrice.objects.get_or_create(quotation_id=quotation_id,
		# 				create_by_id=create_by_id,
		# 				currency_id=currency_id,
		# 				price_unit_id=price_unit_id,
		# 				price_in_usd = price_in_usd,
		# 				size=size,
		# 				price=price)

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
