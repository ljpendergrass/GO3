# Generated by Django 3.0 on 2020-01-05 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0011_assoc_color'),
        ('gig', '0006_gig_band'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gig',
            name='band',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='gigs', to='band.Band'),
            preserve_default=False,
        ),
    ]