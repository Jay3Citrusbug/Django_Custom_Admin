# Generated by Django 3.2.12 on 2022-12-06 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0076_alter_product_product_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
