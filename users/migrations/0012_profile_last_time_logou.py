# Generated by Django 3.0.6 on 2020-06-19 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20200617_0247'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='last_time_logou',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]