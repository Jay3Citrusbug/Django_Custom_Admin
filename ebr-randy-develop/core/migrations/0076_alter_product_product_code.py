# Generated by Django 3.2.12 on 2022-12-06 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0075_alter_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_code',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]