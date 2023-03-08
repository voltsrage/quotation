import faker.providers
import random
from django.core.management.base import BaseCommand
from faker import Faker
from quotation.models import Supplier,Quotation,SizePrice

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

		for _ in range(5000):
			quotation_id = random.randint(1,1000)
			create_by_id = 1
			currency_id = random.randint(1,5)
			price_unit_id = random.randint(1,4)
			size = fake.quotation_size()
			price = (round(random.uniform(0.99,19.99),2))
			SizePrice.objects.get_or_create(quotation_id=quotation_id,
				   create_by_id=create_by_id,
					 currency_id=currency_id,
					 price_unit_id=price_unit_id,
					 size=size,price=price)

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

