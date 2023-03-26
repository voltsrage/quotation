import pandas as pd
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from .models import Import
from django.db.models import Avg,Max,Min,Sum,Count, Q,F,Case, Value, When,ExpressionWrapper, DecimalField
from django.db import IntegrityError
from quotation.models import Country,Animal

# Create your views here.
def ImportChartListViewSet(request):
	imports = Import.objects.all()
	total_weight_tons_per_animal_ytd =Animal.objects.raw('''SELECT Id ,NAME, SUM(total_weight) as total_weight FROM
				(SELECT A.Id,A.name, SUM(coalesce(I.total_weight_tons,0)) total_weight
				FROM public.quotation_animal A
				LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
				WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now())
				GROUP BY A.Id,A.name
				UNION
				SELECT A.Id,A.name, 0 FROM public.quotation_animal A) S
				GROUP BY Id ,name
				ORDER BY NAME''')

	total_weight_tons_per_animal_ytd_last_year = Animal.objects.raw('''SELECT Id ,NAME, SUM(total_weight) as total_weight FROM
				(SELECT A.Id,A.name, SUM(coalesce(I.total_weight_tons,0)) total_weight
				FROM public.quotation_animal A
				LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
				WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now()) - 1  AND
					EXTRACT (MONTH FROM I.month) <= EXTRACT(MONTH FROM now())
				GROUP BY A.Id,A.name
				UNION
				SELECT A.Id,A.name, 0 FROM public.quotation_animal A) S
				GROUP BY Id ,name
				ORDER BY NAME''')

	total_weight_tons_per_animal_month =Animal.objects.raw('''SELECT Id ,NAME, SUM(total_weight) as total_weight FROM
				(SELECT A.Id,A.name, SUM(coalesce(I.total_weight_tons,0)) total_weight
				FROM public.quotation_animal A
				LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
				WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now())  AND
					EXTRACT (MONTH FROM I.month) = EXTRACT(MONTH FROM now()) -1
				GROUP BY A.Id,A.name
				UNION
				SELECT A.Id,A.name, 0 FROM public.quotation_animal A) S
				GROUP BY Id ,name
				ORDER BY NAME''')

	animal_month = []
	for animal in total_weight_tons_per_animal_ytd:
		animal_month.append({
			'id':animal.id,
			'name':animal.name,
			'total_weight':animal.total_weight
		})

	animal_month_month = []
	for animal in total_weight_tons_per_animal_month:
		animal_month_month.append({
			'name':animal.name,
			'total_weight':animal.total_weight
		})

	animal_month_last_year = []
	for animal in total_weight_tons_per_animal_ytd_last_year:
		animal_month_last_year.append({
			'id':animal.id,
			'name':animal.name,
			'total_weight':animal.total_weight
		})
	pageSize = request.GET.get('pageSize')

	if pageSize is None:
		pageSize = 10

	paginator = Paginator(imports,pageSize)
	page = request.GET.get('page')
	data = paginator.get_page(page)
	print(animal_month_month)
	context = {
				"data":data,
				'total_weight_tons_per_animal_month':animal_month_month,
				'total_weight_tons_per_animal_ytd':animal_month,
				'total_weight_tons_per_animal_ytd_last_year':animal_month_last_year,
			}
	return render(request,'importcharts/list.html',context)

def get_current_month_weight(request):
	total_weight_tons_per_animal_month =Animal.objects.raw('''SELECT Id ,NAME, SUM(total_weight) as total_weight FROM
				(SELECT A.Id,A.name, SUM(coalesce(I.total_weight_tons,0)) total_weight
				FROM public.quotation_animal A
				LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
				WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now())  AND
					EXTRACT (MONTH FROM I.month) = EXTRACT(MONTH FROM now()) -1
				GROUP BY A.Id,A.name
				UNION
				SELECT A.Id,A.name, 0 FROM public.quotation_animal A) S
				GROUP BY Id ,name
				ORDER BY NAME''')

	total_weight_tons_per_animal_month_last_year = Animal.objects.raw('''SELECT Id ,NAME, SUM(total_weight) as total_weight FROM
				(SELECT A.Id,A.name, SUM(coalesce(I.total_weight_tons,0)) total_weight
				FROM public.quotation_animal A
				LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
				WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now()) - 1  AND
					EXTRACT (MONTH FROM I.month) = EXTRACT(MONTH FROM now()) - 1
				GROUP BY A.Id,A.name
				UNION
				SELECT A.Id,A.name, 0 FROM public.quotation_animal A) S
				GROUP BY Id ,name
				ORDER BY NAME''')

	animal_month = []
	for animal in total_weight_tons_per_animal_month:
		animal_month.append({
			'name':animal.name,
			'total_weight':animal.total_weight
		})

	animal_month_last_year = []
	for animal in total_weight_tons_per_animal_month_last_year:
		animal_month_last_year.append({
			'name':animal.name,
			'total_weight':animal.total_weight
		})

	context = {
				'total_weight_tons_per_animal_month':animal_month,
				'total_weight_tons_per_animal_month_last_year':animal_month_last_year
			}
	return JsonResponse(context)

def get_current_ytd_weight(request):
	total_weight_tons_per_animal_ytd =Animal.objects.raw('''SELECT Id ,NAME, SUM(total_weight) as total_weight FROM
				(SELECT A.Id,A.name, SUM(coalesce(I.total_weight_tons,0)) total_weight
				FROM public.quotation_animal A
				LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
				WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now())
				GROUP BY A.Id,A.name
				UNION
				SELECT A.Id,A.name, 0 FROM public.quotation_animal A) S
				GROUP BY Id ,name
				ORDER BY NAME''')

	total_weight_tons_per_animal_ytd_last_year = Animal.objects.raw('''SELECT Id ,NAME, SUM(total_weight) as total_weight FROM
				(SELECT A.Id,A.name, SUM(coalesce(I.total_weight_tons,0)) total_weight
				FROM public.quotation_animal A
				LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
				WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now()) - 1  AND
					EXTRACT (MONTH FROM I.month) <= EXTRACT(MONTH FROM now())
				GROUP BY A.Id,A.name
				UNION
				SELECT A.Id,A.name, 0 FROM public.quotation_animal A) S
				GROUP BY Id ,name
				ORDER BY NAME''')

	animal_month = []
	for animal in total_weight_tons_per_animal_ytd:
		animal_month.append({
			'name':animal.name,
			'total_weight':animal.total_weight
		})

	animal_month_last_year = []
	for animal in total_weight_tons_per_animal_ytd_last_year:
		animal_month_last_year.append({
			'name':animal.name,
			'total_weight':animal.total_weight
		})
	context = {
				'total_weight_tons_per_animal_ytd':animal_month,
				'total_weight_tons_per_animal_ytd_last_year':animal_month_last_year
			}
	return JsonResponse(context)

def import_file(request):
	data = Import.objects.all()
	if request.method == 'POST' and request.FILES['file']:
			file = request.FILES['file']
			if file.name.endswith('.xlsx'):
					df = pd.read_excel(file)
			elif file.name.endswith('.csv'):
					df = pd.read_csv(file)
			else:
					return render(request, 'error.html', {'error': 'File type not supported'})

			my_list = df.values.tolist()

			for i,item in enumerate(my_list):
				import_item = Import(
					commodity_code=item[2],
					production_description=item[3],
					total_price=item[5]*1000,
					total_weight_tons=item[6],
					total_weight_kg=item[7]
					)
				if 'shrimp' in item[3] or 'Shrimp' in item[3]:
					import_item.animal_id = 1
				elif 'salmon' in item[3] or 'Salmon' in item[3]:
					import_item.animal_id = 2
				elif 'lobster' in item[3] or 'Lobster' in item[3]:
					import_item.animal_id = 3
				elif 'Scallops' in item[3] or 'scallops' in item[3]:
					import_item.animal_id = 4
				elif 'halibut' in item[3] or 'Halibut' in item[3]:
					import_item.animal_id = 5
				elif 'Crab' in item[3] or 'crab' in item[3]:
					import_item.animal_id = 6

				if "Viet Nam" in item[4]:
					item[4] = 'Vietnam'

				if "Korea, Republic of" in item[4]:
					item[4] = 'Korea (South)'

				if "Russian Federation" in item[4]:
					item[4] = 'Russia'

				if "Islamic Republic of Iran" in item[4]:
					item[4] = 'Iran'

				if "Arab Emirates, United" in item[4]:
					item[4] = 'United Arab Emirates'

				if "Taiwan, ROC" in item[4]:
					item[4] = 'Taiwan'

				if "Federated States of Micronesia" in item[4]:
					item[4] = 'Micronesia'

				if "Korea, Democratic People's Republic of" in item[4]:
					item[4] = 'Korea (North)'

				if "Moldova, Republic of" in item[4]:
					item[4] = 'Moldova'

				if 'Türkiye' in item[4]:
					item[4] = 'Turkey'

				import_item.country_name = item[4]

				country = Country.objects.get(name=item[4])

				import_item.country = country

				if(item[7] != 0):
					price_per_kg = item[5]*1000/item[7]
				else:
					price_per_kg = 0

				import_item.price_per_kg = price_per_kg

				year = item[1].split('/')[0]
				month = item[1].split('/')[1]
				if int(month) < 10:
					month = f'0{month}'

				date = f'{year}-{month}-01'
				month_for_db = datetime.datetime.strptime(date, '%Y-%m-%d').date()

				import_item.month = month_for_db

				try:
					import_item.save()
				except IntegrityError as e:
					if 'unique constraint' in str(e.args):
						continue

			data = Import.objects.all().order_by('-month')
			paginator = Paginator(data,10)
			page = request.GET.get('page')
			data = paginator.get_page(page)
			context = {
				"data":data
			}
			return render(request, 'importcharts/list.html',context)

	return render(request, 'importcharts/list.html')

def tooltip_view(request, animal_id):
	isYtd = request.GET.get('isYtd')

	if isYtd == 'true':
		import_species_raw = Animal.objects.raw(f'''SELECT 1 as id, production_description, SUM(total_weight) as total_weight FROM
					(SELECT I.Id,I.animal_id,I.production_description, SUM(coalesce(I.total_weight_tons,0)) total_weight
					FROM public.quotation_animal A
					LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
					WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now())
					AND animal_id = {animal_id}
					GROUP BY I.Id,I.animal_id,I.production_description
					UNION
					SELECT A.Id,A.animal_id,A.production_description, 0 FROM public.importcharts_import A
					LEFT JOIN public.quotation_animal I ON A.animal_id = I.Id
					WHERE animal_id = {animal_id}) S
					GROUP BY production_description
					ORDER BY production_description''')
	else:
		import_species_raw = Animal.objects.raw(f'''SELECT 1 as id, production_description, SUM(total_weight) as total_weight FROM
					(SELECT I.Id,I.animal_id,I.production_description, SUM(coalesce(I.total_weight_tons,0)) total_weight
					FROM public.quotation_animal A
					LEFT JOIN public.importcharts_import I ON I.animal_id = A.Id
					WHERE EXTRACT (YEAR FROM I.month) = EXTRACT(YEAR FROM now())
					AND animal_id = {animal_id} AND
					EXTRACT (MONTH FROM I.month) = EXTRACT(MONTH FROM now()) -1
					GROUP BY I.Id,I.animal_id,I.production_description
					UNION
					SELECT A.Id,A.animal_id,A.production_description, 0 FROM public.importcharts_import A
					LEFT JOIN public.quotation_animal I ON A.animal_id = I.Id
					WHERE animal_id = {animal_id}) S
					GROUP BY production_description
					ORDER BY production_description''')


	species = []
	for specie in import_species_raw:
		species.append({
			'name':specie.production_description,
			'total_weight':specie.total_weight
		})
	animal = Animal.objects.get(id=animal_id)
	data = {
		'title':animal.name,
		'content':species
	}
	return JsonResponse(data)