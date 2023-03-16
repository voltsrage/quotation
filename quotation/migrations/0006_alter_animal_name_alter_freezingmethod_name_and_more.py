# Generated by Django 4.1.4 on 2023-02-19 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quotation", "0005_alter_port_telephone"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="freezingmethod",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="harvestingmethod",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="incoterm",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="priceunit",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="processingmethod",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name="specie",
            name="name",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]