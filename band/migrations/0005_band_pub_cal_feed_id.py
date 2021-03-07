# Generated by Django 3.0.7 on 2021-03-07 18:56

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('band', '0004_band_pub_cal_feed_dirty'),
    ]

    operations = [
        migrations.AddField(
            model_name='band',
            name='pub_cal_feed_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
    ]
