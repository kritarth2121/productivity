# Generated by Django 2.2.4 on 2020-05-20 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20200511_1631'),
    ]

    operations = [
        migrations.CreateModel(
            name='Views',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('view', models.IntegerField(default=0)),
            ],
        ),
    ]
