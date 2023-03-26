from django.urls import path
from . import views

from .views import (
    ImportChartListViewSet,
    import_file,
    get_current_month_weight,
    get_current_ytd_weight,
    tooltip_view
)

app_name = 'importchart'
urlpatterns = [
	path('', ImportChartListViewSet, name='list'),
  path('import_file/', import_file, name='import_file'),
  path('get_current_month_weight/', get_current_month_weight, name='get_current_month_weight'),
  path('get_current_ytd_weight/', get_current_ytd_weight, name='get_current_ytd_weight'),
	path('tooltip/<int:animal_id>/', tooltip_view, name='tooltip'),
]