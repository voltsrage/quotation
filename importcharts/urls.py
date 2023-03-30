from django.urls import path
from . import views

from .views import (
    ImportChartListViewSet,
    import_file,
    get_current_month_weight,
    get_current_ytd_weight,
    tooltip_view,
    importsAnimalSelect,
    importsDashboard,
		barchart_data,
    linechart_data,
    piechart_data,
    piechart_data_echart
)

app_name = 'importchart'
urlpatterns = [
	path('', ImportChartListViewSet, name='list'),
  path('import_file/', import_file, name='import_file'),
  path('get_current_month_weight/', get_current_month_weight, name='get_current_month_weight'),
  path('get_current_ytd_weight/', get_current_ytd_weight, name='get_current_ytd_weight'),
	path('tooltip/<int:animal_id>/', tooltip_view, name='tooltip'),
	path('importsAnimalSelect/', importsAnimalSelect, name='importsAnimalSelect'),
	path('importsDashboard//<int:animal_id>/', importsDashboard, name='importsDashboard'),
  path('barchart_data/', barchart_data, name='barchart_data'),
  path('linechart_data/', linechart_data, name='linechart_data'),
  path('piechart_data/', piechart_data, name='piechart_data'),
  path('piechart_data_echart/', piechart_data_echart, name='piechart_data_echart'),
]