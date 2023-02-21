from django.shortcuts import render
from django.http import HttpResponse,Http404


def dashboard(request):
	return render(request, 'dashboard.html', {})