from django.urls import path
from . import views

from .views import (
    ImportChartListViewSet,
    import_file
)

app_name = 'importchart'
urlpatterns = [
	path('', ImportChartListViewSet, name='list'),
  path('import_file/', import_file, name='import_file'),
]