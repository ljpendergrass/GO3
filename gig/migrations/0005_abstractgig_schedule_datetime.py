# Generated by Django 3.0 on 2020-01-26 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gig', '0004_auto_20200121_2028'),
    ]

    operations = [
        migrations.AddField(
            model_name='abstractgig',
            name='schedule_datetime',
            field=models.DateTimeField(blank=True, default=None),
            preserve_default=False,
        ),
    ]
