# Generated by Django 3.2.12 on 2022-09-29 05:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0066_auto_20220928_0958'),
    ]

    operations = [
        migrations.RenameField(
            model_name='visitorhistory',
            old_name='type_name_id',
            new_name='type_id',
        ),
    ]
