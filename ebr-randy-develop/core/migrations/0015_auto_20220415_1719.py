# Generated by Django 3.2.12 on 2022-04-15 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_remove_reviewgeneral_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewbrand',
            name='featured_review',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='reviewcategory',
            name='featured_review',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]