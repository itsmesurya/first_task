# Generated by Django 2.1.5 on 2019-01-31 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20190129_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='current_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='message',
            field=models.TextField(max_length=100),
        ),
        migrations.AlterField(
            model_name='post',
            name='message_html',
            field=models.TextField(editable=False, max_length=100),
        ),
    ]
