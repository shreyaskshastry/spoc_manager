# Generated by Django 3.1.2 on 2021-12-15 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spoc', '0003_auto_20211215_1428'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spoc',
            name='created_date',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='spoc',
            name='modified_date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
