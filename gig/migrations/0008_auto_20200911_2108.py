# Generated by Django 3.0.7 on 2020-09-12 01:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gig', '0007_gigcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='gig',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='historicalgig',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]