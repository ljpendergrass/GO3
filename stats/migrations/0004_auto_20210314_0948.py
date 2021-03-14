# Generated by Django 3.1.7 on 2021-03-14 13:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0011_auto_20210313_1757'),
        ('stats', '0003_auto_20210314_0917'),
    ]

    operations = [
        migrations.CreateModel(
            name='BandMetric',
            fields=[
                ('metric_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='stats.metric')),
                ('band', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='metrics', to='band.band')),
            ],
            bases=('stats.metric',),
        ),
        migrations.DeleteModel(
            name='BandStat',
        ),
    ]
