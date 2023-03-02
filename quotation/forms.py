from django import forms
from .models import Quotation, SizePrice
from django.forms import inlineformset_factory

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
		widgets = {
            'size': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'price_unit': forms.Select(
                attrs={
                    'class': 'form-control priceunit'
                    }
                ),
						'currency': forms.Select(
                attrs={
                    'class': 'form-control'
                    }
                ),
            'price': forms.NumberInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }


SizeFormSet = inlineformset_factory(
	Quotation, SizePrice, form=SizePriceForm,
	extra=1, can_delete=True, can_delete_extra=True
)