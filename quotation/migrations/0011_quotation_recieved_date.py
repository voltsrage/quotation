# Generated by Django 4.1.4 on 2023-02-19 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("quotation", "0010_processingmethod_note"),
    ]

    operations = [
        migrations.AddField(
            model_name="quotation",
            name="recieved_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
