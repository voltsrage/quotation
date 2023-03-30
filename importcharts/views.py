import pandas as pd
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from .models import Import
from .forms import ImportFilterForm
from django.db.models import Avg,Max,Min,Sum,Count, Q,F,Case, Value, When,ExpressionWrapper, DecimalField
from django.db import IntegrityError
from quotation.models import Country,Animal

# Create your views here.
def ImportChartListViewSet(request):
	form = ImportFilterForm(request.GET)

	selected_commodityCodes  = request.GET.getlist('commodityCodes[]')
	selected_months  = request.GET.getlist('months[]')
	selected_descriptions  = request.GET.getlist('descriptions[]')
	selected_countries  = request.GET.getlist('countries[]')

	imports = Import.objects.all()

	if len(selected_commodityCodes) > 0:
		imports = imports.filter(Q(commodity_code__in=selected_commodityCodes))

	if len(selected_months) > 0:
		imports = imports.filter(Q(month__in=selected_months))

	if len(selected_descriptions) > 0:
		imports = imports.filter(Q(production_description__in=selected_descriptions))

	if len(selected_countries) > 0:
		imports = imports.filter(Q(country__in=selected_countries))

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

	context = {
				"data":data,
				'total_weight_tons_per_animal_month':animal_month_month,
				'total_weight_tons_per_animal_ytd':animal_month,
				'total_weight_tons_per_animal_ytd_last_year':animal_month_last_year,
				'form':form
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

def importsAnimalSelect(request):
	context = {

	}
	return render(request,'importcharts/animalselect.html',context)

def importsDashboard(request,animal_id):
	descriptions = Import.objects.filter(animal=animal_id).order_by('production_description').values_list('production_description', flat=True).distinct()
	countries = Import.objects.filter(animal=animal_id).order_by('country_name').values_list('country','country_name').distinct()
	years = Import.objects.order_by('month__year').values_list('month__year', flat=True).distinct()

	min_date =  Import.objects.aggregate(min_dt=Min('month'))
	max_date =  Import.objects.aggregate(max_dt=Max('month'))

	date_range = {
		'min': min_date['min_dt'].strftime('%Y-%m-%d'),
		'max':max_date['max_dt'].strftime('%Y-%m-%d')
	}

	context = {
		'descriptions':descriptions,
		'countries':countries,
		'years':years,
		'date_range':date_range,
		'animal_id':animal_id
	}
	return render(request,'importcharts/dashboard.html',context)

def barchart_data(request):
	selected_countries = request.GET.getlist('countries[]')
	selected_years = request.GET.getlist('years[]')
	selected_descriptions = request.GET.getlist('descriptions[]')

	data = {
				'labels': selected_years,
				'datasets': []
		}

	dataset_borderColors = ['rgba(0,110,185, 1)',
				'rgba(242,108,82, 1)',
				'rgba(0,48,70, 1)']

	dataset_backgroundColors = ['rgba(0,110,185, 0.1)',
				'rgba(242,108,82, 0.1)',
				'rgba(0,48,70, 0.1)']

	for i, country in enumerate(selected_countries):
				dataset = {
						'label': Country.objects.get(pk=country).name,
						'data': [],
						'backgroundColor': dataset_backgroundColors[i % len(dataset_backgroundColors)],
						'borderColor': dataset_borderColors[i % len(dataset_borderColors)],
						'borderWidth': 1
				}
				for year in selected_years:
						total_weight = Import.objects.filter(country=country, month__year=year, production_description__in=selected_descriptions).aggregate(total_weight=Sum('total_weight_tons'))['total_weight']

						dataset['data'].append(total_weight if total_weight else 0)
				data['datasets'].append(dataset)

	return JsonResponse(data)

def linechart_data(request):
	selected_countries = request.GET.getlist('countries[]')
	selected_descriptions = request.GET.getlist('descriptions[]')
	startDate = request.GET.get('startDate', '')
	endDate = request.GET.get('endDate', '')


	queryset = Import.objects.all()

	if startDate:
			startDate = datetime.datetime.strptime(startDate, '%d/%m/%Y').date()
			queryset = queryset.filter(month__gte=startDate)
	if endDate:
			endDate = datetime.datetime.strptime(endDate, '%d/%m/%Y').date()
			queryset = queryset.filter(month__lte=endDate)

	if len(selected_countries) > 0:
			queryset = queryset.filter(Q(country__in=selected_countries))


	queryset = queryset.filter(Q(production_description__in=selected_descriptions))

	weights = queryset
	datasets = []
	dataset_borderColors = ['rgba(0,110,185, 1)',
			'rgba(242,108,82, 1)',
			'rgba(0,48,70, 1)',
			'rgba(0, 125, 137, 1)',
			'rgba(255,205,52, 1)',
			'rgba(63,191,176, 1)',
			'rgba(162,38,21, 1)',
			'rgba(34,192,241, 1)',
			'rgba(171,127,25, 1)',
			'rgba(236,233,36, 1)',
			'rgba(115,184,101, 1)',
			'rgba(95,100,106, 1)',]

	dataset_backgroundColors = ['rgba(0,110,185, 0.1)',
			'rgba(242,108,82, 0.1)',
			'rgba(0,48,70, 0.1)',
			'rgba(0, 125, 137, 0.1)',
			'rgba(255,205,52, 0.1)',
			'rgba(63,191,176, 0.1)',
			'rgba(162,38,21, 0.1)',
			'rgba(34,192,241, 0.1)',
			'rgba(171,127,25, 0.1)',
			'rgba(236,233,36, 0.1)',
			'rgba(115,184,101, 0.1)',
			'rgba(95,100,106, 0.1)']

	months_in_range = Import.objects.filter(Q(month__gte=startDate) & Q(month__lte=endDate)).order_by('month__year','month__month').distinct('month__year','month__month')


	for i,country in enumerate(selected_countries):
			weights_country = weights.filter(country=country)
			data = []
			labels = []
			for month in months_in_range:
				weights_month = weights_country.filter(month=month.month)
				labels.append(f'{month.month.strftime("%Y-%m")}')
				if weights_month.exists():
					total_weight = weights_month.aggregate(total_weight=Sum('total_weight_tons'))['total_weight']
					data.append(round(total_weight, 2))
				else:
					data.append(0)

			dataset = {
						'label': Country.objects.get(pk=country).name,
						'data': data,
						'borderColor': dataset_borderColors[i],
						'backgroundColor': dataset_backgroundColors[i]
				}
			datasets.append(dataset)
	data = {
				'labels': labels,
				'datasets': datasets
		}
	options = {
			'scales': {
					'yAxes': [{
							'ticks': {
									'beginAtZero': True
							}
					}]
			}
	}

	return JsonResponse({
			'data': data, 'options': options
		})

def piechart_data(request):
	selected_year = request.GET.get('year')
	selected_descriptions = request.GET.getlist('descriptions[]')
	animal_id = request.GET.get('animal_id')
	queryset = Import.objects.filter(animal=animal_id)

	if selected_year:
		queryset = queryset.filter(month__year=selected_year)
	else:
		queryset = queryset.filter(month__year=queryset.aggregate(max_year=Max('month__year'))['max_year'])

	if len(selected_descriptions) > 0:
		queryset = queryset.filter(Q(production_description__in=selected_descriptions))

	year_total_weight_years =  queryset.values('month__year').annotate(total_weight=Sum('total_weight_tons'))
	year_total_weight = year_total_weight_years.get(month__year=selected_year)['total_weight']
	queryset = queryset.values('month__year','country__name').annotate(total_weight=Sum('total_weight_tons')).order_by('month__year','country__name')

	data = []
	labels = []
	for item in queryset:
		percent = (item['total_weight'] * 100) / year_total_weight
		data.append(round(percent,2))
		labels.append(item['country__name'])

	datasets = []
	dataset = {
		'label':str(selected_year),
		'data':data,
    'hoverOffset': 4,
    'backgroundColor':[
    '#4E79A7',
    '#F28E2B',
    '#E15759',
    '#76B7B2',
    '#59A14F',
    '#EDC949',
    '#AF7AA1',
    '#FF9DA7',
    '#9C755F',
    '#BAB0AC',
    '#7F7F7F',
    '#CED1D6',
    '#B07AA1',
    '#FFB5B8',
    '#8C613C',
    '#BDC9E1',
    '#FFA384',
    '#9CB3D5',
    '#BEBBD8',
    '#D6B4A7',
    '#9C9E97',
    '#FDCDAC',
    '#B3E2CD',
    '#C6DBEF',
    '#FDB462',
    '#C2A5CF',
    '#FFCC99',
    '#8DD3C7',
    '#FFFFB3',
    '#80B1D3'
]
	}
	datasets.append(dataset)

	data = {
				'labels': labels,
				'datasets': datasets
		}

	return JsonResponse({'data':data})


def piechart_data_echart(request):
	selected_year = request.GET.get('year')
	selected_descriptions = request.GET.getlist('descriptions[]')
	animal_id = request.GET.get('animal_id')
	queryset = Import.objects.filter(animal=animal_id)

	if selected_year:
		queryset = queryset.filter(month__year=selected_year)
	else:
		queryset = queryset.filter(month__year=queryset.aggregate(max_year=Max('month__year'))['max_year'])

	if len(selected_descriptions) > 0:
		queryset = queryset.filter(Q(production_description__in=selected_descriptions))

	# year_total_weight_years =  queryset.values('month__year').annotate(total_weight=Sum('total_weight_tons'))
	# if year_total_weight_years:
	# 	year_total_weight = year_total_weight_years.get(month__year=selected_year)['total_weight']
	# else:
	# 	year_total_weight = 1
	queryset = queryset.values('month__year','country__name').annotate(total_weight=Sum('total_weight_tons')).order_by('month__year','country__name')

	seriesData = []
	labels = []
	for item in queryset:
		percent = item['total_weight']
		seriesData.append({'name':item['country__name'],'value':round(percent,2)})
		labels.append(item['country__name'])

	data = {
				'labels': labels,
				'seriesData': seriesData
		}

	return JsonResponse({'data':data})