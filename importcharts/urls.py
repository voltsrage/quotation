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
    piechart_data_echart,
    linechart_data_echarts,
    barchart_data_echarts,
    treemapchart_data_echarts,
)

app_name = 'importchart'
urlpatterns = [
	path('', ImportChartListViewSet, name='import_list'),
  path('import_file/', import_file, name='import_file'),
  path('get_current_month_weight/', get_current_month_weight, name='get_current_month_weight'),
  path('get_current_ytd_weight/', get_current_ytd_weight, name='get_current_ytd_weight'),
	path('tooltip/<int:animal_id>/', tooltip_view, name='tooltip'),
	path('importsAnimalSelect/', importsAnimalSelect, name='importsAnimalSelect'),
	path('importsDashboard//<int:animal_id>/', importsDashboard, name='importsDashboard'),
  path('barchart_data/', barchart_data, name='barchart_data'),
  path('barchart_data_echarts/', barchart_data_echarts, name='barchart_data_echarts'),
  path('piechart_data_echart/', piechart_data_echart, name='piechart_data_echart'),
  path('linechart_data_echarts/', linechart_data_echarts, name='linechart_data_echarts'),
  path('treemapchart_data_echarts/', treemapchart_data_echarts, name='treemapchart_data_echarts'),
]