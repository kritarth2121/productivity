# Generated by Django 3.0.6 on 2020-06-16 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_delete_teammember'),
        ('users', '0005_auto_20200615_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='team',
            field=models.ForeignKey( on_delete=django.db.models.deletion.CASCADE, to='blog.Team'),
            preserve_default=False,
        ),
    ]
