# models.py
from django.db import models

class Product(models.Model):
    brand = models.CharField(max_length=50)
    supplier = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    
 # forms.py
from django import forms
from .models import Product

class ProductForm(forms.Form):
    brand_filter = forms.CharField(max_length=50)
    supplier_filter = forms.CharField(max_length=50)
    price_filter = forms.DecimalField(max_digits=8, decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['brand_filter'].widget.attrs.update({'class': 'form-control'})
        self.fields['supplier_filter'].widget.attrs.update({'class': 'form-control'})
        self.fields['price_filter'].widget.attrs.update({'class': 'form-control'})

    products = Product.objects.all()

    def as_table(self):
        rows = []
        for product in self.products:
            rows.append(f"<tr><td>{product.brand}</td><td>{product.supplier}</td><td>{product.price}</td></tr>")
        return mark_safe(f"<table class='table'><thead><tr><th>Brand</th><th>Supplier</th><th>Price</th></tr></thead><tbody>{''.join(rows)}</tbody></table>")
      
    <!-- template.html -->
{% load static %}

<form id="product-form" method="POST">
    {% csrf_token %}
    <div class="form-group">
        {{ form.brand_filter.label_tag }}
        {{ form.brand_filter }}
    </div>
    <div class="form-group">
        {{ form.supplier_filter.label_tag }}
        {{ form.supplier_filter }}
    </div>
    <div class="form-group">
        {{ form.price_filter.label_tag }}
        {{ form.price_filter }}
    </div>
    <div id="product-table">
        {{ form.as_table }}
    </div>
    <button type="submit" class="btn btn-primary">Submit</button>
</form>

<script src="{% static 'js/jquery.min.js' %}"></script>
<script>
    $(document).ready(function() {
        $('#product-form').on('submit', function(event) {
            event.preventDefault();
            $.ajax({
                type: 'POST',
                url: '',
                data: {
                    'brand_filter': $('#id_brand_filter').val(),
                    'supplier_filter': $('#id_supplier_filter').val(),
                    'price_filter': $('#id_price_filter').val(),
                     'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(response) {
                $('#product-table').html(response);
            },
            error: function(xhr, status, error) {
                console.error(error);
            }
        });
    });
});
  
  
  # views.py
from django.shortcuts import render
from django.http import JsonResponse
from .forms import ProductForm
from .models import Product

def product_filter(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            brand_filter = form.cleaned_data.get('brand_filter')
            supplier_filter = form.cleaned_data.get('supplier_filter')
            price_filter = form.cleaned_data.get('price_filter')
            products = Product.objects.filter(
                brand__icontains=brand_filter,
                supplier__icontains=supplier_filter,
                price__lte=price_filter,
            )
            form.products = products
            table_html = form.as_table()
            return JsonResponse({'table_html': table_html})
    else:
        form = ProductForm()
    return render(request, 'template.html', {'form': form})
                   
   
