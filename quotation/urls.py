from django.urls import path
from . import views

app_name = 'quotation'
urlpatterns = [
	path('', views.listQuotation, name='list'),
	path('create/', views.createQuotation, name='create'),
	path('<int:id>/', views.detailQuotation, name='detail'),
	path('<int:id>/edit', views.updateQuotation, name='edit'),
]