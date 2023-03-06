from django import forms
from .models import Quotation, SizePrice,Supplier
from django.forms import inlineformset_factory

class QuotationForm(forms.ModelForm):
	recieved_date = forms.DateField(
		widget=forms.DateInput(attrs={'type':'date'})
		)
	note = forms.CharField(
		widget=forms.Textarea(attrs={'rows':5})
	)
	class Meta:
		model = Quotation
		exclude = ('create_by',)


class SupplierForm(forms.ModelForm):
	class Meta:
		model = Supplier
		exclude = ('create_by',)
		widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control'
                    }
                ),
        }

	def clean_name(self):
		name = self.cleaned_data['name']
		if Supplier.objects.filter(name=name):
			raise forms.ValidationError(
				'Supplier with this name already exists'
			)
		else:
			return name

class SizePriceForm(forms.ModelForm):
	net_weight_box = forms.DecimalField(max_digits=6,decimal_places=2,widget=forms.NumberInput(attrs={
                    'class': 'form-control', 'step': 0.01, 'placeholder':'NetWeight/box (kg)' }),required=False)
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
	extra=1, can_delete=True, can_delete_extra=True, can_order=True
)