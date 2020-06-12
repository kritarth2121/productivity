# Generated by Django 3.0.6 on 2020-06-09 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_views'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='description',
            new_name='work_done',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='work',
            new_name='work_today',
        ),
        migrations.RemoveField(
            model_name='post',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='post',
            name='status',
        ),
    ]
