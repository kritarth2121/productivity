# Generated by Django 3.0.6 on 2020-06-17 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_delete_teammember'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='work_today',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
