# Generated by Django 3.2.12 on 2022-04-25 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_auto_20220420_1658'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pages',
            options={'verbose_name': 'Page', 'verbose_name_plural': 'Pages'},
        ),
        migrations.AlterModelOptions(
            name='pagesreview',
            options={'verbose_name': 'Page Review', 'verbose_name_plural': 'Pages Reviews'},
        ),
        migrations.AddField(
            model_name='reviewgalley',
            name='order',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
