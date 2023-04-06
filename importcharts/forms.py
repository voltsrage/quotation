from django import forms
from .models import *


class ImportFilterForm(forms.Form):
    commodity_code = forms.ModelChoiceField(queryset=Import.objects.order_by('commodity_code').values_list('commodity_code', flat=True).distinct(), required=False)
    country = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
    start_month = forms.ModelChoiceField(queryset=Import.objects.order_by('month').values_list('month', flat=True).distinct(), required=False)
    end_month = forms.ModelChoiceField(queryset=Import.objects.order_by('month').values_list('month', flat=True).distinct(), required=False)
    production_description = forms.ModelChoiceField(queryset=Import.objects.order_by('production_description').values_list('production_description', flat=True).distinct(), required=False)