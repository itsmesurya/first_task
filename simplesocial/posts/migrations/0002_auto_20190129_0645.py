# Generated by Django 2.1.5 on 2019-01-29 06:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ['-dead_line']},
        ),
        migrations.RenameField(
            model_name='post',
            old_name='created_at',
            new_name='dead_line',
        ),
    ]
