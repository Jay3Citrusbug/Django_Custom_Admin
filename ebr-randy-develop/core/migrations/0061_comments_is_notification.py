# Generated by Django 3.2.12 on 2022-09-07 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0060_alter_pages_demo_page_bike_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='is_notification',
            field=models.BooleanField(default=False),
        ),
    ]
