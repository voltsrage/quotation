<!-- jQuery -->
<script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
<!-- jQuery UI -->
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js"></script>

# models.py
from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=255)

class Brand(models.Model):
    name = models.CharField(max_length=255)

class Category(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    createdate = models.DateTimeField(auto_now_add=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.brand} {self.category}"
      
      
  # forms.py
from django import forms
from .models import Supplier, Brand, Category

class ProductFilterForm(forms.Form):
    supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), required=False)
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False)
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

# views.py
from django.shortcuts import render
from .models import Product
from .forms import ProductFilterForm

def product_table(request):
    products = Product.objects.all()
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data['supplier']:
            products = products.filter(supplier=form.cleaned_data['supplier'])
        if form.cleaned_data['brand']:
            products = products.filter(brand=form.cleaned_data['brand'])
        if form.cleaned_data['category']:
            products = products.filter(category=form.cleaned_data['category'])

    context = {'products': products, 'form': form}
    return render(request, 'product_table.html', context)
  
  <!-- product_table.html -->
{% extends "base.html" %}

{% block content %}
<form id="product-filter-form" method="get">
  <table>
    <thead>
      <tr>
        <th>Price</th>
        <th>
          <select name="supplier" id="id_supplier">
            <option value="">All Suppliers</option>
            {% for supplier in form.supplier.field.queryset %}
            <option value="{{ supplier.pk }}">{{ supplier }}</option>
            {% endfor %}
          </select>
        </th>
        <th>Create Date</th>
        <th>
          <select name="brand" id="id_brand">
            <option value="">All Brands</option>
            {% for brand in form.brand.field.queryset %}
            <option value="{{ brand.pk }}">{{ brand }}</option>
            {% endfor %}
          </select>
        </th>
        <th>
          <select name="category" id="id_category">
            <option value="">All Categories</option>
            {% for category in form.category.field.queryset %}
            <option value="{{ category.pk }}">{{ category }}</option>
{% endfor %}
</select>
</th>
</tr>
</thead>
<tbody>
{% for product in products %}
<tr>
<td>{{ product.price }}</td>
<td>{{ product.supplier }}</td>
<td>{{ product.createdate }}</td>
<td>{{ product.brand }}</td>
<td>{{ product.category }}</td>
</tr>
{% empty %}
<tr>
<td colspan="5">No products found.</td>
</tr>
{% endfor %}
</tbody>

  </table>
</form>
{% endblock %}

{% block extra_js %}

<script>
  $(document).ready(function () {
    // Update the table with AJAX when a filter is changed
    $("#id_supplier, #id_brand, #id_category").on("change", function () {
      $.ajax({
        url: "{% url 'product_table' %}",
        data: $("#product-filter-form").serialize(),
        success: function (data) {
          // Replace the table with the updated one
          $("table").replaceWith($(data).find("table"));
        },
        error: function (xhr, status, error) {
          console.error("AJAX error:", status, error);
        },
      });
    });
  });
</script>
{% endblock %}

6. Add a URL pattern for the view in your `urls.py`:

```python
# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('product_table/', views.product_table, name='product_table'),
]
  
