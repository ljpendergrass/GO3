# Generated by Django 3.1.7 on 2021-04-04 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0011_auto_20210313_1757'),
        ('gig', '0010_auto_20210404_1255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plan',
            name='assoc',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plans', to='band.assoc', verbose_name='assoc'),
        ),
    ]