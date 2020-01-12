# Generated by Django 3.0 on 2020-01-12 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0013_auto_20200111_2241'),
        ('gig', '0013_auto_20200111_2319'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='band.Section', verbose_name='section'),
        ),
    ]