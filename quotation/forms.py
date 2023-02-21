from django import forms
from .models import Quotation, SizePrice

class QuotationForm(forms.ModelForm):
	recieved_date = forms.DateField(
		widget=forms.DateTimeInput(attrs={'type':'date'})
		)
	note = forms.CharField(
		widget=forms.Textarea(attrs={'rows':5})
	)
	class Meta:
		model = Quotation
		exclude = ('create_by',)


class SizePriceForm(forms.ModelForm):
	class Meta:
		model = SizePrice
		exclude = ('create_by',)