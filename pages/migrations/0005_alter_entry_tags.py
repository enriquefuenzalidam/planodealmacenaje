# Generated by Django 5.0.3 on 2024-04-02 23:07

import pages.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_entry_description_date_file_image_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=pages.models.LowercaseTextField(verbose_name='Tags'),
        ),
    ]
