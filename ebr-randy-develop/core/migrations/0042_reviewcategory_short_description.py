# Generated by Django 3.2.12 on 2022-06-02 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_pages_keyword'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewcategory',
            name='short_description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
