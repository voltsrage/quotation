from django import forms
from .models import *
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

class QuotationFilterForm(forms.Form):
	processing_method = forms.ModelChoiceField(queryset=ProcessingMethod.objects.all(), required=False)
	harvesting_method = forms.ModelChoiceField(queryset=HarvestingMethod.objects.all(), required=False)
	freezing_method = forms.ModelChoiceField(queryset=FreezingMethod.objects.all(), required=False)
	specie = forms.ModelChoiceField(queryset=Specie.objects.all(), required=False)
	origin = forms.ModelChoiceField(queryset=Country.objects.all(), required=False)
	destination = forms.ModelChoiceField(queryset=Port.objects.all(), required=False)
	years =forms.ModelChoiceField(queryset= Quotation.objects.order_by('recieved_date__year').values_list('recieved_date__year', flat=True).distinct(), required=False)
	start_date = forms.DateField(input_formats='%Y,%m,%d',widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}), required=False)
	end_date = forms.DateField(input_formats='%Y,%m,%d',widget=forms.DateInput(attrs={'type':'date','class': 'form-control'}), required=False)

