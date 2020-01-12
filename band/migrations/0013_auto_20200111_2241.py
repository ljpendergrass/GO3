# Generated by Django 3.0 on 2020-01-12 03:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0012_auto_20200111_2228'),
    ]

    operations = [
        migrations.AddField(
            model_name='assoc',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='assoc',
            name='status',
            field=models.IntegerField(choices=[(0, 'Not Confirmed'), (1, 'Confirmed'), (2, 'Invited'), (3, 'Alumni'), (4, 'Pending')], default=0),
        ),
    ]