# Generated by Django 3.2.12 on 2022-11-17 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_auto_20221014_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitorhistory',
            name='type_url',
            field=models.TextField(),
        ),
    ]
