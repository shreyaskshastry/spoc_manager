# Generated by Django 3.1.2 on 2021-12-16 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spoc', '0007_merge_20211216_1034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spoc',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]