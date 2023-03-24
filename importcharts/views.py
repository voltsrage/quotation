import pandas as pd
import datetime
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.paginator import Paginator
from .models import Import
from django.db.models import Avg,Max,Min,Sum,Count, Q,F,Case, Value, When,ExpressionWrapper, DecimalField
from django.db import IntegrityError
from quotation.models import Country

# Create your views here.
def ImportChartListViewSet(request):
	imports = Import.objects.all()
	total_weight_tons_per_animal_ytd = imports.filter(month__year=datetime.date.today().year).values('animal__name').annotate(total_weight=Sum('total_weight_tons')).order_by('animal__name')
	total_weight_tons_per_animal_ytd_last_year = imports.filter(Q(month__year=datetime.date.today().year-1) &  Q(month__month__lte=datetime.date.today().month)).values('animal__name').annotate(total_weight=Sum('total_weight_tons')).order_by('animal__name')
	total_weight_tons_per_animal_month = imports.filter(Q(month__year=datetime.date.today().year) & Q(month__month=datetime.date.today().month-1)).values_list('animal__name').annotate(total_weight=Sum('total_weight_tons'))
	total_weight_tons_per_animal_month_last_year = imports.filter(Q(month__year=datetime.date.today().year-1) & Q(month__month=datetime.date.today().month-1)).values_list('animal__name').annotate(total_weight=Sum('total_weight_tons'))
	print(list(total_weight_tons_per_animal_ytd))
	print(list(total_weight_tons_per_animal_ytd_last_year))
	pageSize = request.GET.get('pageSize')

	if pageSize is None:
		pageSize = 10

	paginator = Paginator(imports,pageSize)
	page = request.GET.get('page')
	data = paginator.get_page(page)
	context = {
				"data":data,
				'total_weight_tons_per_animal_ytd':list(total_weight_tons_per_animal_ytd),
				'total_weight_tons_per_animal_ytd_last_year':list(total_weight_tons_per_animal_ytd_last_year),
				'total_weight_tons_per_animal_month':total_weight_tons_per_animal_month,
				'total_weight_tons_per_animal_month_last_year':total_weight_tons_per_animal_month_last_year
			}
	return render(request,'importcharts/list.html',context)


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

