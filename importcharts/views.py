import pandas as pd
from django.shortcuts import render, redirect
from django.http import JsonResponse

# Create your views here.
def ImportChartListViewSet(request):

	context = {
	}
	return render(request,'importcharts/list.html',context)


def import_file(request):
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
				if 'shrimp' in item[3] | 'Shrimp' in item[3]:
					print('has_shrimp')
				elif 'salmon' in item[3] | 'Salmon' in item[3]:
					print('has_salmon')
				elif 'lobster' in item[3] | 'Lobster' in item[3]:
					print('has_lobster')
				elif 'Scallops' in item[3] | 'scallops' in item[3]:
					print('has_scallops')

				if "Viet Nam" in item[4]:
					item[4] = 'VietName'

				if(item[7] != 0):
					price_per_kg = item[5]*1000/item[7]
				else:
					price_per_kg = 0

				print(f'{item[0]},{item[3]}, {item[4]}, {round(price_per_kg,3)}')

			return JsonResponse({'success': True, 'list':my_list})

	return render(request, 'importcharts/list.html')