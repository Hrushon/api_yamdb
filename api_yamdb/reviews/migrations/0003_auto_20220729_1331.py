# Generated by Django 2.2.16 on 2022-07-29 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220729_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='titles',
            name='description',
            field=models.TextField(default='to describe', null=True),
        ),
    ]