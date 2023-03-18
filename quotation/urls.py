from django.urls import path
from . import views

from .views import (
	listQuotation,
	createQuotation,
	detailSizePrice_update_hx_view,
	detailQuotation_hx,
	updateQuotation,
	detailQuotation,
  deleteQuotation,
  QuotationCreate,
	delete_sizeprice,
  QuotationUpdate,
  add_supplier,
  add_supplier_reload_supplier_dropdown,
  quotation_chart_data,
  price_chart_data_multiple
)

app_name = 'quotation'
urlpatterns = [
	path('', listQuotation, name='list'),
	path('create/', createQuotation, name='create'),
  path('create-supplier/', add_supplier, name='create_supplier'),
  path('create-new/', QuotationCreate.as_view(), name='create_new'),
  path('update/<int:pk>/', QuotationUpdate.as_view(), name='update_quotation'),
  path('delete-sizeprice/<int:pk>/', delete_sizeprice, name='delete_sizeprice'),
	path('hx/<int:parent_id>/sizeprice/<int:id>/', detailSizePrice_update_hx_view, name='hx-sizeprice-detail'),
	path("hx/<int:parent_id>/sizeprice/", detailSizePrice_update_hx_view, name='hx-sizeprices-create'),
	path('hx/<int:id>/', detailQuotation_hx, name='hx-detail'),
	path('<int:id>/edit/', updateQuotation, name='edit'),
  path('<int:id>/delete/', deleteQuotation, name='delete'),
	path('<int:id>/', detailQuotation, name='detail'),
	path('add_supplier_reload', add_supplier_reload_supplier_dropdown, name='add_supplier_reload'),
  path('chart-data/', quotation_chart_data, name='quotation_chart_data'),
  path('chart-data-multiple/', price_chart_data_multiple, name='price_chart_data_multiple')
]