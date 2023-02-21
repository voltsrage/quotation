# Generated by Django 4.1.4 on 2023-02-19 07:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("quotation", "0006_alter_animal_name_alter_freezingmethod_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="animal",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="catchtype",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="country",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="currency",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="freezingmethod",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="harvestingmethod",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="incoterm",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="port",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="priceunit",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="processingmethod",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="scientificname",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="specie",
            options={"ordering": ["name"]},
        ),
        migrations.AlterModelOptions(
            name="supplier",
            options={"ordering": ["name"]},
        ),
    ]
